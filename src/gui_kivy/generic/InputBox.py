from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class InputBox:
    def __init__(self, callback, title=""):
        self.text = ""
        self.callback = callback
        self.grid = GridLayout(cols=1)

        self.grid.input_text = TextInput(text=self.text)
        self.grid.ok = Button(text="OK")
        self.grid.add_widget(self.grid.input_text)
        self.grid.add_widget(self.grid.ok)

        self.popup = Popup(title=title, content=self.grid)
        self.grid.ok.bind(on_release=lambda _: self.cb_ok())

        self.popup.open()

    def cb_ok(self):
        self.text = self.grid.input_text.text
        self.callback(self.text)
        self.popup.dismiss()
