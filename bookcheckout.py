# Module used for checking out a book.
# Created by Anand Samra on OCt 17th


import database as db
import unittest


def checkout_book(member_id, book_id):
    """ This function is used to checkout the book
        Using the strings associated with the member id and book id
        passes the arguments to the database module to perform the SQL actions
        PARAMETERS:
        member_id -- the string associated with the member id
        book_id -- the string associated with the book_id """
    results = db.checkout_book_sql(member_id,book_id)
    return results


class Test_Method(unittest.TestCase):
    """ UNIT TESTING CLASS"""
    def test(self):
        checkout_book("1007","1")
        self.assertEqual(checkout_book("1006","1"),"Error: Book 1 is currently rented")
        self.assertEqual(checkout_book("1000","100"),"Error: No Book ID = 100")
        self.assertEqual(checkout_book("1001","2"),"Book 2 succesfully checked out")


if __name__=='__main__':
    #######testing###############
    unittest.main()





