from tkinter import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20)

# Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")

canvas.create_image(100,100,image=logo_img)
canvas.grid(row= 0, column = 1)

#Label
website_label = Label(text="Website:")
website_label.grid(row= 1, column= 0)

username_label = Label(text="Email/Username:")
username_label.grid(row= 2, column= 0)

password_label = Label(text="Password:")
password_label.grid(row= 3, column= 0)

#Entry
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)

username_entry = Label(width=35)
username_entry.grid(row=2, column=1, columnspan=2)




window.mainloop()
