import tkinter as tk
from tkinter import Button, Entry, Label, messagebox, Toplevel
import openai
import sqlite3

#Set your OpenAI API key
openai.api_key = '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'
#REST OF CODE


conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID INTEGER PRIMARY KEY,
                    Email TEXT UNIQUE NOT NULL,
                    Password TEXT NOT NULL
                  )''')
conn.commit()






def on_click(event):
    if user_input_entry.get() == "Please ask any questions":
        user_input_entry.delete(0, tk.END)


def start_chatbot():
    print("Welcome! The Chatbot is ready for your questions")
def send_to_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace model to 'gpt-3.5-turbo'
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
        max_tokens=100

    )
    return response['choices'][0]['message']['content'].strip()


def process_user_input():  ##adding event=none
    user_input = user_input_entry.get()
    user_input_entry.delete(0, tk.END)

    # Send user input to OpenAI for generating a response
    response = send_to_openai(user_input)

    # Display the response in the chat window
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"User: {user_input}\n")
    chat_display.insert(tk.END, f"Chatbot: {response}\n\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

#CREATE ROOT WINDOW
root = tk.Tk()
root.title("chatbot GUI")
#size and color
window_width = root.winfo_screenwidth() // 5
window_height = root.winfo_screenheight() // 2
root.geometry(f"{window_width}x{window_height}")

###BINDING THE ENTER KEY TO THE USER_INPUT_ENTRY WIDGET
user_input_entry = Entry(root, width=50, state="disabled")
user_input_entry.insert(0, "Please ask any questions regarding your problems")
user_input_entry.bind("<FocusIn>", on_click)
user_input_entry.pack(expand=True, fill='x')

#BIND THE ENTER KEY TO THE USER_INPUT_ENTRY WIDGET
user_input_entry.bind("<Return>", process_user_input)

# Chat entry and buttons initially disabled
business_contact_button = Button(root, text="Business Contact", command=lambda: display_contact_info(),
                                 state="disabled")


###DEFINING LOGIN
def open_login_page():
    login_window = Toplevel(root)
    login_window.title("Login")

    email_label = Label(login_window, text="Email:")
    email_label.grid(row=0, column=0, padx=10, pady=5)
    email_entry = Entry(login_window)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = Label(login_window, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    login_button = Button(login_window, text="Login", command=lambda: login(email_entry.get(), password_entry.get()))
    login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    back_button = Button(login_window, text="Back", command=login_window.destroy)
    back_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # Enable chat entry and buttons when logged in
    user_input_entry.config(state="normal")
    business_contact_button.config(state="normal")
    tracking_information_button.config(state="normal")


def open_sign_up_page():
    sign_up_window = Toplevel(root)
    sign_up_window.title("Sign Up")

    email_label = Label(sign_up_window, text="Email:")
    email_label.grid(row=0, column=0, padx=10, pady=5)
    email_entry = Entry(sign_up_window)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = Label(sign_up_window, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry = Entry(sign_up_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    reenter_password_label = Label(sign_up_window, text="Re-enter Password:")
    reenter_password_label.grid(row=2, column=0, padx=10, pady=5)
    reenter_password_entry = Entry(sign_up_window, show="*")
    reenter_password_entry.grid(row=2, column=1, padx=10, pady=5)

    sign_up_button = Button(sign_up_window, text="Sign Up",
                            command=lambda: sign_up(email_entry.get(), password_entry.get(),
                                                    reenter_password_entry.get()))
    sign_up_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    back_button = Button(sign_up_window, text="Back", command=sign_up_window.destroy)
    back_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # Enable chat entry and buttons when signed up
    user_input_entry.config(state="normal")
    business_contact_button.config(state="normal")
    tracking_information_button.config(state="normal")


def guest_login():
    print("Guest login")

    # Enable chat entry and buttons for guest login
    user_input_entry.config(state="normal")
    business_contact_button.config(state="normal")
    tracking_information_button.config(state="normal")


def sign_up(email, password, confirm_password):
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match. Please try again.")
        return

    try:
        cursor.execute("INSERT INTO Users (Email, Password) VALUES (?, ?)", (email, password))
        conn.commit()
        messagebox.showinfo("Success", "Sign-up successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists. Please choose another.")


def login(email, password):
    cursor.execute("SELECT * FROM Users WHERE Email = ? AND Password = ?", (email, password))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("Success", "Login successful!")

        # Enable chat entry and buttons when logged in
        user_input_entry.config(state="normal")
        business_contact_button.config(state="normal")
        tracking_information_button.config(state="normal")
    else:
        messagebox.showerror("Error", "Invalid email or password. Please try again.")


def display_contact_info():
    phone_label.config(text="Phone Number: 123-456-7890")
    address_label.config(text="Address: 123 Main St, City, Country")
    email_label.config(text="Email: contact@example.com")


# Chat entry and buttons initially disabled
user_input_entry = Entry(root, width=50, state="disabled")
user_input_entry.insert(0, "Please ask any questions regarding your problems")
user_input_entry.bind("<FocusIn>", on_click)
user_input_entry.pack(expand=True, fill='x')

# Create button to send user input
send_button = Button(root, text="Enter", command=process_user_input)
send_button.pack()

business_contact_button = Button(root, text="Business Contact", command=lambda: display_contact_info(),
                                 state="disabled")
business_contact_button.pack()
tracking_information_button = Button(root, text="Track Order", state="disabled")
tracking_information_button.pack()

phone_label = Label(root, text="")
phone_label.pack()

address_label = Label(root, text="")
address_label.pack()

email_label = Label(root, text="")
email_label.pack()

# Create buttons for different actions
login_button = Button(root, text="Login", command=open_login_page)
login_button.pack()

sign_up_button = Button(root, text="Sign Up", command=open_sign_up_page)
sign_up_button.pack()

guest_button = Button(root, text="Guest", command=guest_login)
guest_button.pack()

##AI INTEGRATION
# Enable chat entry and buttons
user_input_entry.config(state="normal")
business_contact_button.config(state="normal")
tracking_information_button.config(state="normal")


# Create chat display area
chat_display = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
chat_display.pack(expand=True, fill='both')


# Create button to send user input
send_button = Button(root, text="Send",)
send_button.pack()
# Create button to send user input
send_button.pack()


root.mainloop()
