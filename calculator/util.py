from tkinter import *

#operation functions
def button_add(e):
    global first_number, op_flag
    first_number = int(e.get())
    e.delete(0, END)
    op_flag = 'add'

def button_sub(e):
    global first_number, op_flag
    first_number = int(e.get())
    e.delete(0, END)
    op_flag = 'sub'

def button_mult(e):
    global first_number, op_flag
    first_number = int(e.get())
    e.delete(0, END)
    op_flag = 'mult'

def button_div(e):
    global first_number, op_flag
    first_number = int(e.get())
    e.delete(0, END)
    op_flag = 'div'

def button_mod(e):
    global first_number, op_flag
    first_number = int(e.get())
    e.delete(0, END)
    op_flag = 'mod'

def button_pow(e):
    global first_number, op_flag
    first_number = int(e.get())
    e.delete(0, END)
    op_flag = 'pow'

#Misc. functions
def button_equal(e):
    second_number = e.get()
    e.delete(0, END)
    e.insert(0, pick_operation(first_number, int(second_number)))

def button_click(e, number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, int(str(current) + str(number)))

def button_clear(e):
    e.delete(0, END)

def pick_operation(first, second):
    if op_flag == 'add':
        return first + second
    if op_flag == 'sub':
        return first - second
    if op_flag == 'mult':
        return first * second
    if op_flag == 'div':
        return first / second
    if op_flag == 'pow':
        return first ** second
    if op_flag == 'mod':
        return first % second
    else:
        raise ValueError
