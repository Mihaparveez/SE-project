import streamlit as st
from back import add_book, get_books, get_book_by_id, get_books_by_name, get_books_by_author, delete_book, update_book

def main():
    st.title("Library")

    # Create a sidebar menu with different operations
    menu_option = st.sidebar.selectbox("Select Operation", ["Display Books", "Add Book", "Update Book", "Delete Book", "Get Book by ID", "Get Books by Name", "Get Books by author"])

    if menu_option == "Add Book":
        # Get book information from user input
        book_name = st.text_input("Book Name:")
        book_id = st.text_input("Book ID:")
        author = st.text_input("author:")

        # Add book to the database when the user clicks the button
        if st.button("Add Book"):
            add_book(book_name, book_id, author)
            st.success("Book added successfully!")

    elif menu_option == "Display Books":
        # Display books
        st.title("Book List")
        books = get_books()

        if books:
            for book in books:
                st.write(f"Book ID: {book[0]}, Book Name: {book[1]}, author: {book[2]}")
        else:
            st.write("No books available.")

    elif menu_option == "Update Book":
        # Update book
        st.title("Update Book")
        book_id_to_update = st.text_input("Enter Book ID to update:")
        new_book_name = st.text_input("Enter new Book Name:")
        new_author = st.text_input("Enter new author:")
        if st.button("Update Book"):
            update_book(book_id_to_update, new_book_name, new_author)
            st.success("Book updated successfully!")

    elif menu_option == "Delete Book":
        # Delete book
        st.title("Delete Book")
        book_id_to_delete = st.text_input("Enter Book ID to delete:")
        if st.button("Delete Book"):
            delete_book(book_id_to_delete)
            st.success("Book deleted successfully!")

    elif menu_option == "Get Book by ID":
        # Get book by ID
        st.title("Get Book by ID")
        book_id_to_get = st.text_input("Enter Book ID to get:")
        if st.button("Get Book by ID"):
            book = get_book_by_id(book_id_to_get)
            if book:
                st.write(f"Book ID: {book[0]}, Book Name: {book[1]}, author: {book[2]}")
            else:
                st.write("Book not found.")

    elif menu_option == "Get Books by Name":
        # Get books by name
        st.title("Get Books by Name")
        book_name_to_get = st.text_input("Enter Book Name to get:")
        if st.button("Get Books by Name"):
            books_by_name = get_books_by_name(book_name_to_get)
            if books_by_name:
                for book in books_by_name:
                    st.write(f"Book ID: {book[0]}, Book Name: {book[1]}, author: {book[2]}")
            else:
                st.write("No books found with the given name.")

    elif menu_option == "Get Books by author":
        # Get books by author
        st.title("Get Books by author")
        author_to_get = st.text_input("Enter author to get:")
        if st.button("Get Books by author"):
            books_by_author = get_books_by_author(author_to_get)
            if books_by_author:
                for book in books_by_author:
                    st.write(f"Book ID: {book[0]}, Book Name: {book[1]}, author: {book[2]}")
            else:
                st.write("No books found with the given author.")

if __name__ == "__main__":
    main()
