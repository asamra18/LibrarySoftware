# This is the module which performs all the actions required on the database.
# Created by Anand Samra on Oct 14th


import subprocess  as sp
import os
import sqlite3
from sqlite3 import Error as e
from datetime import date



CurrentDB ="library.db" #default library database
global conn

def setDB (DB_Name):
    """ Changes the database as required. Likely not going to be needed
         Unless i Implement a functionality to change the library location(ie use a different database)
          PARAMETERS:
              DB_NAME -- the name of the database to connect to"""

    global CurrentDB 
    CurrentDB = DB_Name

#This function was only used to populate the database initially. Can be reused to reset the database values to what was submitted
#Used this to ensure proper testing


def populate_database():
    """ Populate the Database and the associated values with the txt files
       This function was only used to populate the database initially. Can be reused to reset the database values to what was submitted
        Used this to ensure proper testing"""
    conn = None
    try:
        conn = sqlite3.connect(CurrentDB)
    except Error as e:
        print(e)

    # Above creates the connect to the sql database as required

    c = conn.cursor()
    sql_Create_Book_Info_table =  """CREATE TABLE IF NOT EXISTS Book_Info( book_id INTEGER PRIMARY KEY UNIQUE ,
                                      ISBN INTEGER NOT NULL,
                                      title TEXT NOT NULL,
                                      author TEXT NOT NULL,
                                      purchase_date TEXT NOT NULL,
                                      rented_by INTEGER NOT NULL);"""
    sql_Create_Loan_History_Table  =  """CREATE TABLE IF NOT EXISTS Loan_Info( transaction_id INTEGER PRIMARY KEY UNIQUE,
                                          book_id NOT NULL,
                                          checkout_date TEXT NOT NULL,
                                          return_date TEXT,
                                          member_id INTEGER NOT NULL);"""


    """  Above lines are the sql statements required to create the tables if they do not already exist in the data base
         This is helplful as it allows the database to already contain the tables. The only way for a book to be added, or an existing book
          to be removed is by manually changing the txt file"""

    try:
        c.execute(sql_Create_Book_Info_table)
        c.execute(sql_Create_Loan_History_Table)

    except Error as e:
        print(e)
    # Above try except blocks are used to execute the sql create table statements described above

    with open("Book_Info.txt") as book_info:
        for line in book_info:
            current_line = line.split(',')
            sqlite3_insert_statement =""" INSERT OR IGNORE INTO Book_Info(book_id,ISBN,title,author,purchase_date,rented_by)
                                                VALUES (?,?,?,?,?,?)"""
            try:
                c.execute(sqlite3_insert_statement, current_line)
                conn.commit()
            except Error as e:
                print(e)

    # Above loop opens the book info txt file and uploads the information to the Book_Info table in the library database
    # Ignore is used to ignore the information which is already stored in the table

    with open("Loan_History.txt") as loan_info:
        for line in loan_info:
            current_line = line.split(',')
            sqlite3_insert_loan_statement =""" INSERT OR IGNORE INTO Loan_Info (transaction_id,book_id,checkout_date, return_date, member_id)
                                                VALUES (?,?,?,?,?)"""
            try:
                c.execute(sqlite3_insert_loan_statement, current_line)
                conn.commit()
            except Error as e:
                print(e)
    # Above loop opens the loan history txt file and uploads the information to the Loan_Info table in the library database
    # Ignore is used to ignore the information which is already stored in the table


    c.close()
    conn.close()
    #Delete teh cursor and close teh connection


def search_for_book_sql(book_title):
    """ This searches for the book. It inputs the title to a sql statement and executes the query
         PARAMETERS:
         book_title -- the title of the book to query
         RETURNS:
             The books matching the book title or an error message saying nothing was found"""


    try:
        conn = sqlite3.connect(CurrentDB)
        c = conn.cursor()  # gets a cursor for the database

        c.execute(" SELECT DISTINCT * FROM Book_Info where title LIKE UPPER (" + "'%" + "%s" % book_title + "%');")


    except Error as e:
        print(e)
    results = c.fetchall()
        # Above attempts to open a connection to the database and query it for the book title.
        # And saves the books to the resutls variables

    c.close()
    conn.close()
    #Delete the cursor and close the connection


    if len(results) ==0:
        return "No books match the query"
    else:
        return results


    # returns the results so that the booksearch.py module can use the information as required
    # Returns an error message if no book matches the search query


def checkout_book_sql(member_id, book_id):
    """ Function used to perform the sql actions required to checkout a book. Returns associated error messages(as strings) if there are issues
        PARAMETERS:
        member_id -- String associated with the member ID
        book_id -- string associated with the book_id
        RETURNS:
            Message saying the book was properly checked out or an associated error message"""


    sql_select_statement = "Select rented_by FROM Book_Info where book_id = " + book_id
    #sql_check_statement = "SELECT * FROM Members where member_id = " + member_id

    # two sql statements to ensure that the book and member id are valid and found in the database
    try:
        conn = sqlite3.connect(CurrentDB)
        c = conn.cursor()  # gets a cursor for the database
        c.execute(sql_select_statement)


    except Error as e:
        print(e)
    # Above try block gets data from the database to check if there is someone who currently has the book on loan

    results = c.fetchone()

    # This fetches the first row of the cursor. There should only be one as the book id is to be unique.

    if results is None:
        return("Error: No Book ID = " + book_id)
    # Ensures that there is a return on the sql statement
    else:
        results = results[0]
    # this accesses the tuple from the results tuple and saves it as its singular value.
    # 0 if the book is available, or the member id of who has rented it.
        if results != 0:
            return ("Error: Book "+book_id+" is currently rented")
        else:
            try:
                update_query_book_info_bc = " UPDATE Book_Info SET rented_by = " + member_id + " where book_id = " + book_id

                update_query_loan_history_bc = "INSERT INTO Loan_Info(book_id, checkout_date, member_id) VALUES (?,?,?)"
                #Above lines create template sql strings for the update queries as required

                checkout_date = date.today().strftime('%d/%m/%Y')
                #GEtting the date so that the loan history table is properly updated. and formatting it to match the values already in the DB
                insert_loan_history_tuple = (int(book_id), str(checkout_date), int(member_id))
                # creates a tuple of values so that the sql uupdate properly runs. It casts the variables to the required types.


                c.execute(update_query_book_info_bc)
                conn.commit()

                # Updates the book info table
                c.execute(update_query_loan_history_bc, insert_loan_history_tuple)
                conn.commit()
                # Updates the loan history table as required. Not putting a return date as that will be handled by the book return module

            except Error as e:
                return("Error when updating info records")
            # Should not get here
        c.close()

        conn.close()

    return("Book " +book_id+" succesfully checked out")


def return_book_sql(book_id):
    """ Function used to perform the sql actions required to return a book. Returns associated error messages(as strings) if there are issues
            PARAMETERS:
            book_id -- string associated with the book_id
            RETURNS:
                A message saying if the book was succesfully returned or an associated error message"""
    sql_select_statement_br = "Select rented_by FROM Book_Info where book_id = " + book_id
    # Getting the member id of the person who rented the book so records can be properly updated.
    try:
        conn = sqlite3.connect(CurrentDB)
        c = conn.cursor()  # gets a cursor for the database

        c.execute(sql_select_statement_br)

    except Error as e:
        print(e)
        # Attempting to open a connection to the DB and execute the sql query defined above
        # SHould not get an error

    member_id = c.fetchone()


    if member_id is None:
        return("No book associated with ID: "+book_id)
         # Checking if there is actually a book associated with that ID
    else:
        member_id = member_id[0]
        member_id = str(member_id)
        # getting the true member id from the tuple returned by the fetchone call

        if member_id=="0":
            return("Error: Book "+book_id+" currently not on loan")
        # Returning the error message associated with attempting to return a not on loan book
        else:
            try:
                update_query_book_info_br = " UPDATE Book_Info SET rented_by = 0 "+" where book_id = " + book_id

                update_query_loan_history_br = "UPDATE Loan_Info SET return_date = (?) WHERE book_id =" + book_id + " AND member_id = " + member_id+ " AND return_date IS NULL"
                # This query ensures that the correct loan transaction is acquired as someone can rent the same book twice
                # Above lines create template sql strings for the update queries as required

                return_date = date.today().strftime('%d/%m/%Y')
                #Getting the date so that the loan history table is properly updated. and formatting it to match the values already in the DB
                insert_loan_history_value = (str(return_date),)
                # creates a tuple of values so that the sql uupdate properly runs. It casts the variables to the required types.


                c.execute(update_query_book_info_br)
                conn.commit()

                # Updates the book info table
                c.execute(update_query_loan_history_br, insert_loan_history_value)
                conn.commit()
                # Updates the loan history table as required. Not putting a return date as that will be handled by the book return module


            except Error as e:
                return("Error when updating info records")
            # SHOuld not get here

            c.close()
            conn.close()

    return ("Book " + book_id+ " succesfully returned")


def display_books_sql():
    """ This gets all books in the library database
         and used a dictionary to associated the name to a value which represents the number of loans it has had so far
         RETURNS:
             A list of all books which have been rented at least once and how many times they have been rented
    """
    sql_drop_view_statement = """DROP VIEW IF EXISTS [display_table]"""
    # sql_statement to drop the view first so that it can be recreated with updated values as books will be consistently checked out and returned

    sql_create_view_statement = """ CREATE VIEW [display_table] AS SELECT *  FROM Loan_Info JOIN Book_Info ON Book_Info.book_id = Loan_Info.book_id;"""
    # Above is a sqlstatement used to join the Book_info and Loan_info table
    # This results in a temp table which only has the books which have been rented
    # A book will only appear in this table if a record exists showing it has been rented
    # This table will be useful as we now count how many times a distinct book title has appeared in this view

    sql_select_from_view_statement = """ SELECT title, count(*)  FROM display_table GROUP BY title;"""
    # This is a template statment to return the the book title with how many times it has been rented out from the library
    # This uses the temporary table(VIEW) created from the second sql statement described above

    try:
        conn = sqlite3.connect(CurrentDB)
        c = conn.cursor()  # gets a cursor for the database
        c.execute(sql_drop_view_statement)
        c.execute(sql_create_view_statement)
        c.execute(sql_select_from_view_statement)
        results = c.fetchall()
    except Error as e:
        print(e)
        # should not get here

    # The above try - except blocks executes the required sql queries and save the results to a variabled named "results"
    # results variable is a list of tuples where the first element in the tuple is the title of a book
    # and the second element is the number of times it has been rented
    c.close()
    conn.close()

    return results
   # returing the results list


def sql_get_purchase_date(book_title):
    """ Function to return the purchase dates of the given book title
        PARAMETERS:
        book_title -- the book title to find the purchase date of
        RETURNS:
            results -- a string associated with the purchase date of the title"""

    try:
        conn = sqlite3.connect(CurrentDB)
        c = conn.cursor()  # gets a cursor for the database

        c.execute(" SELECT purchase_date FROM Book_Info where title LIKE UPPER (" + "'%" + "%s" % book_title + "%');")

        results = c.fetchall()
    except Error as e:
        print(e)
        #Should not get here

    # Above attempts to connect to the database and saves the results of the query to the results variable
    c.close()
    conn.close()
    # Closing cursor and connection

    return results

def get_titles():
    """ Function used to allow autocomplete to work with the combobox in the Menu module
        RETURNS: results -- a list containing all book titles in the databse"""
    sql_select_statement = """ SELECT DISTINCT title from Book_Info;"""
    try:
        conn = sqlite3.connect(CurrentDB)
        c = conn.cursor()  # gets a cursor for the database
        c.execute(sql_select_statement)
        results = c.fetchall()
    except Error as e:
        print(e)
        # Should not get here

        # Above attempts to connect to the database and saves the results of the query to the results variable
    c.close()
    conn.close()
    return results




if __name__=='__main__':
    #######testing###############

    # Used to ensure that the tables were intialized properly. The other database functions were checked in conjunction
    # With their associated .py module.
    try:
        conn = sqlite3.connect(CurrentDB)
        c = conn.cursor()  # gets a cursor for the database

        c.execute("SELECT * FROM Book_Info;")
        results = c.fetchall()
        print(results)

        c.execute("Select rented_by FROM Book_Info where book_id = 1;")
        results = c.fetchall()
        print(results)

        c.execute("SELECT DISTINCT * FROM Book_Info where title LIKE UPPER ('%Harry%');")
        results = c.fetchall()
        print(results)
    except Error as e:
        print(e)



