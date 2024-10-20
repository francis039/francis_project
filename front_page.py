import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import dashboard as dash
        

def validate_login(event=None):
    email = email_ent.get()
    password = password_ent.get()

    if email == 'admin' and password == '123':
        root.destroy()
        dash.main() 

    else:
        messagebox.showerror( title = "Login Faild", message="Wrong Email and/or password")



root = tk.Tk()
root.config(bg='#00F2FE')
root.geometry('1370x700')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

img = Image.open("user.png")
resized_img = img.resize((100, 100))
tk_img = ImageTk.PhotoImage(resized_img)

form_frame = tk.Frame(root, background='white', borderwidth=30)
form_frame.grid(row=1, column=0, pady=20)


lbl_img = tk.Label(form_frame, image=tk_img, background='white', activebackground='white')
lbl_img.grid(row=0, column=0, columnspan=2)

form_lbl = tk.Label(form_frame, text="Login", fg="black", background='white',font=('Arial',19,'bold'))
form_lbl.grid(row=1, column=0, columnspan=2)

email_ent = tk.Entry(form_frame, borderwidth='4')
email_ent.config(width=30)
email_ent.insert(0, "User name")
email_ent.grid(row=2, column=0, pady=5, padx=5)

password_ent = tk.Entry(form_frame, borderwidth='4',show="*")
password_ent.config(width=30)
password_ent.insert(0, "Password")
password_ent.grid(row=3, column=0, pady=5, padx=5)

btn_login = tk.Button(form_frame, text="Login", bg="#1488CC", borderwidth='4',activebackground="#1488CC", 
                      activeforeground="white" ,fg="White", font=('Arial', 11, 'bold'), width=27, command=validate_login)
btn_login.grid(row=4, column=0, pady=5, padx=5)

# lbl_forgot = tk.Label(form_frame, text="Forgot Password?")
# lbl_forgot.grid(row=5, column=0, columnspan=2)

email_ent.bind("<Return>", validate_login)
password_ent.bind("<Return>", validate_login)

root.mainloop()