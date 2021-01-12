from tkinter import *
from PIL import ImageTk,Image
import glob

#initialize root widget and path data
root = Tk()
root.withdraw()
path = input("Enter absolute folder path: ")
pic_lst = glob.glob(path + "/*.png")
root.title("PNG Viewer")
root.deiconify()

#set image variables
img_dct = dict()
for i in range(len(pic_lst)):
    exec(f'my_img_{i} = pic_lst[{i}]')
    exec(f'img_dct["my_img_" + str(i)] = my_img_{i}')

#OPTION TO FIX ASPECT RATIO
# fixed_width = 400
# def resize_aspect_ratio(im):
#     global fixed_width
#     basewidth = fixed_width
#     wpercent = (basewidth/float(im.size[0]))
#     hsize = int((float(im.size[1])*float(wpercent)))
#     im = im.resize((basewidth,hsize), Image.ANTIALIAS)
#     return im
# Then, change ImageTk.PhotoImage(im) ->
#   ImageTk.PhotoImage(resize_aspect_ratio(im)) in final_image_list

image_list = [Image.open(img_dct[var_name]) for var_name in img_dct.keys()]
final_image_list = [ImageTk.PhotoImage(im) for im in image_list]

#set status bar
status = Label(root, text = "Image 1 of " + str(len(final_image_list)), bd = 1, relief = SUNKEN, anchor = E)

#initialize first image label
my_label = Label(image = final_image_list[0])
my_label.grid(row = 1, column = 1, sticky = "nesw")
my_label.grid(row = 0, column = 0, columnspan = 3)

###############################
## define functionality of buttons
###############################
def forward(image_number):
    global my_label, button_forward, button_back
    my_label.grid_forget()
    my_label = Label(image = final_image_list[image_number - 1])
    my_label.grid(row = 0, column = 0, columnspan = 3)

    #update buttons
    button_back = Button(root, text = "<<",
        command = lambda: back(image_number - 1))
    button_forward = Button(root, text = ">>",
        command = lambda: forward(image_number + 1))

    #Key press functionality
    def left_press(event=None):
        if image_number == 1:
            button_back = Button(root, text = "<<", state = DISABLED)
            return
        back(image_number - 1)
    root.bind('<Left>', left_press)

    def right_press(event=None):
        if image_number == len(final_image_list):
            button_forward = Button(root, text = ">>", state = DISABLED)
            return
        forward(image_number + 1)
    root.bind('<Right>', right_press)

    root.bind("<Escape>", lambda x: root.destroy())

    if image_number == len(final_image_list):
        button_forward = Button(root, text = ">>", state = DISABLED)

    button_back.grid(row = 1, column = 0)
    button_forward.grid(row = 1, column = 2, pady = 10)

    #update status bar
    status = Label(root, text = "Image " + str(image_number) + " of " + str(len(final_image_list)), bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 2, column = 0, columnspan = 3, sticky = W+E)

def back(image_number):
    global my_label, button_forward, button_back
    my_label.grid_forget()
    my_label = Label(image = final_image_list[image_number - 1])
    my_label.grid(row = 0, column = 0, columnspan = 3)

    #update buttons
    button_back = Button(root, text = "<<",
        command = lambda: back(image_number - 1))
    button_forward = Button(root, text = ">>",
        command = lambda: forward(image_number + 1))

    #Key press functionality
    def left_press(event=None):
        if image_number == 1:
            button_back = Button(root, text = "<<", state = DISABLED)
            return
        back(image_number - 1)
    root.bind('<Left>', left_press)

    def right_press(event=None):
        if image_number == len(final_image_list):
            button_forward = Button(root, text = ">>", state = DISABLED)
            return
        forward(image_number + 1)
    root.bind('<Right>', right_press)

    root.bind("<Escape>", lambda x: root.destroy())

    if image_number == 1:
        button_back = Button(root, text = "<<", state = DISABLED)

    button_back.grid(row = 1, column = 0)
    button_forward.grid(row = 1, column = 2, pady = 10)

    #update status bar
    status = Label(root, text = "Image " + str(image_number) + " of " + str(len(final_image_list)), bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 2, column = 0, columnspan = 3, sticky = W+E)

#accounts for initial forward and esc key press
def right_press(event=None):
    forward(2)
root.bind('<Right>', right_press)

root.bind("<Escape>", lambda x: root.destroy())

button_back = Button(root, text = "<<", command = lambda: back(), state = DISABLED)
button_exit = Button(root, text = "EXIT", command = root.quit)
button_forward = Button(root, text = ">>", command = lambda: forward(2))

#put buttons on the screen
button_back.grid(row = 1, column = 0)
button_exit.grid(row = 1, column = 1)
button_forward.grid(row = 1, column = 2, pady = 10)
status.grid(row = 2, column = 0, columnspan = 3, sticky = W+E)

root.mainloop()
