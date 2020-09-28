from datetime import datetime
import pandas as pd
import numpy as np


class TransactionBook:
    def __init__(self, path=""):
        # Constants ToDo: Shall be initialized from configuration file
        #   Pandas dataframe headings
        self.DATE = "Date"
        self.ACCOUNT = "Account"
        self.DESCRIPTION = "Description"
        self.AMOUNT = "Amount"
        self.CATEGORY = "Category"
        #   Other constants
        self.CURRENCY = "€"
        self.DATE_TIME_FORMAT = "%d.%m.%Y"
        self.DATE_DELIMITER = "."

        # Init data set columns:
        self._data = pd.DataFrame(columns=[self.DATE, self.ACCOUNT, self.DESCRIPTION, self.AMOUNT, self.CATEGORY])

        self.path = path  # Hold the entire path to the database file including the filename
        self.accounts = []  # Holds the list of all accounts in the dataset
        self.categories = []  # Holds the list of all categories in the dataset

    # Accessors
    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def get_accounts(self):
        return self.accounts

    def set_accounts(self, accounts):
        self.accounts = accounts

    def get_categories(self):
        return self.categories

    def set_categories(self, categories):
        self.categories = categories

    def get_data(self):
        return self._data.copy()

    def set_data(self, data):
        self._data = data

    def add_account(self, account):
        if account not in self.accounts:
            self.accounts.append(account)
            self.accounts.sort()

    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
            self.categories.sort()

    def get_transaction_by_index(self, index):
        df = self.get_data()
        date = df[self.DATE].loc[index].strftime(self.DATE_TIME_FORMAT)
        account = df[self.ACCOUNT].loc[index]
        description = df[self.DESCRIPTION].loc[index]
        amount = df[self.AMOUNT].loc[index]
        category = df[self.CATEGORY].loc[index]

        return date, account, description, amount, category

    # Methods
    #   Transaction
    def new_transaction(self, date, account, description, amount, category):
        df = self.get_data()
        # If its the first element in the dataset: set index to 0, else: set index to the next index available
        index = 0 if np.isnan(df.index.max()) else (df.index.max() + 1)
        # Format date string to datetime object
        date = datetime.strptime(date, self.DATE_TIME_FORMAT)
        # Add transaction to dataset
        df.loc[index] = [date, account, description, amount, category]
        self.set_data(df)
        # Append lists if new category or account is added to data
        self.add_category(category)
        self.add_account(account)

    def edit_transaction(self, index, date, account, description, amount, category):
        date = datetime.strptime(date, self.DATE_TIME_FORMAT)
        self._data.loc[index] = [date, account, description, amount, category]
        # Append lists if new category or account is added to data
        self.add_category(category)
        self.add_account(account)

    def edit_transaction_field(self, index, field, content):
        if field == self.DATE:
            content = datetime.strptime(content, self.DATE_TIME_FORMAT)
        self._data[field].values[index] = content

    def delete_transaction(self, index):
        self._data = self._data.drop(index)

    #   Account
    def account_balance(self, account, data):
        df = data
        return df.loc[df[self.ACCOUNT] == account, self.AMOUNT].sum()

    def total_balance(self, data):
        df = data
        return df[self.AMOUNT].sum()

    def filter_date(self, from_date, to_date):
        data = self.get_data()
        df = data
        df = df.loc[df[self.DATE] >= from_date]
        df = df.loc[df[self.DATE] <= to_date]
        return df

    def populate_categories_from_data(self):
        df = self.get_data()
        categories = df[self.CATEGORY].unique()
        category_list = categories.tolist()
        category_list.sort()
        self.categories = category_list

    def populate_accounts_from_data(self):
        df = self.get_data()
        accounts = df[self.ACCOUNT].unique()
        self.accounts = accounts.tolist()

    def populate_lists_from_data(self):
        self.populate_categories_from_data()
        self.populate_accounts_from_data()

    def save(self):
        self.save_as(self.path)

    def save_as(self, file_path):
        df = self.get_data()
        df[self.DATE] = df[self.DATE].dt.strftime(self.DATE_TIME_FORMAT)
        df.to_csv(file_path, sep=';', index=False)

    def load(self):
        file_path = self.path
        self.load_from(file_path)

    def load_from(self, file_path):
        df = pd.read_csv(file_path, sep=';')
        df[self.DATE] = pd.to_datetime(df[self.DATE], format=self.DATE_TIME_FORMAT)
        self.set_data(df)
        self.populate_lists_from_data()

    def years(self):
        df = self.get_data()
        df["Year"] = [el.year for el in df[self.DATE]]
        years = df["Year"].unique()
        return years.tolist()

# Data aggregation methods:
    def pivot_monthly_trend(self, df_in, negative_amount_only=False):
        month = 'Month'
        df = df_in.copy()
        # Add additional helper column with months
        df[month] = [el.month for el in df[self.DATE]]
        df["Year"] = [el.year for el in df[self.DATE]]
        years = df["Year"].unique()
        years = years.tolist()
        year = max(years)
        df = df.loc[df["Year"] == year]  # Pivot latest year of data set
        # Create list with formatted months
        label = ["01.", "02.", "03.", "04.", "05.", "06.", "07.", "08.", "09.", "10.", "11.", "12."]
        label = [i + str(year) for i in label]
        # Init result list
        result = [0] * 12
        # Calculate balance at months
        if negative_amount_only:
            df = df.loc[df[self.AMOUNT] < 0]
        for i in range(1, 13):
            result[i - 1] = df.loc[df[month] == i, self.AMOUNT].sum()
        return label, result

    def pivot_category_pie(self, df_in, percent=False):
        # Filter for expenses -> negative amounts only
        df = df_in.copy()
        df = df.loc[df[self.AMOUNT] < 0]
        # Get categories which have a negative balance
        categories = df[self.CATEGORY].unique()
        categories = categories.tolist()
        # Init list of results
        result = [0] * len(categories)
        # Calculate negative sum for each category
        for i, cat in enumerate(categories):
            result[i] = df.loc[df[self.CATEGORY] == cat, self.AMOUNT].sum()
        # Sort lists ascending
        result, label = (list(t) for t in zip(*sorted(zip(result, categories))))
        # Calculate result in percent if requested
        if percent:
            sum_of_expenses = sum(result)
            for i, res in enumerate(result):
                result[i] = (res / sum_of_expenses) * 100
        return label, result
