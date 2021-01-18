from tkinter import *
import sqlite3
from tkinter import messagebox

root = Tk()
root.title("Database Entry Form")

#set status bar
status = Label(root, text = "status: ", bd = 1, relief = SUNKEN, anchor = E)
status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

#Create a database/ connect to one
conn = sqlite3.connect("address_book.db")

#Create cursor
c = conn.cursor()

#######################################################################
## Create table (only need to run once)
#######################################################################
# c.execute("""
#     CREATE TABLE addresses (
#     first_name text,
#     last_name text,
#     address text,
#     city text,
#     state text,
#     zipcode integer)
#     """)

#Create updating functionality for the update function
def updater_func(editor):

    record_id = select_box.get()

    #Create a database/ connect to one
    conn = sqlite3.connect("address_book.db")

    #Create cursor
    c = conn.cursor()

    c.execute("""
    UPDATE addresses SET

    first_name = :first,
    last_name = :last,
    address = :address,
    city = :city,
    state = :state,
    zipcode = :zipcode

    WHERE oid = :oid
    """, {
    'first': f_name_editor.get(),
    'last': l_name_editor.get(),
    'address': address_editor.get(),
    'city': city_editor.get(),
    'state':state_editor.get(),
    'zipcode': zipcode_editor.get(),
    'oid': record_id
    })

    #Commit changes
    conn.commit()

    #Close connection
    conn.close()

    #Refresh status bar
    status = Label(root, text = "status: Record Updated", bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

    editor.destroy()

#Create function to delete a record
def delete():

    conn = sqlite3.connect("address_book.db")

    #Create cursor
    c = conn.cursor()

    oids = c.execute("SELECT rowid FROM addresses")
    oid_list = []
    [oid_list.append(str(x[0])) for x in oids]

    try:
        #Delete a record
        c.execute("DELETE FROM addresses WHERE oid = " + select_box.get())
        #implicit conversion too! (thanks to sql or thanks to python?)
    except:
        #set default deletion ID
        select_box.insert(0, 0)
        c.execute("DELETE FROM addresses WHERE oid = " + select_box.get())
        #Clear text boxes
        select_box.delete(0, END)

    #just for aesthetics, doesn't really do anything
    if str(select_box.get()) not in oid_list:
        #update status bar
        status = Label(root, text = "status: Deletion Rejected", bd = 1, relief = SUNKEN, anchor = E)
        status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

        messagebox.showerror("Error", "ID does not exist")
        return

    #Clear text box
    select_box.delete(0, END)

    conn.commit()

    conn.close()

    status = Label(root, text = "status: Record Deleted", bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)


#Create submit function for Database
def submit(event = None): #the arguement is for the key bind functionality

    conn = sqlite3.connect("address_book.db")

    c = conn.cursor()

    #Insert Into TABLE
    c.execute("""INSERT INTO addresses VALUES (
        :f_name, :l_name, :address, :city, :state, :zipcode)""",
        {
            'f_name':f_name.get(),
            'l_name':l_name.get(),
            'address': address.get(),
            'city':city.get(),
            'state':state.get(),
            'zipcode': zipcode.get(),
        })

    get_list = [f_name.get(), l_name.get(), address.get(), city.get(),
        state.get(), zipcode.get()]

    for i in get_list:
        if i == '':
            ans = messagebox.askyesno("Warning", "Entry has missing fields. Continue?")
            if ans == 1:
                status = Label(root, text = "status: Entry Submitted", bd = 1, relief = SUNKEN, anchor = E)
                status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)
                break
            else:
                c.execute('rollback')
                status = Label(root, text = "status: Entry Rejected", bd = 1, relief = SUNKEN, anchor = E)
                status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)
                break

    #Clear text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

    status = Label(root, text = "status: Entry Submitted", bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

    conn.commit()

    conn.close()

#Create query function
def query():
    global print_frame

    conn = sqlite3.connect("address_book.db")

    c = conn.cursor()

    #Query the Database
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall() #or fetchone, fetchmany(50)

    # destory frame if exists (i.e. inital button press)
    if "print_frame" in globals():
        print_frame.grid_forget()

    #Loop through results
    print_records = ""
    print_frame = LabelFrame(root, text = "Summary of Database: ", borderwidth = 0, highlightthickness = 0)
    print_frame.grid(row = 9, columnspan = 2)

    oids = c.execute("SELECT rowid FROM addresses")
    oid_list = []
    [oid_list.append(str(x[0])) for x in oids]

    for record in records:
        if record[6] != oid_list[-1]:
            print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[4]) + ", " + str(record[6]) + "\n"
        else:
            print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[3]) + ", " + str(record[6])

    query_label = Label(print_frame, text = print_records, anchor = 'w').grid(row = 9, columnspan = 3)

    conn.commit()

    conn.close()

    status = Label(root, text = "status: Querying Database", bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

#Create hide function
def hide():
    if "print_frame" in globals():
        print_frame.grid_forget()

    status = Label(root, text = "status: ", bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

#create a function to edit an entry
def update():
    global print_frame, status

    status = Label(root, text = "status: Updating Record", bd = 1, relief = SUNKEN, anchor = E)
    status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

    editor = Tk()
    editor.title("Update Entry Form")

    conn = sqlite3.connect("address_book.db")

    c = conn.cursor()

    oids = c.execute("SELECT rowid FROM addresses")
    oid_list = []
    [oid_list.append(str(x[0])) for x in oids]

    record_id = select_box.get()

    try:
        c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    except:
        editor.update()
        editor.destroy()

        status = Label(root, text = "status: Update Failed", bd = 1, relief = SUNKEN, anchor = E)
        status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

        messagebox.showerror("Error", "ID does not exist")

        #set default deletion ID
        select_box.insert(0, 0)

        #Clear text boxes
        select_box.delete(0, END)
        return

    if str(select_box.get()) not in oid_list:
        #update status bar
        status = Label(root, text = "status: Update Rejected", bd = 1, relief = SUNKEN, anchor = E)
        status.grid(row = 100, column = 0, columnspan = 3, sticky = W+E)

        messagebox.showerror("Error", "ID does not exist")
        editor.update()
        editor.destroy()
        #Clear text boxes
        select_box.delete(0, END)
        return


    #Query the Database
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = c.fetchall() #or fetchone, fetchmany(50)

    conn.commit()

    conn.close()

    #for use in other functions
    global f_name_editor, l_name_editor, address_editor, city_editor, state_editor, zipcode_editor

    #Create text boxes
    f_name_editor = Entry(editor, width = 40, borderwidth = 2)
    f_name_editor.grid(row = 0, column = 1, pady = (10,0), padx = (0, 10))
    l_name_editor = Entry(editor, width = 40, borderwidth = 2)
    l_name_editor.grid(row = 1, column = 1, padx = (0, 10))
    address_editor = Entry(editor, width = 40, borderwidth = 2)
    address_editor.grid(row = 2, column = 1, padx = (0, 10))
    city_editor = Entry(editor, width = 40, borderwidth = 2)
    city_editor.grid(row = 3, column = 1, padx = (0, 10))
    state_editor = Entry(editor, width = 40, borderwidth = 2)
    state_editor.grid(row = 4, column = 1, padx = (0, 10))
    zipcode_editor = Entry(editor, width = 40, borderwidth = 2)
    zipcode_editor.grid(row = 5, column = 1, padx = (0, 10))

    #create text box labels
    f_name_label_editor = Label(editor, text = "First Name")
    f_name_label_editor.grid(row = 0, column = 0, sticky = 'w', padx = (10, 0), pady = (10,0))
    l_name_label_editor = Label(editor, text = "Last Name")
    l_name_label_editor.grid(row = 1, column = 0, sticky = 'w', padx = (10, 0))
    address_label_editor = Label(editor, text = "Address")
    address_label_editor.grid(row = 2, column = 0, sticky = 'w', padx = (10, 0))
    city_label_editor = Label(editor, text = "City")
    city_label_editor.grid(row = 3, column = 0, sticky = 'w', padx = (10, 0))
    state_label_editor = Label(editor, text = "State")
    state_label_editor.grid(row = 4, column = 0, sticky = 'w', padx = (10, 0))
    zipcode_label_editor = Label(editor, text = "Zipcode")
    zipcode_label_editor.grid(row = 5, column = 0, sticky = 'w', padx = (10, 0))

    #loop through results
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    #Create save button
    save_btn = Button(editor, text = "Save Updated Record", command = lambda: updater_func(editor))
    save_btn.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 146)


#Create text boxes
f_name = Entry(root, width = 40, borderwidth = 2)
f_name.grid(row = 0, column = 1, pady = (10,0), padx = (0, 10))
l_name = Entry(root, width = 40, borderwidth = 2)
l_name.grid(row = 1, column = 1, padx = (0, 10))
address = Entry(root, width = 40, borderwidth = 2)
address.grid(row = 2, column = 1, padx = (0, 10))
city = Entry(root, width = 40, borderwidth = 2)
city.grid(row = 3, column = 1, padx = (0, 10))
state = Entry(root, width = 40, borderwidth = 2)
state.grid(row = 4, column = 1, padx = (0, 10))
zipcode = Entry(root, width = 40, borderwidth = 2)
zipcode.grid(row = 5, column = 1, padx = (0, 10))
select_box = Entry(root, width = 40, borderwidth = 2)
select_box.grid(row = 10, column = 1, pady = (20, 0), padx = (0, 10))

#create text box labels
f_name_label = Label(root, text = "First Name")
f_name_label.grid(row = 0, column = 0, sticky = 'w', padx = (10, 0), pady = (10,0))
l_name_label = Label(root, text = "Last Name")
l_name_label.grid(row = 1, column = 0, sticky = 'w', padx = (10, 0))
address_label = Label(root, text = "Address")
address_label.grid(row = 2, column = 0, sticky = 'w', padx = (10, 0))
city_label = Label(root, text = "City")
city_label.grid(row = 3, column = 0, sticky = 'w', padx = (10, 0))
state_label = Label(root, text = "State")
state_label.grid(row = 4, column = 0, sticky = 'w', padx = (10, 0))
zipcode_label = Label(root, text = "Zipcode")
zipcode_label.grid(row = 5, column = 0, sticky = 'w', padx = (10, 0))
select_box_label = Label(root, text = "Select ID")
select_box_label.grid(row = 10, column = 0, sticky = 'w', padx = (10, 0), pady = (40, 0))



#Create submit Button
submit_btn = Button(root, text = "Add Record", command = submit)
submit_btn.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 136)

#create query button
query_btn = Button(root, text = "Show Records", command = query)
query_btn.grid(row = 7, column = 0, columnspan = 1, pady = 10, padx = (10, 0), ipadx = 45)

#Create hide Button
hide_btn = Button(root, text = "Hide Records", command = hide)
hide_btn.grid(row = 7, column = 1, columnspan = 1, pady = 10, ipadx = 45)

#Create delete button
delete_btn = Button(root, text = "Delete Record", command = delete)
delete_btn.grid(row = 11, column = 0, columnspan = 1, pady = 10, padx = (10, 0), ipadx = 45)

#Create update button
update_btn = Button(root, text = "Update Record", command = update)
update_btn.grid(row = 11, column = 1, columnspan = 1, pady = 10, ipadx = 45)




#Key binds
f_name.bind("<Return>", submit)
l_name.bind("<Return>", submit)
address.bind("<Return>", submit)
city.bind("<Return>", submit)
state.bind("<Return>", submit)
zipcode.bind("<Return>", submit)

conn.commit()

conn.close()

root.mainloop()
