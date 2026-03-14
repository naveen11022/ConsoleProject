import json

FILE = "books.json"


class Book:
    # _instance = None
    #
    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(Book, cls).__new__(cls)
    #
    #     return cls._instance

    def __init__(self, bookid, name, ISBN, authorname,DOP,quantity):
        self.bookid = bookid
        self.name = name
        self.ISBN = ISBN
        self.authorname = authorname
        self.DOP = DOP
        self.quantity = quantity

    def add_book(self):
        with open(FILE, "r") as file:
            book_structure = {
                "bookid": self.bookid,
                "name": self.name,
                "ISBN": self.ISBN,
                "authorname": self.authorname,
                "DOP": self.DOP,
                "quantity": self.quantity
            }
            data = json.load(file)
            print(data.append(book_structure))

    def remove_book(self,book_id):
        with open(FILE, "r") as file:
            books = json.load(file)

            for book in books:
                if book["bookid"] == book_id:
                    books.remove(book)
                    with open(FILE, "w") as file:
                        json.dump(books, file)

