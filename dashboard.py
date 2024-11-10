import tkinter as tk
import mysql.connector
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
#import front_page as fp


class DashBoard:
    def __init__(self, root):
        self.root = root

        ##  The First Frame That hold the Option_Menu Button Section ##
        self.frame_menu = tk.LabelFrame(self.root, width=190, height=700)
        self.frame_menu.grid(row=0, column=0)
        self.frame_menu.grid_propagate(False)

        ###########
        self.frame = tk.Frame(self.frame_menu)
        self.frame.grid(row=0, column=0, columnspan=2, pady=4, ipady=20)

        self.img = Image.open("prof.png")
        self.resized_img = self.img.resize((70, 70))
        self.tk_img = ImageTk.PhotoImage(self.resized_img)
        lbl_img = tk.Label(self.frame, image=self.tk_img)
        lbl_img.grid(row=0, column=0)

        lbl_t = tk.Label(self.frame, text="Welcome Admin", font=("Arial",12, 'bold'))
        lbl_t.grid(row=1, column=0)
        ############

        ### From Frame Menu ###
        # Add Data  Button Section
        lbl_add = tk.Label(self.frame_menu, text="ADD DATA", font=('Arial', 10, 'bold'), pady=5)
        lbl_add.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.add_option = ["Cash in", "Cash out"]
        self.choose_add = tk.StringVar(value=self.add_option[0])
        add_btn = tk.OptionMenu(self.frame_menu, self.choose_add, *self.add_option, command=self.chose_add)
        add_btn.config(width=17)
        add_btn.grid(row=2, column=0, columnspan=2)

        # Update Data Button Section #
        lbl_update = tk.Label(self.frame_menu, text="UPDATE DATA", font=('Arial', 10, 'bold'), pady=5)
        lbl_update.grid(row=3, column=0, columnspan=2)
        self.up_option = ["Cash in", "Cash out"]
        self.choose_up = tk.StringVar(value=self.up_option[0])
        up_btn = tk.OptionMenu(self.frame_menu, self.choose_up, *self.up_option, command=self.chose_update)
        up_btn.config(width=17)
        up_btn.grid(row=4, column=0, columnspan=2)

        # Delete Data Button Section #
        lbl_del = tk.Label(self.frame_menu, text="DELETE DATA", font=('Arial', 10, 'bold'), pady=5)
        lbl_del.grid(row=5, column=0, columnspan=2)
        self.del_option = ["Cash in", "Cash out"]
        self.choose_del = tk.StringVar(value=self.del_option[0])

        btn_del = tk.OptionMenu(self.frame_menu, self.choose_del, *self.del_option, command=self.chose_delete)
        btn_del.config(width=17)
        btn_del.grid(row=6, column=0, columnspan=2)

        # Count the total Amount And Charge Button Section #
        lbl_total = tk.Label(self.frame_menu, text="TOTAL: AMOUNT/CHARGE", font=('Arial', 10, 'bold'), pady=5)
        lbl_total.grid(row=7, column=0, columnspan=2)
        self.total_option = ["Cash in", "Cash out"]
        self.choose_total = tk.StringVar(value=self.del_option[0])

        btn_total = tk.OptionMenu(self.frame_menu, self.choose_total, *self.total_option, command=self.chose_to_total)
        btn_total.config(width=17)
        btn_total.grid(row=8, column=0, columnspan=2)

        #### Log Out ####
        btn_log = tk.Button(self.frame_menu, text='Sign Out', font=('Arial', 10, 'bold'), width=17, command=self.sign_out)
        btn_log.grid(row=9, column=0, columnspan=2, pady=260)
        ###########

        ## The Second Frame That holds the two tables represent by Treeview namely the Cash_out and Cash_in ##
        self.frame_tables = tk.LabelFrame(self.root, width=900, height=700, background='white')
        self.frame_tables.grid(row=0, column=1, sticky='nsew', padx=2) 
        self.frame_tables.grid_propagate(False) 
        self.frame_tables.grid_columnconfigure(0, weight=1)
        self.frame_tables.grid_rowconfigure(0, weight=1)
        self.frame_tables.grid_rowconfigure(1, weight=1)  

        #############
        # Frame Cash Out
        self.c_o_frame = tk.LabelFrame(self.frame_tables,text='CASH OUT TABLE', labelanchor='n', width=600, height=100)
        self.c_o_frame.grid(row=0, column=0, ipady=100, sticky='nsew', padx=10, pady=10)
        self.c_o_frame.grid_propagate(False)
        self.c_o_frame.grid_rowconfigure(0, weight=1)
        self.c_o_frame.grid_columnconfigure(0, weight=1)

        c_o_columns = ('ID','Reference Num', 'Amount', 'Charge', 'Date', 'Signature')

        self.c_o_tree = ttk.Treeview(self.c_o_frame, columns=c_o_columns, show='headings')
        self.c_o_tree.grid(row=0, column=0, sticky="nsew")

        self.c_o_tree.heading('ID', text='ID')
        self.c_o_tree.heading('Reference Num', text='Reference #')
        self.c_o_tree.heading('Amount', text='Amount')
        self.c_o_tree.heading('Charge', text='Charge')
        self.c_o_tree.heading('Date', text='Date: YYYY-MM-DD')
        self.c_o_tree.heading('Signature', text='Signature')

        self.c_o_tree.column('ID', width=80, anchor='center')
        self.c_o_tree.column('Reference Num', width=120, anchor='center')
        self.c_o_tree.column('Amount', width=80, anchor='center')
        self.c_o_tree.column('Charge', width=80, anchor='center')
        self.c_o_tree.column('Date', width=120, anchor='center')
        self.c_o_tree.column('Signature', width=100, anchor='center')

        c_o_scrollbar = ttk.Scrollbar(self.c_o_frame, orient="vertical", command=self.c_o_tree.yview)
        c_o_scrollbar.grid(row=0, column=1, sticky='ns')
        self.c_o_tree.configure(yscrollcommand=c_o_scrollbar.set)

        self.treeview_style = ttk.Style()
        self.treeview_style.theme_use('default')
        self.treeview_style.configure('Treeview', background="#58F5E7", foreground="black",
                                 fieldbackground="#58F5E7")
        self.treeview_style.map("Treeview", background=[('selected', '#A34708')])

        self.fetch_cash_out_data()

        # Frame Cash In
        self.c_i_frame = tk.LabelFrame(self.frame_tables, text='CASH IN TABLE', labelanchor='n', width=600, height=300)
        self.c_i_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.c_i_frame.grid_propagate(False)
        self.c_i_frame.grid_rowconfigure(0, weight=1)
        self.c_i_frame.grid_columnconfigure(0, weight=1)

        c_i_columns = ('ID','Sender Name', 'Gcash Num', 'Amount', 'Charge','Date')

        self.c_i_tree = ttk.Treeview(self.c_i_frame, columns=c_i_columns, show='headings', height=12)
        self.c_i_tree.grid(row=0, column=0, sticky="nsew")

        self.c_i_tree.heading('ID', text='ID')
        self.c_i_tree.heading('Sender Name', text='Sender Name')
        self.c_i_tree.heading('Gcash Num', text='Gcash Num')
        self.c_i_tree.heading('Amount', text='Amount')
        self.c_i_tree.heading('Charge', text='Charge')
        self.c_i_tree.heading('Date', text='Date: YYYY-MM-DD')

        self.c_i_tree.column('ID', width=80, anchor='center')
        self.c_i_tree.column('Sender Name', width=120, anchor='center')
        self.c_i_tree.column('Gcash Num', width=120, anchor='center')
        self.c_i_tree.column('Amount', width=80, anchor='center')
        self.c_i_tree.column('Charge', width=80, anchor='center')
        self.c_i_tree.column('Date', width=120, anchor='center')
    
        scrollbar = ttk.Scrollbar(self.c_i_frame, orient="vertical", command=self.c_i_tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.c_i_tree.configure(yscrollcommand=scrollbar.set)

        self.fetch_cash_in_data()
        ############

        

        ## The Third Frame which hold the widgets came from the Option_Menu Button ##
        self.third_frame = tk.LabelFrame(self.root, width=280, height=700)
        self.third_frame.grid(row=0, column=2)
        self.third_frame.grid_propagate(False)

        # Frame for Adding Data
        self.frame_add = tk.LabelFrame(self.third_frame, width=270, height=320)
        self.frame_add.grid(row=0, column=0, sticky='ns')
        self.frame_add.grid_propagate(False)  
        lbl = tk.Label(self.frame_add, text='NO ENTRY', font=('Arial', 19, 'bold'), padx=67, pady=100)
        lbl.grid(row=0, column=0)

        # Frame for total
        self.frame_total = tk.LabelFrame(self.third_frame, width=270, height=375)
        self.frame_total.grid(row=1, column=0)
        self.frame_total.grid_propagate(False)
        lbl = tk.Label(self.frame_total, text='NO ENTRY', font=('Arial', 19, 'bold'), padx=67, pady=110)
        lbl.grid(row=0, column=0)
                        

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="gcash_db"

        )
        self.cursor = self.db.cursor()

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS gcash_db")
        
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cash_out(
                    id INT primary key auto_increment,
                    Reference_number VARCHAR(13),
                    Amount INT,
                    Charge INT,
                    Date DATE,
                    Signature VARCHAR(50)
                )
        """)
        self.cursor.execute("""

                CREATE TABLE IF NOT EXISTS cash_in(
                    id INT primary key auto_increment,
                    Sender_Name VARCHAR(50),
                    Phone_number VARCHAR(11),
                    Amount INT,
                    Charge INT,
                    Date DATE
                )
        """)

        self.db.commit()
        self.cursor.close()
        self.db.close()




    def sign_out(self):
        self.root.destroy()
        
    
########### ADDING CASH-IN AND CASH-OUT DATA #################################
    def chose_add(self, *args):
      
        for widget in self.frame_add.winfo_children():
            widget.destroy()

        choosen = self.choose_add.get()

        if choosen == "Cash in":
            self.cash_in_form_add()
        else:
            self.cash_out_form_add()

    ####### ADD CASH-IN DATA #######
    def cash_in_form_add(self):
        
        lbl = tk.Label(self.frame_add, text="CASH IN", fg="Blue", font=('Arial Bold', 12))
        lbl.grid(row=0, column=0, columnspan=2)

        lbl_s_n = tk.Label(self.frame_add, text="Sender Name:")        
        lbl_phone_num = tk.Label(self.frame_add, text="Phone #:")       
        lbl_amount = tk.Label(self.frame_add, text="Amount:")       
        lbl_charge = tk.Label(self.frame_add, text="Charge:")      
        lbl_date = tk.Label(self.frame_add, text="Date: Y-M-D")

        self.ent_s_n = tk.Entry(self.frame_add)       
        self.ent_phone_num = tk.Entry(self.frame_add)       
        self.ent_amount = tk.Entry(self.frame_add)       
        self.ent_charge = tk.Entry(self.frame_add)       
        self.ent_date = tk.Entry(self.frame_add)

        btn_add = tk.Button(self.frame_add, text="ADD DATA", font=('Arial', 11, 'bold'), command=self.add_cash_in)

        lbl_s_n.grid(row=1, column=0, sticky='w', pady=5)
        lbl_phone_num.grid(row=2, column=0, sticky='w', pady=5)
        lbl_amount.grid(row=3, column=0, sticky='w', pady=5)
        lbl_charge.grid(row=4, column=0, sticky='w', pady=5)
        lbl_date.grid(row=5, column=0, sticky='w', pady=5)

        self.ent_s_n.grid(row=1, column=1,pady=5)
        self.ent_phone_num.grid(row=2, column=1,pady=5)
        self.ent_amount.grid(row=3, column=1,pady=5)
        self.ent_charge.grid(row=4, column=1,pady=5)
        self.ent_date.grid(row=5, column=1, pady=5 )

        btn_add.grid(row=6, column=0, columnspan=2, pady=5)

    def add_cash_in(self):

        sender_name = self.ent_s_n.get()
        phone_num = self.ent_phone_num.get()
        amount = self.ent_amount.get()
        charge = self.ent_charge.get()
        date = self.ent_date.get()

        if not (sender_name and phone_num and amount and charge and date):
            messagebox.showerror("Error", "All fields must be filled")
            return
        
        if not sender_name.isalpha():
            messagebox.showerror("Error", "Sender Name should be valid Name")
            return
        
        if not phone_num.isdigit():
            messagebox.showerror('Error', 'Phone Number should be valid Integers')
            return
        
        if len(phone_num) > 11 or len(phone_num) < 11:
            messagebox.showerror('Error', 'Please Enter a valid Phone Number')
            return
        
        if not charge.isdigit():
            messagebox.showerror('Error', 'Charge should be valid Integers')
            return
        
        if not amount.isdigit():
            messagebox.showerror('Error', 'Amount should be valid Integers')
            return
        
        self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
        self.cursor = self.db.cursor()

        insert_query = "INSERT INTO cash_in (Sender_Name, Phone_number, Amount, Charge, Date) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(insert_query, (sender_name, phone_num, amount, charge, date))
        self.db.commit()
        messagebox.showinfo("Success", "Cash In data added successfully")

        self.cursor.close()
        self.db.close()

        self.ent_s_n.delete(0, tk.END)
        self.ent_phone_num.delete(0, tk.END)
        self.ent_amount.delete(0, tk.END)
        self.ent_charge.delete(0, tk.END)
        self.ent_date.delete(0, tk.END)

        self.fetch_cash_in_data()

    def fetch_cash_in_data(self):

        for row in self.c_i_tree.get_children():
            self.c_i_tree.delete(row)

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="gcash_db"
        )
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT id, Sender_Name, Phone_number, Amount, Charge, Date FROM cash_in")
        rows = self.cursor.fetchall()

        for row in rows:
            self.c_i_tree.insert('', 'end', values=row)

        self.cursor.close()
        self.db.close()

    ####### ADD CASH-OUT DATA #######
    def cash_out_form_add(self):

        lbl = tk.Label(self.frame_add, text="CASH OUT", fg="Blue", font=('Arial Bold', 12))
        lbl.grid(row=0, column=0, columnspan=2)
        
        lbl_ref = tk.Label(self.frame_add, text="Reference #: ")
        lbl_am = tk.Label(self.frame_add, text="Amount: ")       
        lbl_charge = tk.Label(self.frame_add, text="Charge: ")       
        lbl_da = tk.Label(self.frame_add, text="Date: Y-M-D ")       
        lbl_sig = tk.Label(self.frame_add, text="Signature: ")

        self.ent_ref = tk.Entry(self.frame_add)
        self.ent_am = tk.Entry(self.frame_add) 
        self.ent_charge = tk.Entry(self.frame_add)       
        self.ent_da = tk.Entry(self.frame_add)       
        self.ent_sig = tk.Entry(self.frame_add)

        btn_add = tk.Button(self.frame_add, text="ADD DATA", font=('Arial', 11, 'bold'), command=self.add_cash_out)

        lbl_ref.grid(row=1, column=0, sticky='w', pady=5)
        lbl_am.grid(row=2, column=0, sticky='w', pady=5)
        lbl_charge.grid(row=3, column=0, sticky='w', pady=5)
        lbl_da.grid(row=4, column=0, sticky='w', pady=5)
        lbl_sig.grid(row=5, column=0, sticky='w', pady=5)

        self.ent_ref.grid(row=1, column=1, pady=5)
        self.ent_am.grid(row=2, column=1, pady=5)
        self.ent_charge.grid(row=3, column=1, pady=5)
        self.ent_da.grid(row=4, column=1,pady=5)
        self.ent_sig.grid(row=5, column=1,pady=5)

        btn_add.grid(row=6, column=0, columnspan=2, pady=5)

    def add_cash_out(self):

        reference = self.ent_ref.get()
        amount = self.ent_am.get()
        charge = self.ent_charge.get()
        date = self.ent_da.get()
        signature = self.ent_sig.get()

        if not (reference and amount and charge and date and signature):
            messagebox.showerror("Error", "All fields must be filled")
            return
        self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
        self.cursor = self.db.cursor()

        insert_query = "INSERT INTO cash_out (Reference_number, Amount, Charge, Date, Signature) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(insert_query, (reference, amount, charge, date, signature))
        self.db.commit()
        messagebox.showinfo("Success", "Cash out data added successfully")

        self.cursor.close()
        self.db.close()

        self.ent_ref.delete(0, tk.END)
        self.ent_am.delete(0, tk.END)
        self.ent_charge.delete(0, tk.END)
        self.ent_da.delete(0, tk.END)
        self.ent_sig.delete(0, tk.END)

        self.fetch_cash_out_data()

    def fetch_cash_out_data(self):

        for row in self.c_o_tree.get_children():
            self.c_o_tree.delete(row)

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="gcash_db"
        )
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT id, Reference_number, Amount, Charge, Date, Signature FROM cash_out")
        rows = self.cursor.fetchall()

        for row in rows:
            self.c_o_tree.insert('', 'end', values=row)

        self.cursor.close()
        self.db.close()
############################################################################

################### UPDATING CASH IN AND CASH OUT ##########################
    def chose_update(self, *args):
        
        for widget in self.frame_add.winfo_children():
            widget.destroy()

        choosen = self.choose_up.get()

        if choosen == "Cash in":
            self.update_c_i()

        else:
            self.update_c_o()

    ####### UPDATE CASH-IN #######   
    def update_c_i(self):

        lbl_id = tk.Label(self.frame_add, text='Enter ID that you want to update', font=('Arial', 11))
        self.ent_id = tk.Entry(self.frame_add)
        
        btn_save = tk.Button(self.frame_add, text='ENTER', font=('Arial', 11, 'bold'), width=10, command=self.up_cash_in)
        
        lbl_id.grid(row=0, column=0, padx=28, pady=12)
        self.ent_id.grid(row=1, column=0, pady=12)
        btn_save.grid(row=2, column=0, columnspan=2, pady=12)

    def up_cash_in(self):

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
        cursor = db.cursor()
        
        self.update_window_c_i = tk.Toplevel(self.root)
        self.update_window_c_i.resizable(False, False)

        frame = tk.LabelFrame(self.update_window_c_i)
        frame.grid(row=0, column=0)

        edit_s_n = tk.Label(frame, text="Sender Name:")      
        edit_phone_num = tk.Label(frame, text="Phone #:")     
        edit_amount = tk.Label(frame, text="Amount:")
        edit_charge = tk.Label(frame, text="Charge:")
        edit_date = tk.Label(frame, text="Date: M/D/Y")

        edit_ent_s_n = tk.Entry(frame)       
        edit_ent_phone_num = tk.Entry(frame)       
        edit_ent_amount = tk.Entry(frame)        
        edit_ent_charge = tk.Entry(frame)       
        edit_ent_date = tk.Entry(frame)

        edit_s_n.grid(row=0, column=0, sticky='w', pady=5)
        edit_phone_num.grid(row=1, column=0, sticky='w', pady=5)
        edit_amount.grid(row=2, column=0, sticky='w', pady=5)
        edit_charge.grid(row=3, column=0, sticky='w', pady=5)
        edit_date.grid(row=4, column=0, sticky='w', pady=5)

        edit_ent_s_n.grid(row=0, column=1,pady=5)
        edit_ent_phone_num.grid(row=1, column=1,pady=5)
        edit_ent_amount.grid(row=2, column=1,pady=5)
        edit_ent_charge.grid(row=3, column=1,pady=5)
        edit_ent_date.grid(row=4, column=1, pady=5 )

        btn_save_c_in = tk.Button(frame, text="SAVE", width=10, command=lambda: self.save_cash_in(
            edit_ent_s_n.get(),edit_ent_phone_num.get(), edit_ent_amount.get(),edit_ent_charge.get(),
            edit_ent_date.get()
        ))
        btn_save_c_in.grid(row=5, column=0, columnspan=2, pady=5)

        record_id_c_i = self.ent_id.get()
        cursor.execute("SELECT * FROM cash_in WHERE id=%s",(record_id_c_i,))
        cash_in_data = cursor.fetchall()

        for data in cash_in_data:
            edit_ent_s_n.insert(0, data[1])
            edit_ent_phone_num.insert(0, data[2])
            edit_ent_amount.insert(0, data[3])
            edit_ent_charge.insert(0, data[4])
            edit_ent_date.insert(0, data[5])
        cursor.close()
        db.close()
    def save_cash_in(self, sender_name, phone_num, amount, charge, date):
        
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
        cursor = db.cursor()

        updated_id = self.ent_id.get()
        update_query = """UPDATE cash_in SET Sender_Name=%s, Phone_number=%s, Amount=%s, Charge=%s, Date=%s 
                        WHERE id=%s""" 
        values = (sender_name, phone_num, amount, charge, date, updated_id)
        cursor.execute(update_query, values)
        db.commit()
        self.update_window_c_i.destroy()
        cursor.close()
        db.close()
        self.fetch_cash_in_data()

    ###### UPDATE CASH OUT ######
    def update_c_o(self):

        for widget in self.frame_add.winfo_children():
            widget.destroy()

        lbl_id = tk.Label(self.frame_add, text='Enter ID that you want to update', font=('Arial', 11))
        self.ent_id_c_o = tk.Entry(self.frame_add)
        
        btn_save = tk.Button(self.frame_add, text='ENTER', font=('Arial', 11, 'bold'), width=10, command=self.up_cash_out)

        lbl_id.grid(row=0, column=0, padx=28, pady=12)
        self.ent_id_c_o.grid(row=1, column=0, pady=12)
        btn_save.grid(row=2, column=0, columnspan=2, pady=12)

    def up_cash_out(self):

        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
        cursor = db.cursor()

        self.update_window_c_o = tk.Toplevel(self.root)
        self.update_window_c_o.resizable(False, False)

        frame_o = tk.LabelFrame(self.update_window_c_o)
        frame_o.grid(row=0, column=0)
        
        edit_lbl_ref = tk.Label(frame_o, text="Reference #: ")
        edit_lbl_am = tk.Label(frame_o, text="Amount: ")
        edit_lbl_charge = tk.Label(frame_o, text="Charge: ")
        edit_lbl_da = tk.Label(frame_o, text="Date: M/D/Y ")
        edit_lbl_sig = tk.Label(frame_o, text="Signature: ")
        
        edit_ent_ref = tk.Entry(frame_o)
        edit_ent_am = tk.Entry(frame_o)
        edit_ent_charge = tk.Entry(frame_o)
        edit_ent_da = tk.Entry(frame_o)
        edit_ent_sig = tk.Entry(frame_o)

        edit_lbl_ref.grid(row=0, column=0, sticky='w', pady=5)
        edit_lbl_am.grid(row=1, column=0, sticky='w', pady=5)
        edit_lbl_charge.grid(row=2, column=0, sticky='w', pady=5)
        edit_lbl_da.grid(row=3, column=0, sticky='w', pady=5)
        edit_lbl_sig.grid(row=4, column=0, sticky='w', pady=5)

        edit_ent_ref.grid(row=0, column=1, pady=5)
        edit_ent_am.grid(row=1, column=1, pady=5)
        edit_ent_charge.grid(row=2, column=1, pady=5)
        edit_ent_da.grid(row=3, column=1,pady=5)
        edit_ent_sig.grid(row=4, column=1,pady=5)

        btn_save_c_o = tk.Button(frame_o, text="SAVE", width=10, command=lambda: self.save_cash_out(
              edit_ent_ref.get(),edit_ent_am.get(),edit_ent_charge.get(),edit_ent_da.get(),edit_ent_sig.get() 
        ))
        btn_save_c_o.grid(row=5, column=0, columnspan=2, pady=5)

        record_id_c_0 = self.ent_id_c_o.get()
        cursor.execute("SELECT * FROM cash_out WHERE id=%s",(record_id_c_0,))
        cash_out_data = cursor.fetchall()

        for data in cash_out_data:
            edit_ent_ref.insert(0, data[1])
            edit_ent_am.insert(0, data[2])
            edit_ent_charge.insert(0, data[3])
            edit_ent_da.insert(0, data[4])
            edit_ent_sig.insert(0, data[5])

        cursor.close()
        db.close()
    def save_cash_out(self, reference, amount, charge, date, signature):
        
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
        cursor = db.cursor()

        updated_id = self.ent_id_c_o.get()
        update_query = """UPDATE cash_out SET Reference_number=%s, Amount=%s, Charge=%s, Date=%s, Signature=%s 
                        WHERE id=%s""" 
        values = (reference,amount, charge, date, signature, updated_id)
        cursor.execute(update_query, values)
        db.commit()
        self.update_window_c_o.destroy()
        cursor.close()
        db.close()
        self.fetch_cash_out_data()
#############################################################################

########## DELETING CASH-IN AND CASH-OUT DATA ##############################
    def chose_delete(self, *args):
        
        for widget in self.frame_add.winfo_children():
            widget.destroy()

        choosen = self.choose_del.get()

        if choosen == "Cash in":
            self.delete_c_i()

        else:
            self.delete_c_o()

    ### DELETE CASH-IN DATA ###
    def delete_c_i(self):

        for widget in self.frame_add.winfo_children():
            widget.destroy()

        def delete_cash_in_data():
            
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
            cursor = db.cursor()

            try:
                del_id = selected_id_del.get()

                if not del_id:
                    messagebox.showerror('Delete Error', 'Please ente first an ID')
                    return 
                if not del_id.isdigit():
                    messagebox.showerror('Delete Error', 'Please Enter a valid integers ID')
                    selected_id_del.delete(0, tk.END)
                    return
            except ValueError:
                messagebox.showerror('Delete Error', 'Please Enter a Valid ID')

            delete_query = '''DELETE FROM cash_in WHERE id=%s'''
            values = (del_id,)
            cursor.execute(delete_query, values)
            db.commit()

            cursor.close()
            db.close()
            self.fetch_cash_in_data()
            selected_id_del.delete(0, tk.END)

        lbl_id = tk.Label(self.frame_add, text='Enter ID that you want to delete', font=('Arial', 11))
        selected_id_del = tk.Entry(self.frame_add)
        
        btn_del = tk.Button(self.frame_add, text='DELETE DATA', width=11, font=('Arial', 11, 'bold'),command=delete_cash_in_data)
        
        lbl_id.grid(row=0, column=0, padx=28, pady=12)
        selected_id_del.grid(row=1, column=0, pady=12)
        btn_del.grid(row=2, column=0, columnspan=2, pady=12)

    ### DELETE CASH-OUT DATA ###
    def delete_c_o(self):
        
        for widget in self.frame_add.winfo_children():
            widget.destroy()

        def delete_cash_out_data():
            
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="gcash_db"
            )
            cursor = db.cursor()

            try:
                del_id = selected_id_del_c_o.get()

                if not del_id:
                    messagebox.showerror('Delete Error', 'Please ente first an ID')
                    return 
                if not del_id.isdigit():
                    messagebox.showerror('Delete Error', 'Please Enter a valid integers ID')
                    selected_id_del_c_o.delete(0, tk.END)
                    return
            except ValueError:
                messagebox.showerror('Delete Error', 'Please Enter a Valid ID')

            delete_c_o_query = '''DELETE FROM cash_out WHERE id=%s'''
            values = (del_id,)
            cursor.execute(delete_c_o_query, values)
            db.commit()

            cursor.close()
            db.close()
            self.fetch_cash_out_data()
            selected_id_del_c_o.delete(0, tk.END)

        lbl_id = tk.Label(self.frame_add, text='Enter ID that you want to delete', font=('Arial', 11))
        selected_id_del_c_o = tk.Entry(self.frame_add)
        
        btn_del_c_o = tk.Button(self.frame_add, text='DELETE DATA', width=11, font=('Arial', 11, 'bold'),command=delete_cash_out_data)
        
        lbl_id.grid(row=0, column=0, padx=28, pady=12)
        selected_id_del_c_o.grid(row=1, column=0, pady=12)
        btn_del_c_o.grid(row=2, column=0, columnspan=2, pady=12)

###### TO SUM UP THE AMOUNT AND CHARGE IN CASH-IN AND CASH-OUT ############
    def chose_to_total(self, *args):

        for widget in self.frame_total.winfo_children():
            widget.destroy()

        choosen = self.choose_total.get()

        if choosen == "Cash in":
            self.cash_in_total()
        else:
            self.cash_out_total()

    def cash_in_total(self):

        for widget in self.frame_total.winfo_children():
            widget.destroy()

        def sum_up_c_i():
            
            from_date = ent_from_date.get()
            to_date = ent_date_to.get()

            try:
                
                db_connection = mysql.connector.connect(
                    host="localhost",       
                    user="root",
                    password="1234",
                    database="gcash_db"  
                )
                cursor = db_connection.cursor()

                sum_query = """SELECT SUM(amount), SUM(charge) FROM cash_in WHERE date BETWEEN %s AND %s"""
                cursor.execute(sum_query, (from_date, to_date))
                result = cursor.fetchone()

                if result:
                    total_amount, total_charge = result
                    total_cash_in = total_amount + total_charge if total_amount and total_charge else 0
                    messagebox.showinfo("Total Cash-In", f"Total Amount: {total_amount}\nTotal Charge: {total_charge}\nGrand Total: {total_cash_in}")
                else:
                    messagebox.showwarning("No Data", "No transactions found in the specified date range.")
                cursor.close()
                db_connection.close()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
        
        lbl_c_i = tk.Label(self.frame_total, text='TOTAL CASH - IN', font=('Arial', 12, 'bold'), padx=65)
        
        lbl_from_date = tk.Label(self.frame_total, text='From:', font=('Arial', 11, 'bold'), pady=5)
        ent_from_date = tk.Entry(self.frame_total)
        
        lbl_date_to = tk.Label(self.frame_total, text='To:', font=('Arial', 11, 'bold'), pady=5)
        ent_date_to = tk.Entry(self.frame_total)
        
        btn_total = tk.Button(self.frame_total, text='TOTAL', font=('Arial', 11, 'bold'), width=10, command=sum_up_c_i)
        
        lbl_c_i.grid(row=0, column=0, pady=25)
        lbl_from_date.grid(row=1, column=0, sticky='w')
        ent_from_date.grid(row=2, column=0)
        lbl_date_to.grid(row=3, column=0, sticky='w')
        ent_date_to.grid(row=4, column=0)
        btn_total.grid(row=5, column=0, columnspan=2, pady=7)
    
    def cash_out_total(self):

        for widget in self.frame_total.winfo_children():
            widget.destroy()

        def sum_up_c_o():

            from_date = ent_from_date.get()
            to_date = ent_date_to.get()

            try:
                
                db_connection = mysql.connector.connect(
                    host="localhost",       
                    user="root",
                    password="1234",
                    database="gcash_db"  
                )
                cursor = db_connection.cursor()

                sum_query = """SELECT SUM(amount), SUM(charge) FROM cash_out WHERE date BETWEEN %s AND %s"""
                cursor.execute(sum_query, (from_date, to_date))
                result = cursor.fetchone()

                if result:
                    total_amount, total_charge = result
                    total_cash_in = total_amount + total_charge if total_amount and total_charge else 0
                    messagebox.showinfo("Total Cash-In", f"Total Amount: {total_amount}\nTotal Charge: {total_charge}\nGrand Total: {total_cash_in}")
                else:
                    messagebox.showwarning("No Data", "No transactions found in the specified date range.")
                cursor.close()
                db_connection.close()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
        
        lbl_c_o = tk.Label(self.frame_total, text='TOTAL CASH-OUT', font=('Arial', 12, 'bold'), padx=65)

        lbl_from_date = tk.Label(self.frame_total, text='From:', font=('Arial', 11, 'bold'), pady=5)
        ent_from_date = tk.Entry(self.frame_total)

        lbl_date_to = tk.Label(self.frame_total, text='To:', font=('Arial', 11, 'bold'), pady=5)
        ent_date_to = tk.Entry(self.frame_total)
      
        btn_total = tk.Button(self.frame_total, text='TOTAL', font=('Arial', 11, 'bold'), width=10, command=sum_up_c_o)
        
        lbl_c_o.grid(row=0, column=0, pady=25)
        lbl_from_date.grid(row=1, column=0, sticky='w')
        ent_from_date.grid(row=2, column=0)
        lbl_date_to.grid(row=3, column=0, sticky='w')
        ent_date_to.grid(row=4, column=0)
        btn_total.grid(row=5, column=0, columnspan=2, pady=7)
################################################################################




def main():

    root = tk.Tk()
    root.resizable(False, False)
    Dash = DashBoard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
