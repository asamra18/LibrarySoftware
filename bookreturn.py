# Module which performs the communication required between the menu and the database
# Created by Anand Samra on Oct 15th

import database as db
from booklist import Book
import bookcheckout
import unittest

def return_book(book_id):
    """ Attempts to return the book associated with book_id
        or returns and displays the correct error message
        PARAMTERS:
        book_id -- The string associated with the book to return
        RETURNS: the associated message of whether a book was rented out succesfully
        """
    if book_id is None:
        return
    results = db.return_book_sql(book_id)
    # Calling the associated database actions and saving it to the results variable
    return results


class Test_Method(unittest.TestCase):
    """" UNIT TESTING CLASS"""
    def test(self):
        self.assertEqual(return_book("6"),"Error: Book 6 currently not on loan")
        self.assertEqual(return_book("10000"),"No book associated with ID: 10000")
        bookcheckout.checkout_book("1007","1")
        self.assertEqual(return_book("1"),"Book 1 succesfully returned")




if __name__ == '__main__':
    #######testing###############
    unittest.main()




