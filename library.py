import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

def add_book():

    for widget in frame_add_search_up_del.winfo_children():
            widget.destroy()


    def add():
        
        try:
            title = title_ent.get().strip()
            author = author_ent.get().strip()
            year_pub = y_p_ent.get().strip()
            number_copies = n_p_ent.get().strip()

            if not title or not author or not year_pub or not number_copies:
                messagebox.showerror('Adding Error', "All fields must be filled!")
                return

            if not year_pub.isdigit():
                messagebox.showerror('Adding Error', "Year Published must be a number!")
                return

            if not number_copies.isdigit():
                messagebox.showerror('Adding Error', "Number of Copies must be a number!")
                return

        except ValueError:
            messagebox.showerror('Adding Error', 'Invalid Inpur')
            return

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="libraryDB"
            )
        cursor = db.cursor()

        insert_query = "INSERT INTO Books (Title, Author, Year_published, Number_of_copies) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (title, author, year_pub, number_copies))
        db.commit()
        messagebox.showinfo("Success", "Data added successfully")

        cursor.close()
        db.close()

        title_ent.delete(0, tk.END)
        author_ent.delete(0, tk.END)
        y_p_ent.delete(0, tk.END)
        n_p_ent.delete(0, tk.END)
        fetch_books()

    lbl_title = tk.Label(frame_add_search_up_del, text='Title: ', font=('Arial', 11, 'bold'), bg='cyan')
    lbl_author = tk.Label(frame_add_search_up_del, text='Author: ', font=('Arial', 11,'bold'), bg='cyan')
    lbl_year_pub = tk.Label(frame_add_search_up_del, text='Year Published: ', font=('Arial', 11, 'bold'), bg='cyan')
    lbl_number_copies = tk.Label(frame_add_search_up_del, text='Number of Copies: ',font=('Arial', 11, 'bold'), bg='cyan')

    title_ent = tk.Entry(frame_add_search_up_del, border=3)
    author_ent = tk.Entry(frame_add_search_up_del, border=3)
    y_p_ent = tk.Entry(frame_add_search_up_del, border=3)
    n_p_ent = tk.Entry(frame_add_search_up_del, border=3)

    add_btn = tk.Button(frame_add_search_up_del, text='Submit', width=10, font=('Arial', 11,'bold' ),
        fg='White', bg='Blue', activebackground='Blue', activeforeground='White', command=add)

    lbl_title.grid(row=0, column=0)
    lbl_author.grid(row=2, column=0)
    lbl_year_pub.grid(row=4, column=0)
    lbl_number_copies.grid(row=6, column=0)

    title_ent.grid(row=1, column=0)
    author_ent.grid(row=3, column=0)
    y_p_ent.grid(row=5, column=0)
    n_p_ent.grid(row=7, column=0, pady=2)

    add_btn.grid(row=8, column=0, columnspan=2,  pady=4)


def fetch_books():
        
        for row in books_columns_tree.get_children():
            books_columns_tree.delete(row)

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="libraryDB"
            )
        cursor = db.cursor()

        cursor.execute("SELECT id, Title, Author, Year_published, Number_of_copies FROM Books")
        books = cursor.fetchall()

        for book in books:
            books_columns_tree.insert('', 'end', values=book)

        cursor.close()
        db.close()


def search(): 
    
    for widget in frame_add_search_up_del.winfo_children():
            widget.destroy()
    
    def search_book():

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="libraryDB"
            )
        cursor = db.cursor()

        try:
            search_term = ent_search.get()

            if not search_term:
                messagebox.showerror('Search Error', 'Enter Author or Title first')
                return

            if search_term.isdigit():
                messagebox.showerror('Search Error', 'Its must me a set of characters not integers')
                return 

        except ValueError:
            messagebox.showerror('Search Error', 'Invalid Input')

        search_query = '''SELECT * FROM Books WHERE Author LIKE %s OR Title LIKE %s'''
        values = ('%' + search_term + '%', '%' + search_term + '%')

        cursor.execute(search_query, values)
        results = cursor.fetchall()

        show_result = tk.Toplevel(root)

        lbl_result = tk.Label(show_result, text=f"Results for: {search_term}", font=('Arial', 12))
        lbl_result.pack(pady=10)

        listbox = tk.Listbox(show_result, width=58, height=15)
        listbox.pack(pady=10)

        if not results:
            lbl_result.config(text='No Books Found', font=('Arial', 15, 'bold'))
        
        else:
            for result in results:
                listbox.insert(tk.END, f"   {result[0]}) Title: {result[1]}, Author: {result[2]}, Year Pub: {result[3]}, Number copies: {result[4]}")
       
        cursor.close()
        db.close()

    lbl_search = tk.Label(frame_add_search_up_del, text='Enter the Author or Title of the Book you are looking for',font=('Arial', 11, 'bold'), bg='cyan')
    ent_search = tk.Entry(frame_add_search_up_del, border=3)
    btn_search = tk.Button(frame_add_search_up_del, text='Search', width=10, font=('Arial', 11,'bold'), command=search_book,fg='White', bg='Blue', activebackground='Blue', activeforeground='White')
    
    lbl_search.grid(row=0, column=0, pady=10)
    ent_search.grid(row=1, column=0, pady=10)
    btn_search.grid(row=2, column=0, pady=10)


def update():

    for widget in frame_add_search_up_del.winfo_children():
            widget.destroy()

    def save(updated_title, updated_author, updated_pub_year, updated_copies, record_id, update_window):

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="libraryDB"
            )
        cursor = db.cursor()

        update_query = """UPDATE Books SET Title=%s, Author=%s, Year_published=%s, Number_of_copies=%s 
                        WHERE id=%s""" 
        values = (updated_title, updated_author, updated_pub_year, updated_copies, record_id)

        cursor.execute(update_query, values)
        db.commit()
        update_window.destroy()
        cursor.close()
        db.close()
        fetch_books()

    def up():
        
        update_window = tk.Toplevel(root, padx=96, pady=14)
        update_window.title('UPDATE WINDOW')
        update_window.geometry('400x300')
        update_window.resizable(False, False)

        frame = tk.Frame(update_window, width=400, height=300)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0,ipadx=20, sticky="nsew")

        title = tk.Label(frame, text='Title:',font=('Arial', 11))
        author = tk.Label(frame, text='Author:',font=('Arial', 11))
        year_pub = tk.Label(frame, text='Year of Publised:',font=('Arial', 11))
        num_copies = tk.Label(frame, text='Number of Copies:',font=('Arial', 11))
        
        ent_title = tk.Entry(frame)
        ent_author = tk.Entry(frame)
        ent_pub = tk.Entry(frame)
        ent_copies = tk.Entry(frame)

        btn_save = tk.Button(frame, text='Save', width=10, font=('Arial', 11),
                    command=lambda: save(ent_title.get(), ent_author.get(), ent_pub.get(), ent_copies.get(), ent_id.get(), update_window))

        title.grid(row=0, column=0,  pady=2)
        author.grid(row=2, column=0,  pady=2)
        year_pub.grid(row=4, column=0,  pady=2)
        num_copies.grid(row=6, column=0,  pady=2)
        
        ent_title.grid(row=1, column=0,  pady=2)
        ent_author.grid(row=3, column=0,  pady=2)
        ent_pub.grid(row=5, column=0,  pady=2)
        ent_copies.grid(row=7, column=0,  pady=2)

        btn_save.grid(row=8, column=0, columnspan=2, pady=2)

        try:
            selected_id = ent_id.get()

            if not selected_id:
                messagebox.showerror('Update Error', 'Please Enter first the ID')
                return
            
            if not selected_id.isdigit():
                messagebox.showerror('Updare Error', 'Enter a valid interger')
                ent_id.delete(0, tk.END)
                return
        except ValueError:
            messagebox.showerror('Update Error', 'Please Enter a Valid ID')

        
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="libraryDB"
            )
        cursor = db.cursor()

        record_id = ent_id.get()
        cursor.execute("SELECT * FROM Books WHERE id=%s",(record_id,))
        books = cursor.fetchall()

        for book in books:
            ent_title.insert(0, book[1])
            ent_author.insert(0, book[2])
            ent_pub.insert(0, book[3])
            ent_copies.insert(0, book[4])
        
        cursor.close()
        db.close()
    
    lbl_id = tk.Label(frame_add_search_up_del, text='Enter ID that you want to update', font=('Arial', 11, 'bold'), bg='cyan')
    ent_id = tk.Entry(frame_add_search_up_del, border=3)
    btn_edit = tk.Button(frame_add_search_up_del, text='Enter', width=10,font=('Arial', 11, 'bold'),fg='White', bg='Blue', 
            activebackground='Blue', activeforeground='White', command=up)
    
    lbl_id.grid(row=0, column=0, pady=10)
    ent_id.grid(row=1, column=0, pady=5)
    btn_edit.grid(row=2, column=0, pady=5)


def delete():

    for widget in frame_add_search_up_del.winfo_children():
            widget.destroy()
    
    def delete_book():

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="libraryDB"
            )
        cursor = db.cursor()

        try:
            selected_id = ent_id.get()

            if not selected_id:
                messagebox.showerror('Delete Error', 'Please Enter first the ID')
                return
            if not selected_id.isdigit():
                messagebox.showerror('Delete Error', 'Enter a valid Interger')
                ent_id.delete(0, tk.END)
                return
        except ValueError:
            messagebox.showerror('Delete Error', 'Please Enter a Valid ID')

        delete_query = '''DELETE FROM Books WHERE id=%s'''
        values = (selected_id,)

        cursor.execute(delete_query, values)
        db.commit()

        cursor.close()
        db.close()
        fetch_books()
        
    lbl_id = tk.Label(frame_add_search_up_del, text='Enter Book ID that you want to delete', font=('Arial', 11, 'bold'), bg='cyan')
    ent_id = tk.Entry(frame_add_search_up_del, border=3)
    btn_del = tk.Button(frame_add_search_up_del, text='Delete Book', width=10, font=('Arial', 11, 'bold'),fg='White', bg='Blue', 
                activebackground='Blue', activeforeground='White', command=delete_book)
    
    lbl_id.grid(row=0, column=0, pady=10)
    ent_id.grid(row=1, column=0, pady=10)
    btn_del.grid(row=2, column=0, pady=10)



root = tk.Tk()
root.resizable(False, False)
root.geometry('1000x600')

frame_menu = tk.LabelFrame(root, width=200, height=600, pady=155, padx=5, bg='deep sky blue')
frame_menu.grid_propagate(False)
frame_menu.grid(row=0, column=0)
frame_menu.grid_columnconfigure(0, weight=1)

btn_add = tk.Button(frame_menu, text='ADD BOOK', font=('Arial', 13,'bold'), width=14, bg='yellow', activebackground='yellow',command=add_book)
btn_add.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=10)

btn_search = tk.Button(frame_menu, text="SEARCH BOOK", font=('Arial', 13, 'bold'),width=14, bg='lawn green', activebackground='lawn green', command=search)
btn_search.grid(row=1, column=0, columnspan=2,sticky='nsew', pady=10)

btn_update = tk.Button(frame_menu, text="UPDATE BOOK", font=('Arial', 13, 'bold'),width=14, bg='gold', activebackground='gold', command=update)
btn_update.grid(row=2, column=0, columnspan=2,sticky='nsew', pady=10)

btn_delete = tk.Button(frame_menu, text="DELETE BOOK", font=('Arial', 13, 'bold'),width=14, bg='dark orange', activebackground='dark orange',command=delete)
btn_delete.grid(row=3, column=0, columnspan=2,sticky='nsew', pady=10)

frame_2 = tk.LabelFrame(root, width=800, height=600, bg='floral white')
frame_2.grid_propagate(False)
frame_2.grid(row=0, column=1, sticky='nsew')
frame_2.grid_columnconfigure(0, weight=1)
frame_2.grid_rowconfigure(1, weight=1)

frame_add_search_up_del = tk.LabelFrame(frame_2, width=785, height=260, pady=7, bg='cyan')
frame_add_search_up_del.grid_propagate(False)
frame_add_search_up_del.grid_columnconfigure(0, weight=1)
frame_add_search_up_del.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

lbl_text = tk.Label(frame_add_search_up_del, text='WELCOME', font=('Arial', 20, 'bold'), fg='Blue', bg='cyan')
lbl_text.grid(row=0, column=0, pady=105, padx=10)

headings_style = ttk.Style()
headings_style.configure("Treeview.Heading", background="lawn green", foreground="black", font=('Arial', 11, 'bold'))

books_columns = ('ID','Title', 'Author', 'Year Publised', 'Number of Copies')
books_columns_tree = ttk.Treeview(frame_2, columns=books_columns, show='headings', height=15)
books_columns_tree.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

books_columns_tree.heading('ID', text='ID')
books_columns_tree.heading('Title', text='Title')
books_columns_tree.heading('Author', text='Author')
books_columns_tree.heading('Year Publised', text='Year Publised')
books_columns_tree.heading('Number of Copies', text='Number of Copies')

books_columns_tree.column('ID', width=50, anchor='center')
books_columns_tree.column('Title', width=220, anchor='center')
books_columns_tree.column('Author', width=180, anchor='center')
books_columns_tree.column('Year Publised', width=165, anchor='center')
books_columns_tree.column('Number of Copies', width=170, anchor='center')

# scrollbar = ttk.Scrollbar(frame_2, orient="vertical", command=books_columns_tree.yview)
# scrollbar.grid(row=1, column=1, sticky='ns')
# books_columns_tree.configure(yscrollcommand=scrollbar.set)

treeview_style = ttk.Style()
treeview_style.theme_use('default')
treeview_style.configure('Treeview', background="cyan", foreground="black", fieldbackground="cyan")
#treeview_style.map("Treeview", background=[('selected', 'lawn green')])

fetch_books()

root.mainloop()