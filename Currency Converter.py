from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
import requests
import datetime as dt

# Converting stuff
class CurrencyConverter:

    def __init__(self, url):
        self.url = 'https://api.exchangerate.host/latest'
        self.update_rates()

    def update_rates(self):
        try:
            self.response = requests.get(self.url)
            self.data = self.response.json()
            self.rates = self.data.get('rates')
            self.last_updated = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to fetch exchange rates: {e}')

    def convert(self, amount, base_currency, des_currency):
        if base_currency != 'EUR':
            amount = amount / self.rates[base_currency]
        amount = round(amount * self.rates[des_currency], 2)
        return '{:,}'.format(amount)

# Main window
class Main(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Currency Converter')
        self.geometry('400x500')
        self.config(bg='#3A3B3C')
        self.CurrencyConverter = converter

        # Title Label
        self.title_label = Label(self, text='Currency Converter', bg='#3A3B3C', fg='white', font=('franklin gothic medium', 20))
        self.title_label.place(x=200, y=35, anchor='center')

        # Date and Version Labels
        self.date_label = Label(self, text=f'{dt.datetime.now():%A, %B %d, %Y}', bg='#3A3B3C', fg='white', font=('calibri', 10))
        self.date_label.place(x=0, y=500, anchor='sw')
        self.version_label = Label(self, text='v2.0', bg='#3A3B3C', fg='white', font=('calibri', 10))
        self.version_label.place(x=400, y=500, anchor='se')

        # Last Updated Label
        self.last_updated_label = Label(self, text=f'Last Updated: {self.CurrencyConverter.last_updated}', bg='#3A3B3C', fg='yellow', font=('calibri', 10))
        self.last_updated_label.place(x=200, y=70, anchor='center')

        # Amount Label and Entry
        self.amount_label = Label(self, text='Amount:', bg='#3A3B3C', fg='white', font=('franklin gothic book', 15))
        self.amount_label.place(x=200, y=100, anchor='center')
        self.amount_entry = Entry(self, width=25)
        self.amount_entry.place(x=200, y=130, anchor='center')

        # Currency Comboboxes
        self.currency_variable1 = StringVar(self)
        self.currency_variable2 = StringVar(self)
        self.currency_variable1.set('USD')
        self.currency_variable2.set('NPR')
        self.currency_combobox1 = ttk.Combobox(self, width=20, textvariable=self.currency_variable1, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox1.place(x=200, y=170, anchor='center')
        self.currency_combobox2 = ttk.Combobox(self, width=20, textvariable=self.currency_variable2, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox2.place(x=200, y=210, anchor='center')

        # Buttons
        self.convert_button = Button(self, text='Convert', bg='#52595D', fg='white', command=self.processed)
        self.convert_button.place(x=140, y=250, anchor='center')
        self.clear_button = Button(self, text='Clear', bg='red', fg='white', command=self.clear)
        self.clear_button.place(x=200, y=250, anchor='center')
        self.reverse_button = Button(self, text='Reverse', bg='#3B8CFF', fg='white', command=self.reverse_currency)
        self.reverse_button.place(x=260, y=250, anchor='center')
        self.refresh_button = Button(self, text='Refresh Rates', bg='green', fg='white', command=self.refresh_rates)
        self.refresh_button.place(x=200, y=290, anchor='center')

        # Result Label
        self.final_result = Label(self, text='', bg='#52595D', fg='white', font=('calibri', 12), relief='sunken', width=40)
        self.final_result.place(x=200, y=330, anchor='center')

    def clear(self):
        self.amount_entry.delete(0, END)
        self.final_result.config(text='')

    def reverse_currency(self):
        base = self.currency_variable1.get()
        des = self.currency_variable2.get()
        self.currency_variable1.set(des)
        self.currency_variable2.set(base)

    def refresh_rates(self):
        self.CurrencyConverter.update_rates()
        self.last_updated_label.config(text=f'Last Updated: {self.CurrencyConverter.last_updated}')
        messagebox.showinfo('Success', 'Exchange rates updated successfully!')

    def processed(self):
        try:
            given_amount = float(self.amount_entry.get())
            base_currency = self.currency_variable1.get()
            des_currency = self.currency_variable2.get()
            converted_amount = self.CurrencyConverter.convert(given_amount, base_currency, des_currency)
            self.final_result.config(text=f'{given_amount:,} {base_currency} = {converted_amount} {des_currency}')
        except ValueError:
            messagebox.showwarning('WARNING!', 'Please enter a valid amount!')

if __name__ == '__main__':
    url = 'https://api.exchangerate.host/latest'
    converter = CurrencyConverter(url)
    app = Main(converter)
    app.mainloop()
