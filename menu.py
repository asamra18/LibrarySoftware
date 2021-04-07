# This is the module which acts as main. It creates the GUI and performs the widget creation.
# These widgets then communicate with the associated Python module for the desired functionality.
# Created by Anand Samra on Oct. 14th

from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog

import os
import time
import database as db
import booksearch
import bookcheckout as bc
import bookreturn as br
import booklist as bk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk, Image


# Above are the necessary import statements

class Table:
    """ Class definition to create a table so it is neatly displayed on the tk
         window. Checks to see the data types of the item_list and appends the table initialization as required"""

    def __init__(self, window, item_list,start_row,start_column,size,direction):
        """ Instantiation method.
        PARAMETERS:
        window -- the current working window
        item_list -- the list of items which are to be displayed in table format
        start_row -- the row to start the table
        start_column -- the column to start the table
        w -- desired width of each entry in the table
        direction -- the direction which the table is to display
        """
        if isinstance(item_list[0],tuple):
            # Checking if its a list of tuples to create a two dimensional table

            total_rows = len(item_list)
            total_columns = len(item_list[0])
        # Getting dimensions of the required table

            for i in range(total_rows):
                for j in range(total_columns):
                    self.e = Entry(window,width = size)
                    self.e.grid(row=i+start_row, column=start_column+j)
                    self.e.insert(END, item_list[i][j])
                    self.e.config(state='readonly')
        # Loops through each item in the list, and appends it to the entry window and makes it so that they are read only.

        elif direction =="Horizontal":
            total_columns = len(item_list)
            for i in range(total_columns):
                self.e = Entry(window, width = size)
                self.e.grid(row=start_row, column=i+start_column)
                self.e.insert(END, item_list[i])
                self.e.config(state='readonly')

        elif direction =="Vertical":
            total_columns = len(item_list)
            for i in range(total_columns):
                self.e = Entry(window, width = size)
                self.e.grid(row=i+start_row, column=start_column)
                self.e.insert(END, item_list[i])
                self.e.config(state='readonly')


def create_button_bar():
    """ Creating buttons so that on start the user can select the functionality they want
        From here new windows will be created depending on what the functionality is."""

    wipe_window(window)
    # Used to reinitialize the options

    search_book_btn = Button(window, text="Search For A Book", command=create_book_search_window)
    search_book_btn.grid(column=1, row=2)
    display_books_graph_btn = Button(window, text="Display Popularity of Books As A Graph", command=create_display_books_as_graph_window)
    display_books_graph_btn.grid(column=2, row=2)
    display_books_table_btn = Button(window, text="Display Popularity of Books As A Table", command=create_display_books_as_table_window)
    display_books_table_btn.grid(column=3, row=2)
    check_out_book_btn = Button(window, text="Checkout Books", command=create_checkout_book_window)
    check_out_book_btn.grid(column=4, row=2)
    return_book_btn = Button(window, text="Return Books", command=create_return_book_window)
    return_book_btn.grid(column=5, row=2)
    # Above creates and displays the required buttons in their desired locations

    # Calling the functions to initialize the window and the required buttons
    books_img = ImageTk.PhotoImage(Image.open("Books.jpg"))

    books_img_label = Label(window,image=books_img)
    books_img_label.grid(row=3,column=0,columnspan=6)
    books_img_label.photo_ref= books_img
    # Creating a label which contains an image so the functionality looks nice.



def create_book_search_window():
    """ This creates a window for the user to search for a book
        There is a button to execute the search"""

    wipe_window(window)

    book_search_label = Label(window, text="Enter the book to search for", anchor = 'w')
    book_search_label.grid(row=0, column=0)
    # Creates and displays the label

    book_search_entry = Entry(window,width = 50)  # the "Entry" widget is for getting a user input.
    book_search_entry.grid(row=1, column=0,)
    book_search_entry.bind('<KeyRelease>',check_key)
    #Binding the entry to the required check_key function
    #This allows the combobox be filled with values which contain the string entered so far.

    book_search_button = Button(window, text="Search",
                                command=lambda: create_book_search_results(book_search_entry.get().lstrip(' ')))
    # Above calls the required function and strips any leading spaces
    book_search_button.grid(row=3, column=0)
    # Creates and displays the button in the desired location

    lb = Listbox(window, width =50)
    # Creating a list box to be associated with the entry widget. This contains the Titles matching the string so far.
    lb.grid(row=2, column = 0)
    lb.bind('<Double-Button-1>',selection_event)

    #Placing the combobox in the desired location
    empty_list = []
    #creating an empty list so that the listbox only updates values after a key has been entered

    update(empty_list,lb)
    # Calling the update function so that the combobox can be filled with relevant values




def create_book_search_results(title):
    """ Function to display the results of all the books which match the search book title query
    PARAMETERS:
    title -- the book title which is being queried"""

    wipe_window(window)
    # Wiping
    search_result = booksearch.search_for_book(title)
    # Getting the search results
    if isinstance(search_result,str):
        error_box = Text(window, height=1, width=51)
        error_box.insert(END, search_result)
        error_box.configure(state=DISABLED)
        error_box.grid(row=1, column=0)

    else:
        table = Table(window,search_result,1,0,45, "Horizontal")
        # Above instantiates the the table class to display the query results in a neat table format.

        header_list = ["Book ID", "ISBN", "Title", "Author", "Purchase Date","Rented By"]
         # Creates the header list

        header_table = Table(window, header_list,0,0,45,"Horizontal")
        # CODE REUSABILITY YAYYY
       # Above creates the header table to be displayed

    # IF else statement checks to see if any books were returned from the search query and displays the message if none are returned.

    home_button = Button(window, text="Home", command=create_button_bar)
    home_button.grid(row=len(search_result) + 1, column=0)

    try_again_button = Button(window, text="Try Again", command=create_book_search_window)
    try_again_button.grid(row=home_button.grid_info()['row'] + 1, column=0)
    # Creating the home and try again buttons. Places the try again button one row below the home button by accessing grid info


def create_display_books_as_graph_window():
    """ This creates a window to display the graph of getting the books
        By their popularity"""

    wipe_window(window)
    # Wiping the window
    results_figure,legend, _ = bk.display_books()
    #Gets the figure and the dictionary needed to create the legend, ignores the legend for displaying the table
    canvas = FigureCanvasTkAgg(results_figure, master=window)
    canvas.get_tk_widget().grid(row =0, column = 0, sticky="NSEW")
    #Creates a canvas and inserts the results_figure definied above into it

    for i in range (len(legend)):
        T = Text(window,height=2, width=35,wrap = WORD)
        T.grid(row=10+i, column = 0)
        T.insert(END,str(i)+" = " + str(legend.get(i)))
        T.configure(state='disabled')
        #Loops through the dictionary and displays a text widgets showing the key and its values

        home_button = Button(window, text="Home", command=create_button_bar)
        home_button.grid(row=len(legend)+10, column=0)
        # Creating the home button


def create_display_books_as_table_window():
    """ This creates a window which displays the popular books as a table rather than a graph
         This version will not show how many times that each book has been rented"""

    wipe_window(window)
    # Wiping the window
    _,_,table_legend = bk.display_books()
    legend = [legend_element[0] for legend_element in table_legend]
    # Getting only the book titles from the returned legend.

    #Getting the data back from the booklist module. Only the legend for tables is of concern here, so the _is used as the first placeholder
    legend_table = Table(window,legend,0,0,40,"Vertical")
    # Creating the legend table
    home_button = Button(window, text="Home", command=create_button_bar)
    home_button.grid(row=len(legend), column=0)


def create_checkout_book_window():
    """ This creates a window to for a user to checkout the book required"""

    wipe_window(window)
    # Wiping the window as required

    checkout_book_label = Label(window, text="Enter Book ID's (seperated by comma)", anchor='w')
    checkout_book_label.grid(row=0, column=0)
    member_ID_Label = Label(window, text = " Enter Member ID")
    member_ID_Label.grid(row = 0, column = 1)
    # Above creates the  labels for the necessary info to check out a book

    checkout_book_label_id = Entry(window)  # the "Entry" widget is for getting a user input.
    checkout_book_label_id.grid(row=1, column=0)
    member_ID_Label_entry = Entry(window)
    member_ID_Label_entry.grid(row = 1, column = 1)
    # Above creates the entry field windows required and displays them

    checkout_button = Button(window, text="Checkout", command =
    lambda: create_checkout_book_results(member_ID_Label_entry.get(),get_input_list(checkout_book_label_id)))
    # creates the button to checkout a book and uses the create checkout_book function defined below
    # Uses the get_input_list function to get a list of books to return

    checkout_button.grid(row = 2, column = 0)
    # Places the button in the desired location


def create_checkout_book_results(member_id, book_ids):
    """ Used to display the results of whether a list books was succesfully checked out
        or displays an error describing which books failed and why
        PARAMETERS:
        member_id --  member id of the person checking out the book
        book_ids -- list of ids for the books being checked out"""

    results_bc = []
    # creating an empty ist
    if member_id.isdigit() and len(member_id)==4:
        for i in range(len(book_ids)):
            book_id = book_ids[i].replace(" ","")
            # Removing spaces in case the user entered them in so the program works normally
            if book_id.isdigit():
                results_bc.insert(i,bc.checkout_book(member_id,book_id))
            else:
                results_bc.insert(i,"Invalid Book ID: "+ book_id)
    #Above loop goes over each element in the input of book_ids and appends them to the precreated list which stores the results

    else:
        results_bc.append("Error: Invalid Member ID")
    # This if else branch ensures the member ID is of valid form


    wipe_window(window)

    size = len(max(results_bc, key = len))
    # Getting the correct width of the table to create. It returns the length of the longest string found in the results_bc list
    result_table = Table(window,results_bc, 0,0, size, "Vertical")
    # Creating the results table

    home_button = Button(window, text="Home", command=create_button_bar)
    home_button.grid(row=len(book_ids), column=0)
    try_again_button = Button(window, text="Try Again", command=create_checkout_book_window)
    try_again_button.grid(row=home_button.grid_info()['row'] + 1, column=0)
    # Creating the home and try again buttons


def create_return_book_results(book_ids):
    """ Used to display the results of whether the books were succesfully returned
        PARAMETERS:
        book_ids -- list of ID's for the books being checked out"""

    results_br = []
    for i in range(len(book_ids)):
        book_id = book_ids[i].replace(" ", "")
        if book_id.isdigit():
            results_br.insert(i,br.return_book(book_id))
        else:
            results_br.insert(i,"Invalid Book ID: " + book_id)

    # Above loops through the list of input ID's adn attemps to return them. Appends the results to the results_br list
    # For display

    wipe_window(window)

    size = len(max(results_br,key = len))
    # Getting the correct width of the table to create. It returns the length of the longest string found in the results_br list

    book_return_table = Table(window, results_br,0,0, size, "Vertical")
    # Above Creates and displays a table which is read only showing the results of the action

    home_button = Button(window, text="Home", command = create_button_bar)
    home_button.grid(row = len(book_ids),column = 0)
    try_again_button = Button(window, text = "Try Again", command = create_return_book_window)
    try_again_button.grid(row = home_button.grid_info()['row']+ 1, column = 0)
    # Creating buttons to jump to different place in the program


def create_return_book_window():
    """ Used to create the return books window and get associated info and pass
        it to the return books module"""

    wipe_window(window)
    # Wiping the window as required

    return_book_label = Label(window, text="Enter Book ID's", anchor='w')
    return_book_label.grid(row=0, column=0)
    # Creating the label to let the user know what is expected

    return_book_label_id = Entry(window)  # the "Entry" widget is for getting a user input.
    return_book_label_id.grid(row=1, column=0)
    # Displaying the entry field in the desired location

    checkout_button = Button(window, text= "Return", command = lambda: create_return_book_results(get_input_list(return_book_label_id)))
    checkout_button.grid(row=2, column=0)
    # Creating and displaying the button to perform the book return
    # Uses the return_book function with the required arguments from the bookreturn module


def create_menu_bar():
    """ Creates the menubar"""
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=1)
    filemenu.add_command(label="Initialise DB", command=db.populate_database)
    # Intializes the database to contain the required files

    filemenu.add_command(label="New Action", command=create_button_bar)
    # This recreates the initial screen. So that a user can preform a new action

    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.destroy) # Quits the program

    menubar.add_cascade(label="File", menu=filemenu)

    window.config(menu=menubar)


def all_children (window):
    """ Used to get all the children of the window, so that they can be wiped as needed
        I want to create functionality in seperate windows, without overloading the user's sensitivity
        PARAMETERS:
           window -- the current window
        RETURNS:
            a list of all children"""
    children_list = window.winfo_children()

    for item in children_list:
        if item.winfo_children():
            children_list.extend(item.winfo_children())
    # Loops through and gets all children (widgets) of the window and adds them to a list

    return children_list


def wipe_window(window):
     """ Removes all elements from the window
     PARAMETERS:
     window -- the current working window
     """

     widget_list = all_children(window)
     for item in widget_list:
         item.grid_forget()
     # The above segement is used to wipe the window


def get_input_list(entry):
    """ Function which takes an entry widget as its parameter
        and gets the string associated with the entry and splits it into a list
        PARAMETERS:
        entry -- entry widget to retrive the list of inputs from
        RETURNS:
            list_of_book_ID's -- the list of book id's"""

    list_of_book_IDs = entry.get().split(",")
    # Getting the list of books id's and seperating them by comma
    return list_of_book_IDs


def check_key(event):
    """ Function used to handle an event change(key press) and updating the Entry Widget
        TO be used in conjuction with the search functionality
        PARAMETERS:
            event -- this is a key release that signifies a new key has been entered
            """
    input = event.widget.get()
    # getting the value which has been inserted to the Entry widget. the search entry widget has been binded to this function
    # so it is run whenever a new key(character) has been entered

    fill_values = db.get_titles()
    # Calls a function to get the titles from the database
    # These will act as the place holders in the combobox for autocomplete
    title_values = [i[0] for i in fill_values]
    # converting_the title values which is a list of tuples to just a list of strings

    if input == "":
        data = []
    # Checks if the entry is empty , if so does not display anything
    else:
        data = []
        for string in title_values:
            if input.lower() in string.lower():
                data.append(string)
    # Else statement sees that the input contains a character and loops through all default values and checks for a match
    # If a match occurs, it appends the matching title to the data list

    list_of_widgets = all_children(window)
    for widget in list_of_widgets:
        if isinstance(widget,Listbox):
            update(data,widget)
       # Calls the update function on the listbox found in the window.


def update(values,widget):
    """ Function which takes the values to be inserted to the given widget
        By specifying which widget is to be updated. Right now the only widget using autocomplete
        is a Combobox, but by factoring the code this way, it allows for more widgets to be added with
        slight modiciation to the code below
        PARAMETERS:
            values --  the list of values which are to be inserted to the widget
            widget -- the widget which is to be updated with the values"""

    # Removing all values from the listbox
    widget.delete(0,'end')

    for element in values:
        widget.insert('end', str(element)+"\n")
        # Adding the desired values into the widget so each entry is on a new line

def selection_event(event):
    """ Function used to perform search when a user double clicks on a value in the list box
         PARAMETERS:
             event -- event binded to a widget which calls this function"""
    selection = event.widget.get(ACTIVE)
    # Gets the line of text which has been double clicked by the user
    create_book_search_results(selection.rstrip())
    # Calling the function and removing the newline character





###############################
####------MAIN----------#######
###############################
window = Tk()
#This creates the window


create_menu_bar()
create_button_bar()


window.mainloop()
#This starts the loop for the window to keep it open and running






