#Code by IKrehan#

#obs: line 142

from tkinter import *
from bcrypt import *
import os, sys

#Change the cursor when its on button
def check_hand(e):
    bbox= canvas.bbox(button_login, text_login)
    if bbox[0] < e.x and bbox[2] > e.x and bbox[1] < e.y and bbox[3] > e.y:
        canvas.config(cursor="hand1")
    else:
        canvas.config(cursor="")
        # tendi nada, stackoverflow deve explicações

def login(e):
    if not username.get() or not password.get():
        canvas.itemconfig(warning, text="Please complete all fields!", fill="red")

    else:
        user_check = username.get()
        pass_check = password.get()

        # Load and check the users and passwords
        data_file = open("DATA.txt", "r")
        for line in data_file:
            pos = line.find(":")  # ':' is the division between user and password
            user_crypto = line[:pos]
            
            #remove line break
            pass_w_linebreak = line[pos+1:]
            pass_n = pass_w_linebreak.find("\n")
            pass_crypto = pass_w_linebreak[:pass_n]

            # Check if the input is compatible with the data
            user_flag = checkpw(user_check.encode("utf8"), user_crypto.encode("utf8"))
            pass_flag = checkpw(pass_check.encode("utf8"), pass_crypto.encode("utf8"))


            if user_flag == True and pass_flag == True:
                canvas.itemconfig(warning, text="Sucess!", fill="green")

            else:
                canvas.itemconfig(warning, text="Invalid user or password", fill="red")
        
        data_file.close()


def registration(e):


    def register(e):
        us = username_reg.get()
        ps = password_reg.get()
        salt = gensalt(8) # Crypto Pattern

        user_crypt = hashpw(us.encode('utf8'), salt)
        pass_crypt = hashpw(ps.encode('utf8'), salt)

        # Structure in data: "user:password"
        us_data = user_crypt.decode('utf8') + ":"
        ps_data = pass_crypt.decode('utf8') + "\n"
        data_login = us_data + ps_data

        if not username_reg.get() or not password_reg.get() or not password_confirm.get():
            canvas_register.itemconfig(warn, text="Please complete all fields", fill="red")

        else:
            if password_reg.get() == password_confirm.get():
                data_file = open("DATA.txt", "r")
                for line in data_file:
                    pos = line.find(":")
                    user_crypto = line[:pos]

                    if checkpw(us.encode('utf8'), user_crypto.encode('utf8')) == True:
                        canvas_register.itemconfig(warn, text="Username already used", fill="red")

                    else:
                        canvas_register.itemconfig(warn, text="Sucess!", fill="green")

                        insert_data = open("DATA.txt", "a")
                        insert_data.write(data_login)
                        insert_data.close()
                data_file.close()
                
            else:
                canvas_register.itemconfig(warn, text="Passwords are different!", fill="red")
    #create a new Window to register the user
    root2 = Toplevel()
    root2.title("Registration")
    root2.geometry("350x300")
    root2.resizable(width=False, height=False)

    canvas_register = Canvas(root2, width=350, height=300)
    canvas_register.pack()

    # background
    canvas_register.create_image(0, 0, image=background, anchor=NW)

    # Decoration
    #Entrys
    canvas_register.create_rectangle(55, 55, 305, 85, fill="snow", outline="snow")
    canvas_register.create_image(75, 70, image=user_icon_entry)

    canvas_register.create_rectangle(55, 105, 305, 135, fill="snow", outline="snow")
    canvas_register. create_image(75, 120, image=pass_icon_entry)

    canvas_register.create_rectangle(55, 155, 305, 185, fill="snow", outline="snow")
    canvas_register. create_image(75, 170, image=pass_icon_entry)


    # Variables who receive the input of user
    username_reg = StringVar()
    password_reg = StringVar()
    password_confirm = StringVar()

    # Entrys: Where user entry user ans password
    Entry(canvas_register, textvariable=username_reg, width=25, bd=0, highlightthickness=0, bg="snow").place(x=100, y=60)
    Entry(canvas_register, textvariable=password_reg, show="*", width=25, bd=0, highlightthickness=0, bg="snow").place(x=100, y=110) 
    Entry(canvas_register, textvariable=password_confirm, show="*", width=25, bd=0, highlightthickness=0, bg="snow").place(x=100, y=160) 


    #Button Register
    button_reg = canvas_register.create_rectangle(125, 220, 225, 250, fill="snow", outline="snow", activefill="gainsboro", activeoutline="gainsboro")
    text_reg = canvas_register.create_text(175, 235, text="Register")
    canvas_register.tag_bind(button_reg, "<Button-1>", register)

    # Warnings Label
    warn = canvas_register.create_text(180, 200, text="")


root = Tk()
root.title("Login")
root.geometry("500x500")
root.resizable(width=False, height=False)

canvas = Canvas(root, width=500, height=500)
canvas.pack()

# Open images 
# Paths can be differents in others computers
background = PhotoImage(file="~/Documents/Projetos/Login/back.png")
user_icon_entry = PhotoImage(file="~/Documents/Projetos/Login/man.png")
pass_icon_entry = PhotoImage(file="~/Documents/Projetos/Login/lock.png")
user_icon = PhotoImage(file="~/Documents/Projetos/Login/user.png")

# Background
canvas.create_image(0, 0, image=background, anchor=NW)


# Decoration
#Entrys
canvas.create_rectangle(125, 260, 375, 290, fill="snow", outline="snow")
canvas.create_image(143, 275, image=user_icon_entry)

canvas.create_rectangle(125, 300, 375, 330, fill="snow", outline="snow")
canvas. create_image(143, 315, image=pass_icon_entry)

# Window
canvas.create_image(250, 125, image=user_icon)


# Variables who receive the input of user
username = StringVar()
password = StringVar()

# Entrys: Where user entry user ans password
username_entry = Entry(canvas, textvariable=username, width=25, bd=0, highlightthickness=0, bg="snow").place(x=170, y=265)
password_entry = Entry(canvas, textvariable=password, show="*", width=25, bd=0, highlightthickness=0, bg="snow").place(x=170, y=305) 

# Buttons: Execute commands

# Login
button_login = canvas.create_rectangle(200, 380, 300, 410, fill="snow", outline="snow", activefill="gainsboro", activeoutline="gainsboro")
text_login = canvas.create_text(250, 395, text="Login")
canvas.tag_bind(text_login, "<Button-1>", login)
canvas.tag_bind(button_login, "<Button-1>", login)

# Register
button_register = canvas.create_text(340, 345, text="Sign Up", activefill="blue")
canvas.tag_bind(button_register,"<Button-1>" ,registration)

# Warnings Label
warning = canvas.create_text(200, 350, text="")

canvas.bind("<Motion>",check_hand)


root.mainloop() 
