from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_letter = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_number = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbol = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = password_letter + password_number + password_symbol

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    with open("data.txt", "a") as file:
        data_list = [website_entry.get() + " | ", username_entry.get() + " | ", password_entry.get() + "\n"]

        if website_entry.get() == "" or username_entry.get() == "" or password_entry.get() == "":
            messagebox.showwarning("Empty field", message="Please complete all fields")

        else:
            is_ok = messagebox.askokcancel(title=website_entry.get(),
                                           message=f"These are the details entered: \nEmail: {username_entry.get()}"
                                                   f"\nPassword: {password_entry.get()} \nIs it ok to save?")
            if is_ok:
                file.writelines(data_list)
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

# Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entry
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2, sticky=EW)
website_entry.focus()

username_entry = Entry(width=35)
username_entry.grid(row=2, column=1, columnspan=2, sticky=EW)
username_entry.insert(END, "pelealex02@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky=EW)

# Button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

save_password = Button(text="Add", width=36, command=add_password)
save_password.grid(row=4, column=1, columnspan=2, sticky=EW)

window.mainloop()
