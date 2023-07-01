def input_valid(msg, start=0, end=None):
    while True:
        inp = input(msg)
        if not inp.isdecimal():
            print('Error: Please enter a valid integer!')
            continue
        elif start is not None and end is not None:
            if not (start <= int(inp) <= end):
                print('Error : Invalid range. Try again!')
                continue
        return int(inp)


class Book:
    def __init__(self, book_name, book_id, book_quantity):
        self.book_id, self.book_name, self.total_quantity = book_id, book_name, book_quantity
        self.total_borrowed = 0

    def borrow(self):
        if self.total_quantity - self.total_borrowed == 0:
            return False
        self.total_borrowed += 1
        return True

    def return_copy(self):
        assert self.total_borrowed > 0
        self.total_borrowed -= 1

    def __str__(self):
        return f'Book Name : {self.book_name:20} -ID : {self.book_id:<5}   -Total Quantity : {self.total_quantity:<6}' \
               f'-Total borrowed : {self.total_borrowed}'


class User:
    def __init__(self, user_name, user_id):
        self.user_name, self.user_id = user_name, user_id
        self.borrowed_books = []

    def borrow(self, book):
        self.borrowed_books.append(book)

    def is_borrowed(self, book):
        for borrowed_books in self.borrowed_books:
            if borrowed_books.book_id == book.book_id:
                return True
        return False

    def return_book(self, book):
        for idx, mybook in enumerate(self.borrowed_books):
            if mybook.book_id == book.book_id:
                del self.borrowed_books[idx]
                break

    def simple_repr(self, is_detailed=False):
        ret = f'User Name : {self.user_name:20} -Id : {self.user_id}'
        if is_detailed and self.borrowed_books:
            ret += '\nBorrowed books : \n'
            for book in self.borrowed_books:
                ret += f'\t{str(book)}\n'
        return ret

    def __repr__(self):
        return self.simple_repr(True)


class Backend:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book_name, book_id, book_quantity):
        if self.get_book_by_id(book_id):
            self.books.append(Book(book_name, book_id, book_quantity))
        else:
            return "Error : Book with same Name or ID is already in the system!"

    def print_library_books(self):
        return [str(book) for book in self.books]

    def search_book_with_prefix(self, prefix):
        return [book for book in self.books if book.book_name.startswith(prefix)]

    def add_user(self, user_name, user_id):
        if self.check_user_id(user_id):
            self.users.append(User(user_name, user_id))
        else:
            return 'Error : User With Same ID Found!'

    def get_user_by_name(self, user_name):
        for user in self.users:
            if user_name == user.user_name:
                return user
        return None

    def get_book_by_name(self, book_name):
        for book in self.books:
            if book.book_name == book_name:
                return book
        return None

    def borrow_book(self, user_name, book_name):
        user = self.get_user_by_name(user_name)
        book = self.get_book_by_name(book_name)

        if user is None or book is None:
            return False
        if book.borrow():
            user.borrow(book)
            return True
        return False

    def return_book(self, user_name, book_name):
        user = self.get_user_by_name(user_name)
        book = self.get_book_by_name(book_name)

        if user is None or book is None:
            return

        if user.is_borrowed(book):
            book.return_copy()
            user.return_book(book)

        else:
            print("This user didn't borrow this book !")

    def get_users_borrowed_book(self, book_name):
        book = self.get_book_by_name(book_name)

        if book is None:
            return []

        return [user for user in self.users if user.is_borrowed(book)]

    def get_users(self):
        for user in self.users:
            print(user)
            for book in user.borrowed_books:
                print(book)

    # book ID is unique
    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return False
        return True

    # user ID is unique
    def check_user_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return False
        return True


class Frontend:
    def __init__(self):
        self.backend_manager = Backend()
        self.add_dummy_data()

    # :: :: Done :: ::
    def print_menu(self):
        print('Program Options:')

        messages = [
            'Add book',
            'Print library books',
            'Print books by prefix',
            'Add user',
            'Borrow book',
            'Return book',
            'Print users borrowed book',
            'Print users',
            'Exit the program'
        ]

        messages = [f'{idx + 1}) {item}' for idx, item in enumerate(messages)]
        print('\n'.join(messages))
        msg = f'-Enter your choice from (1 to {len(messages)} ) : '
        return input_valid(msg, 1, len(messages))

    # :: :: Done :: ::
    def add_dummy_data(self):
        self.backend_manager.add_user('Mostafa', 112)
        self.backend_manager.add_user('Ahmed', 32)
        self.backend_manager.add_user('Khaled', 2)

        self.backend_manager.add_book('Test1', 9921, 12)
        self.backend_manager.add_book('Test2', 42231, 2)
        self.backend_manager.add_book('Test3', 122, 333)

    # :: :: Done :: ::
    def run(self):

        while True:

            choice = self.print_menu()

            print()

            # 'Add book'
            if choice == 1:
                self.add_book()
            # 'Print library books' ::::: Done ::::::::
            elif choice == 2:
                self.print_books()
            # 'Print books by prefix'  ::::: Done ::::::::
            elif choice == 3:
                self.search_book_prefix()
            # 'Add user'
            elif choice == 4:
                self.add_user()
            # 'Borrow book'
            elif choice == 5:
                self.borrow_book()
            # 'Return book'
            elif choice == 6:
                self.return_book()
            # 'Print users borrowed book'
            elif choice == 7:
                self.print_users_borrowed_book()
            # 'Print users'
            elif choice == 8:
                self.print_users()
            else:
                print("... Exiting the Program ...")
                break

    def add_book(self):
        print('Enter book Info : ')

        book_name = input('Book Name :')
        book_id = int(input('Book ID : '))
        total_quantity = int(input('Total quantity :'))
        print(self.backend_manager.add_book(book_name, book_id, total_quantity))

    def print_books(self):
        for book in self.backend_manager.print_library_books():
            print(book)

    def search_book_prefix(self):
        prefix = input('Book name : ')
        matches = self.backend_manager.search_book_with_prefix(prefix)
        if len(matches) > 0:
            for book in matches:
                print(book)
        else:
            print('No Match Found')

    def add_user(self):
        print('Enter User Info : ')
        user_name = input('User Name : ')
        user_id = int(input('User Id : '))
        print(self.backend_manager.add_user(user_name, user_id))

    def read_user_name_and_book_name(self, trails=3):
        trails += 1
        while trails > 0:
            trails -= 1
            print('Enter User Name and Book Name: ')
            # Modify it to id later
            user_name = input('User Name : ')
            if self.backend_manager.get_user_by_name(user_name) is None:
                print('Invalid User Name!')
                continue
            book_name = input('Book Name : ')
            if self.backend_manager.get_book_by_name(book_name) is None:
                print('Invalid book name!')
                continue
            return user_name, book_name
        print('you did several trails! Try later..')
        return None, None, None

    def borrow_book(self):

        user_name, book_name = self.read_user_name_and_book_name()

        if user_name is None or book_name is None:
            return
        if not self.backend_manager.borrow_book(user_name, book_name):
            print('Failed to borrow the book!')

    def return_book(self):

        user_name, book_name = self.read_user_name_and_book_name()

        if user_name is None or book_name is None:
            return
        self.backend_manager.return_book(user_name, book_name)

    def print_users_borrowed_book(self):
        book_name = input('Book Name : ')
        if self.backend_manager.get_book_by_name(book_name) is None:
            print('Invalid book name!')
        else:
            user_lst = self.backend_manager.get_users_borrowed_book(book_name)

            if not user_lst:
                print('\nNo one borrowed this book')
            else:
                print('\nList of users borrowed this book ')
                for user in user_lst:
                    print(user.simple_repr())

    def print_users(self):
        user_list = '\n'.join([str(user) for user in self.backend_manager.users])
        print(user_list)


if __name__ == '__main__':
    app = Frontend()
    app.run()
