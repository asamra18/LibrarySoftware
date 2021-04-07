# This is the book search module. Created by Anand Samra on Oct.14th
# Used to perform and define the book search functionality.

import database as db
import unittest


def search_for_book(book_title):
    """ This searches for the book. It inputs the value read from the search
         for book field and uses the SQL template found in the database.py module
         Returns the specified books back to the menu module
         KEYWORD:
         book_title -- search term that is being queried from the DB
         RETURNS:
             results --  a list of books """

    results = db.search_for_book_sql(book_title)
    # Calls the database function associated with searching for a book and
    # saves the values to a variable named books

    return results


class Test_Method(unittest.TestCase):
    """ UNIT TESTING CLASS"""

    def test(self):
        book_validity = [(4, 9780553381702, 'A Storm of Swords', 'George R.R Martin', '15/05/2011', 0)]
        book_validity_2 = [(1, 9781644732083,  'Harry Potter and the Chamber of Secrets',
                            'J K Rowling', '01/01/2015', 0),(2, 9781644732083,  'Harry Potter and the Chamber of Secrets',
                            'J K Rowling', '01/08/2015', 0)]
        # Test list of tuples tuple to see if book search works properly

        self.assertEqual(search_for_book("Storm"),book_validity)
        self.assertEqual(search_for_book("Chamber"),book_validity_2)
        self.assertEqual(search_for_book("BOB"),"No books match the query")

if __name__=='__main__':
    #######testing###############
    unittest.main()









