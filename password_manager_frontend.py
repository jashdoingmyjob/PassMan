import tkinter as tk
import tkinter.messagebox
import password_manager_api as api
from PIL import Image, ImageTk

def main():
    global root
    root = tk.Tk()
    root.title(string="PassMan")
    canvas = tk.Canvas(root, height = 300, width = 300, bg = "black")
    canvas.pack()
    img = tk.PhotoImage(file="password_icon.gif")
    canvas.create_image(0,0, anchor=tk.NW, image=img)
    # canvas.create_image(0,0, image=canvas.image, anchor='nw')
    canvas.pack()

    global service
    global username
    global password
    global username_entry
    global password_entry
    global service_entry
    service = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()
    tk.Label(text='Enter service').pack()
    service_entry = tk.Entry(textvariable=service)
    service_entry.pack()
    tk.Label(text='Enter username').pack()
    username_entry = tk.Entry(textvariable=username)
    username_entry.pack()
    tk.Label(text='Enter password').pack()
    password_entry = tk.Entry(textvariable=password)
    password_entry.pack()

    add_login = tk.Button(root, text="Add Login", padx=10, pady=5, fg="white", bg="#263D42", command=create_login)
    add_login.pack()
    list_logins = tk.Button(root, text="List Usernames", padx=10, pady=5, fg="white", bg="#263D42", command=show_logins)
    list_logins.pack()
    get_pass = tk.Button(root, text="What's my Password?", padx=10, pady=5, fg="white", bg="#263D42", command=show_password)
    get_pass.pack()

    root.mainloop()

def create_login():
    pm = api.PasswordManager()
    username_info = username.get()
    password_info = password.get()
    service_info = service.get()

    pm.add_login(service=service_info, user=username_info, password=password_info)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    service_entry.delete(0, tk.END)

def show_logins():
    pm = api.PasswordManager()
    service_info = service.get()
    users = pm.list_usernames(service=service_info)['usernames']
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    service_entry.delete(0, tk.END)
    # result = tk.Text(users)
    # result.pack()
    tk.messagebox.showinfo("Usernames for {}".format(service_info), users)

def show_password():
    pm = api.PasswordManager()
    service_info = service.get()
    username_info = username.get()
    password = pm.get_password(service=service_info, user=username_info)
    if 'Invalid' in password.keys():
        tk.messagebox.showinfo("Password for user {} for service {}".format(
        username_info, service_info), "There is no password for this user,please try again.")
    else:
        tk.messagebox.showinfo("Password for user {} for service {}".format(
        username_info, service_info), password['password'])

if __name__ == '__main__':
    main()
