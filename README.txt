The library.db file is submitted to match exactly how the submitted txt files are. Once code is being tested, the db will update. Initially no books are on loan.  

booksearch.py: Returns all books if no string provided. Also has an autocomplete functionality. The user must double click the title they are interested in. Otherwise if they press search,
               It will search uisng the input they provided. Not from the list which pops up. 


booklist.py This module returns the books as either a graph, or a list sorted in Descending order based on their popularity. I am happy with how I implemented this because it
             only returns books that have been rented at least once. 
             I am also happy that I implemented the user to see the results as either a graph, or a list(table) as seeing both versions can be helpful. The graph displayed
             plots the books versus their popularity score and uses an algorithm of my own design.  The algorithm finds the
             number of times a book has been rented, and divides it by how long ago the book was purchased (in years). This says the popularity of a book bought in 2010 and rented once,
             would be 1/10. 
             The table version displays a little less information as it only displays the books from highest to lowest sorted by their popularity. Using the same algorithm as above. 


bookreturn.py and bookcheckout.py These modules allow the user to enter multiple Book ID's seperated by a comma
       

I was able to define my own functions so that the same window is used, so that lots of pop ups are not overloading the user. I am also happy with how i segmented the code, and ensured that 
it is reusable if other functionality were to be implemented which can be used in part with already defined modules. 

I am particularily happy with the Table class i created. It was quite hard to debugg the initial issues, but the type checks should be able to allow a table
to be created from either just a list of elements, or a list of tuples.
I also wrote unittests when possible, or I used the command line to display individual elements and ensure the functions worked as expected. I am also quite happy with how i was able to use 
views and ensure that the view updates as the other tables are updated.  

I am incredibly proud of my autocomplete functionality. It took me hours to get, and lots of debugging to understand how widgets and call backs work. But I am quite proud of what
I accomplished. 


When running the individual modules for the UNIT TESTS. PLEASE ENSURE TO RE INITIALIZE THE DB TO MATCH THE TXT FILES. OTHERWISE THE SQL DATABASE WILL BE CHANGED AND THE TEST CAN FAIL
IF THE DATABASE IS UPDATED.  
IT NEEDS TO BE REINITIALIZED BEFORE EVERY TEST (TEST bookreturn, re initialize the DB by dropping the tables manually, then intializing them from the file bar, then test bookcheckout, etc)


