"""
This module contains code which creates graphs of given functions
"""

from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


def change(input):
    """
    Function changes expressions in input.
    :param input: function given
    :return: changed expressions
    """
    input = input.replace("sin", "np.sin")
    input = input.replace("cos", "np.cos")
    input = input.replace("tan", "np.tan")
    input = input.replace("sqrt", "np.sqrt")
    input = input.replace("^", "**")
    input = input.replace("e", "np.e")
    input = input.replace("log", "np.log")
    input = input.replace("pi", "np.pi")
    return input


def create_graph(functions, title, legend, x_label, y_label, x_fr, x_to, y_fr, y_to):
    """
    Function creates plot.
    :param functions: functions to draw
    :param title: the function title
    :param legend: if legend
    :param x_label: label on x-axis
    :param y_label: label on y-axis
    :param x_fr: the range of
    :param x_to: the range of x-axis
    :param y_fr: the range
    :param y_to: the range of y-axis
    """
    func = functions.split(";")
    graph = Figure(figsize=(7, 5))
    pic = graph.add_subplot(111)
    x = np.linspace(x_fr, x_to)
    for figure in func:
        if "/0" in functions:
            messagebox.showwarning("WARNING!", 'You cannot divide by zero!')
        else:
            try:
                f = eval('lambda x: ' + change(figure))
                y = f(x)
                pic.plot(x, y)
            except Exception:
                messagebox.showwarning("WARNING!", 'You used wrong expression')

    pic.set_title(title)
    pic.set_xlim(x_fr, x_to)
    pic.set_ylim(y_fr, y_to)
    pic.set_xlabel(x_label)
    pic.set_ylabel(y_label)
    if legend.get() == 1:
        pic.legend(func)
    return graph


def func_draw():
    """
    Function creates interface for our app.
    """
    window = Tk()
    window.title("Function Graphs Drawer")
    window.geometry("1150x520+50+50")
    window.configure(bg='dark khaki')

    welcome_lbl = Label(window, font='Calibri 16 bold italic', text='Welcome to the Function Graphs Drawer!', bg='dark khaki')
    welcome_lbl.grid(row=0, columnspan=4)  # creates welcome

    func_txt = Label(window, font='Calibri 12', text='Enter Your Function(s):', bg='dark khaki')
    func_txt.grid(row=1, column=0, columnspan=2, rowspan=3)
    func_txt_entry = StringVar()
    func_txt_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=func_txt_entry)
    func_txt_entry.grid(row=1, column=2, columnspan=2, rowspan=3)  # creates entry writing a function

    blank_1 = Label(window, bg='dark khaki')
    blank_1.grid(row=5, column=1)

    func_ttl = Label(window, font='Calibri 12', text='Graph title:', bg='dark khaki')
    func_ttl.grid(row=6, column=0)
    func_ttl_entry = StringVar()
    func_ttl_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=func_ttl_entry)
    func_ttl_entry.grid(row=6, column=1)  # creates entry, graph title

    xlbl_ttl = Label(window, font='Calibri 12', text='XLabel title:', bg='dark khaki')
    xlbl_ttl.grid(row=7, column=0)
    xlbl_ttl_entry = StringVar()
    xlbl_ttl_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=xlbl_ttl_entry)
    xlbl_ttl_entry.grid(row=7, column=1)
    ylbl_ttl = Label(window, font='Calibri 12', text='YLabel title:', bg='dark khaki')
    ylbl_ttl.grid(row=8, column=0)
    ylbl_ttl_entry = StringVar()
    ylbl_ttl_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=ylbl_ttl_entry)
    ylbl_ttl_entry.grid(row=8, column=1)

    legend_chc = IntVar()
    choice = Checkbutton(variable=legend_chc, text='Legend', font='Calibri 12', onvalue=1, offvalue=0, bg='dark khaki')
    choice.grid(row=7, column=3)

    blank_2 = Label(window, bg='dark khaki')
    blank_2.grid(row=9, column=1)

    x_val = Label(window, font='Calibri 12', text='X values', bg='dark khaki')
    x_val.grid(row=10, columnspan=2)

    x_from = Label(window, font='Calibri 12', text='From:', bg='dark khaki')
    x_from.grid(row=11, column=0)
    x_fr_entry = StringVar()
    x_fr_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=x_fr_entry)
    x_fr_entry.grid(row=12, column=0)  # creates entry, from x

    x_to = Label(window, font='Calibri 12', text='To:', bg='dark khaki')
    x_to.grid(row=11, column=1)
    x_to_entry = StringVar()
    x_to_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=x_to_entry)
    x_to_entry.grid(row=12, column=1)  # creates entry, to x

    blank_3 = Label(window, bg='dark khaki')
    blank_3.grid(row=13, column=1)

    y_val = Label(window, font='Calibri 12', text='Y values', bg='dark khaki')
    y_val.grid(row=14, columnspan=2)

    y_from = Label(window, font='Calibri 12', text='From:', bg='dark khaki')
    y_from.grid(row=15, column=0)
    y_fr_entry = StringVar()
    y_fr_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=y_fr_entry)
    y_fr_entry.grid(row=16, column=0)  # creates entry, from y

    y_to = Label(window, font='Calibri 12', text='To:', bg='dark khaki')
    y_to.grid(row=15, column=1)
    y_to_entry = StringVar()
    y_to_entry = Entry(window, font='Calibri 12', bg='khaki', textvariable=y_to_entry)
    y_to_entry.grid(row=16, column=1)  # creates entry, to y

    blank_4 = Label(window, bg='dark khaki')
    blank_4.grid(row=5, column=4)

    canvas_0 = Canvas(window, bg='white')
    canvas_0.place(height=450, width=550, x=530, y=10)

    def draw_click():
        """
        Function that takes action after pushing a button.
        """
        try:
            x_1 = eval(change(x_fr_entry.get()))
            x_2 = eval(change(x_to_entry.get()))
            y_1 = eval(change(y_fr_entry.get()))
            y_2 = eval(change(y_to_entry.get()))
            graph = create_graph(func_txt_entry.get(), func_ttl_entry.get(), legend_chc, xlbl_ttl_entry.get(),
                                 ylbl_ttl_entry.get(), x_1, x_2, y_1, y_2)
            canvas = FigureCanvasTkAgg(graph, master=window)
            canvas.get_tk_widget().place(height=450, width=550, x=530, y=10)
            canvas.draw()
        except Exception:
            messagebox.showerror("ERROR!", 'Values should be int or float')

    btn_draw = Button(window, text='Draw!', command=draw_click, font='Calibri 16', bg='indian red')
    btn_draw.grid(row=11, column=2, columnspan=2, rowspan=2)  # creates frame and draws a function

    btn_quit = Button(window, text='Quit!', command=quit, font='Calibri 16', bg='sienna3')
    btn_quit.grid(row=15, column=2, columnspan=2, rowspan=2)

    window.mainloop()


func_draw()
