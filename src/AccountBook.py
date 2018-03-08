import datetime as dt
import pickle as pickle  # save class to file
import os

from util.add_months import add_months
from Account import Account
from Categorie import Categorie
from StandingOrder import StandingOrder

default_save_dir = "saved_data"


class AccountBook:
    def __init__(self, name="AccountBook"):
        self.name = name
        self.accounts = []
        self.categories = []
        self.standing_orders = []
        if not os.path.isdir(default_save_dir):
            os.mkdir(default_save_dir)
        self.file_path = os.path.join(default_save_dir, name + ".obj")

    def update(self):
        self.update_standing_orders()
        for acc in self.accounts:
            acc.update_interest()

    def new_account(self, *args):
        self.accounts.append(Account(*args))

    def new_categorie(self, *args):
        self.categories.append(Categorie(*args))

    def new_standing_order(
        self, src_acc_id, target_acc_id, amount, date=dt.date.today(),
        interval_months=1, categorie="", description="", bool_income=False
    ):
        self.standing_orders.append(StandingOrder(src_acc_id, target_acc_id,
                                                  amount, date,
                                                  interval_months,
                                                  categorie, description,
                                                  bool_income))

    def get_acc_array_pos(self, acc_id):
        for i, acc in enumerate(self.accounts):
            if acc.id == acc_id:
                return i
        return -1  # not found

    def update_standing_orders(self):
        for sto in self.standing_orders:
            while dt.date.today() >= sto.date:
                if sto.src_acc_id != 0:
                    pos = self.get_acc_array_pos(sto.src_acc_id)
                    self.accounts[pos].withdraw(sto.amount, sto.date,
                                                sto.categorie, sto.description,
                                                sto.bool_income)
                if sto.target_acc_id != 0:
                    pos = self.get_acc_array_pos(sto.target_acc_id)
                    self.accounts[pos].deposit(sto.amount, sto.date,
                                               sto.categorie, sto.description,
                                               sto.bool_income)
                sto.date = add_months(sto.date, sto.interval_months)

    def save(self):
        file_pi = open(self.file_path, 'wb')
        pickle.dump(self, file_pi)

    def save_as(self, file_path):
        self.file_path = file_path
        self.save()

    def load(self):
        filehandler = open(self.file_path, 'rb')
        loaded = pickle.load(filehandler)
        self.name = loaded.name
        self.accounts = loaded.accounts
        self.categories = loaded.categories
        self.standing_orders = loaded.standing_orders
        self.file_path = loaded.file_path

    def load_from(self, file_path):
        self.file_path = file_path
        self.load()
