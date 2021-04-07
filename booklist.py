# Module used to perform backend actions to display books by popularity
# Created by Anand Samra on Oct.19th

import database as db
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import operator


class Book:
    """ Class used to define what a book is. This class is imported into other modules as needed
        Only  a setter method for the rented_by statement so that the database can be updated as required
        Changing other things can have negative consequences as these values should be set in stone.
        This class is mainly used for testing purposes as the database can be updated directly with SQL statements
        PARAMETERS
        book_id -- the id of the book
        ISBN -- the ISBN number
        title --  the title of the book
        author -- the author
        purchase date -- date the book was purchased
        rented_by -- the member id of the person who has borrowed the book
    """
    def __init__(self, book_id, ISBN, title, author, purchase_date, rented_by):
        """ Instantiation method to assign the fields to the corresponding values"""
        self.__book_id = book_id
        self.__ISBN = ISBN
        self.__title = title
        self.__author = author
        self.__purchase_date = purchase_date
        self.__rented_by = rented_by

    def get_book_id(self):
        """ Getter method to return the book id
        RETURNS: the book ID
            """
        return self.__book_id
    def get_ISBN(self):
        """ Getter method to return the ISBN
         RETURNS: the book ISBN number"""
        return self.__ISBN

    def get_title(self):
        """ Getter method to get the book title
        RETURNS: the book title"""
        return self.__title

    def get_author(self):
        """ Getter method to return the author
         RETURN: the book author"""
        return self.__author

    def get_purchase_date(self):
        """ Getter method to return the date the book was purchased
        RETURNS: the purchase date"""
        return self.__purchase_date

    def get_rented_by(self):
        """ Getter method to return the id of the member who has rented the book
        RETURNS: who is renting the book"""
        return self.__rented_by


def display_books():
    """ Function used to communicate with the database to return a dictionary of book
         Mapping their name to the number of loans they have had
         RETURNS:
              a figure which holds the graph of books vs their popularity
              the legend for this figure
              and a legend which is sorted for use as a table"""

    values = db.display_books_sql()

    values.sort(reverse=True,key=lambda x: x[1])
    # Getting the tuple from the database function which returns the books which have been rented at least once and sorting them
    # From highest to lowest
   

    books = [i[0] for i in values]
    #Creates a list which contains the book names


    numbers = [i[1] for i in values]
    numbers = np.array(numbers)
    # Creates a list which contains the number of times each book has been rented
    # The values are joined. numbers[0] is how many times books[0] has been rented
    # And converts it to a np array for array division

    books_ages = []
    # Creating a list to contain the age of the associated book titles

    current_date = date.today()
    # Getting the current date
    current_year = current_date.year
    # Getting the current year

    for book in books:
        full_purchase_dates = db.sql_get_purchase_date(book)
        # Getting the dates associated with a specific book title

        years = list(sum(full_purchase_dates,()))
        # Converts the list of tuples(full_purchase_dates) to a regular list to calculate
        # the middle year it was purchased in can be determined

        mid_year = 0;
        # Creating a temp variable to store the avg year of when a book was purchased
        for value in years:
            year = int(value[-4:])
            # Getting the last 4 characters from the string associated with the purchase date
            # And converting
            mid_year = mid_year + year
            # Adding the year to the average year
        mid_year = int(mid_year/len(years))
        # This computes the middle year of when a book was purchased
        # Casts it to an int so that no decimals occur
        age = current_year-mid_year
        if age == 0:
            age = 1
        # Calculates how old a book is and assigns it a value of 1 if the book was purchased this year

        books_ages.append(age)

    # Above loop goes through every book which has been rented, gets the associated
    # Purchase dates. Then It goes through every purchase date for that book and computes
    # The average year it was purchased and appends it to the purchase years list
    # The purchase years list will be arranged in the same order as the books list
    # the first element in purchase years is the middle year when the first book of
    # the books list was purchased, etc, etc

    popularity_score = numbers/books_ages
    # Creating a NP array to store the popularity scores through NP array division
    # Popularity score is the number of times a book is rented divided by
    # How long ago it was purchased

    x_plots = np.arange(len(books))
    #Creating a lin space to make the graph look neater

    figure = plt.figure()
    g = figure.add_subplot(111)
    g.set_ylabel("Popularity Score")
    g.bar(x_plots,popularity_score,color=['r','g','b', 'c', 'm', 'y'])
    #Creates a figure and adds a subplot to it. And color codes the graph

    
    legend_graph = {x_plots[i]: books[i] for i in range(len(books))}
    #Creates a dictionary which is to be used as the legend for the graph in the menu.py module

    legend_table ={books[i]: popularity_score[i] for i in range(len(popularity_score))}
    # Creating the dictionary which is to be used for the display as table functionality
    sorted_legend_table = sorted(legend_table.items(), key=operator.itemgetter(1),reverse=True)
    # Sorting the legend table

    return figure,legend_graph,sorted_legend_table

if __name__=='__main__':
    #######testing###############

    # Only showing the resulting figure and legend from the test books defined in the menu module
    testbook1 = Book(99, 1111111111111, "TestBook1", "Anand Samra", "21/10/2020", 1)
    testbook2 = Book(100, 1114443339991, "TestBook2", "Anand Samra", "21/10/2020", 0)
    testbook3 = Book(101, 1111111111111, "TestBook1", "Anand Samra", "21/10/2015", 1)
    # Creating test book objects for manual inspection if the algorithm works
    # testbook1 and testbook3 are to represent the same book purchased on different dates

    testbook1_times_rented=2
    testbook2_times_rented=3
    testbook3_times_rented=10

    book1_age = int(2020 - ((2020+2015)/2))
    print(book1_age)
    # this represents the age of when testbook1 and testbook2 which are the same book, purchased on different dates
    book2_age = 1

    book1_score = (testbook3_times_rented+testbook1_times_rented)/book1_age
    book2_score = testbook2_times_rented/book2_age
    # Gettting the scores for each book
    print(book1_score)
    print(book2_score)

    test_values = [(testbook1.get_title(),book1_score ),(testbook2.get_title(),book2_score)]

    test_values.sort(reverse=True,key=lambda x: x[1])
    test_books = [i[0] for i in test_values]
    numbers = [i[1] for i in test_values]
    x_plots = np.arange(len(test_books))

    figure = plt.figure()
    g = figure.add_subplot(111)
    g.bar(x_plots, numbers, color=['r', 'g', 'b', 'c', 'm', 'y'])
    figure.show()

    legend = {x_plots[i]: test_books[i] for i in range(len(test_books))}
    print(legend)
    # After Inspection I see that it works. And that the algorithm works as expected


