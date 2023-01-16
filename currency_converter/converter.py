from tkinter import *
from tkinter import messagebox
import urllib.request
import json
import os
import requests


def connection(host='http://api.nbp.pl/api/exchangerates/tables/c/today/?format=json', time=5):
    """
    Function checks if there is internet connection.
    :param host: (str) given page
    :param time: (int) timeout to check connection
    """
    try:
        urllib.request.urlopen(host, timeout=time)
        return True
    except (ConnectionError, TimeoutError):
        print("No internet connection")
        return False


def get_rates(internet_on):
    """
    Function gets rates of the currencies from given page in function connection.
    :param internet_on: function to check connection
    """
    if internet_on is True:
        data = requests.get('http://api.nbp.pl/api/exchangerates/tables/c/today/?format=json').json()[0]
        rates = data['rates']
        data_date = data['effectiveDate']
        files = os.listdir(os.getcwd())
        for file in files:
            if file.startswith('currency_rates_') and file.endswith('txt'):
                os.remove(file)
        with open('currency_rates_' + data_date + '.txt', "w") as f:
            json.dump(rates, f)
        return rates
    else:
        files = os.listdir(os.getcwd())
        for file in files:
            if file.endswith('txt'):
                with open(file) as f:
                    rates = json.load(rates)
        return rates


def get_currencies(currency):
    """
    Function gets currencies names.
    """
    currencies = []
    for i in currency:
        currencies.append(i['code'])
    return currencies


def open_window():
    """
    Function opens a window with converter.
    """
    internet_connection = connection()
    rates_file = get_rates(internet_connection)
    currency_codes = get_currencies(rates_file)

    window = Tk()

    window.title("Currencies converter")
    window.configure(background='peachpuff')
    window.geometry("470x230")
    window.resizable(0, 0)

    from_txt = Label(window, text='From', font='Calibri 15', bg='peachpuff')
    to_txt = Label(window, text='To', font='Calibri 15', bg='peachpuff')
    input_txt = Label(window, text='Money To Convert :', font='Calibri 15', bg='peachpuff')
    amount_txt = Label(window, text='Money Coverted :', font='Calibri 15', bg='peachpuff')

    input_amount = StringVar()
    output_amount = StringVar()
    choose_1 = StringVar()
    choose_2 = StringVar()
    choose_1.set("Select currency")
    choose_2.set("Select currency")

    def clear():
        """
        Function clears the amounts.
        """
        input_amount.set("")
        output_amount.set("")

    currency_menu_fr = OptionMenu(window, choose_1, *currency_codes)
    currency_menu_fr.configure(bg='light salmon')
    currency_menu_fr["menu"].config(bg='light salmon')
    currency_menu_fr.grid(row=1, column=1)
    currency_menu_to = OptionMenu(window, choose_2, *currency_codes)
    currency_menu_to.configure(bg='light salmon')
    currency_menu_to["menu"].config(bg='light salmon')
    currency_menu_to.grid(row=2, column=1)

    input_entry = Entry(window, textvariable=input_amount)
    output_frame = Label(window, textvariable=output_amount, bg="peachpuff", font="Calibri 16 bold")

    input_txt.grid(row=0, column=0)
    input_entry.grid(row=0, column=1)
    from_txt.grid(row=1, column=0)
    to_txt.grid(row=2, column=0)
    amount_txt.grid(row=3, column=0)

    def count(currency_from, currency_to, amount, rates_list):
        """
        Function converts the money from one currency to the other.
        :param currency_from: chosen currency from
        :param currency_to: chosen currency to
        :param amount: amount of money to convert
        :param rates_list: list of rates
        """
        from_amount = None
        to_amount = None
        for rate in rates_list:
            if currency_from == currency_to:
                messagebox.askretrycancel("warning", 'You can not covert the same currency! Choose a different one.')
                break
            else:
                if rate['code'] == currency_from:
                    from_amount = rate
                if rate['code'] == currency_to:
                    to_amount = rate
        calculate_pln = amount * from_amount['bid']
        calculate_to = calculate_pln / to_amount['bid']
        return format(calculate_to, '.2f')

    def click():
        """
        Counting function.
        """
        try:
            value = count(choose_1.get(), choose_2.get(), float(input_amount.get()), rates_file)
            output_amount.set(value)
        except ValueError:
            messagebox.askretrycancel("warning", 'Amount type should be integar or with dot.')

    count_button = Button(window, text='Convert', bg='darkolivegreen', font='Calibri 14', command=click)
    clear_button = Button(window, text='Clear', bg='tomato', font='Calibri 14', command=clear)
    quit_button = Button(window, text='Quit', bg='goldenrod', font='Calibri 14', command=quit)
    count_button.grid(row=4, column=1)
    clear_button.grid(row=4, column=2)
    quit_button.grid(row=4, column=3)
    output_frame.grid(row=3, column=1)

    window.mainloop()


open_window()
