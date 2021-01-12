from tkinter import *
import util as ut

#Set the root object for tkinter
root = Tk()
root.title("Simple Calculator")

#set the entry object
e = Entry(root, width = 35, borderwidth = 5)
e.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

#define buttons
button_1 = Button(root, text = "1", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 1))
button_2 = Button(root, text = "2", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 2))
button_3 = Button(root, text = "3", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 3))
button_4 = Button(root, text = "4", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 4))
button_5 = Button(root, text = "5", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 5))
button_6 = Button(root, text = "6", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 6))
button_7 = Button(root, text = "7", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 7))
button_8 = Button(root, text = "8", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 8))
button_9 = Button(root, text = "9", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 9))
button_0 = Button(root, text = "0", padx = 40, pady = 20,
    command = lambda: ut.button_click(e, 0))

button_add = Button(root, text = "+", padx = 39, pady = 20,
    command = lambda: ut.button_add(e))
button_sub = Button(root, text = "-", padx = 39, pady = 20,
    command = lambda: ut.button_sub(e))
button_mult = Button(root, text = "*", padx = 39, pady = 20,
    command = lambda: ut.button_mult(e))
button_div = Button(root, text = "/", padx = 39, pady = 20,
    command = lambda: ut.button_div(e))
button_equal = Button(root, text = "=", padx = 89, pady = 20,
    command = lambda: ut.button_equal(e))
button_mod = Button(root, text = "%", padx = 38, pady = 20,
    command = lambda: ut.button_mod(e))
button_pow = Button(root, text = "^", padx = 39, pady = 20,
    command = lambda: ut.button_pow(e))

button_clear = Button(root, text = "Clear", padx = 100, pady = 20,
    command = lambda: ut.button_clear(e))

#put buttons on the screen
button_1.grid(row = 3, column = 0)
button_2.grid(row = 3, column = 1)
button_3.grid(row = 3, column = 2)
button_4.grid(row = 2, column = 0)
button_5.grid(row = 2, column = 1)
button_6.grid(row = 2, column = 2)
button_7.grid(row = 1, column = 0)
button_8.grid(row = 1, column = 1)
button_9.grid(row = 1, column = 2)
button_0.grid(row = 4, column = 0)

button_equal.grid(row = 4, column = 1, columnspan = 2)
button_clear.grid(row = 7, column = 0, columnspan = 3)

button_add.grid(row = 5, column = 0)
button_sub.grid(row = 5, column = 1)
button_mult.grid(row = 5, column = 2)
button_div.grid(row = 6, column = 0)
button_mod.grid(row = 6, column = 1)
button_pow.grid(row = 6, column = 2)

#necessary tkinter loop
root.mainloop()
