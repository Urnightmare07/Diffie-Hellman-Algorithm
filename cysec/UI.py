from tkinter import *
from tkinter import messagebox as mb
from client import Client
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow
import pickle
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import random

a = Tk()
a.title("ISAAProject")
a.geometry("1000x600")
a.configure(bg="black")

# Heading
head = Label(a, text="MODIFIED DIFFIE HELLMAN WITH AES ENCRYPTION AND NETWORK INTRUSION CHECK")
head.config(font=("Helvetica bold", 15, "bold"), fg="green", bg="black")
head.place(x=100, y=10)

# Explanation
s = "This program is made for a safer key exchange by modifying the currently existing Diffie Hellman algorithm and then further encrypting the key \nusing the AES encryption algorithm"
exp = Label(a, text=s)
exp.config(font=('Helvetica bold', 12), fg="green", bg="black")
exp.place(x=10, y=125)

# Our names
names = Label(a, text="Avinash\n\nYogeesh\n\nJai\n\nRishi\n\nAnand")
names.config(font=("Helvetica bold", 12, "bold"), fg="green", bg="black")
names.place(x=425, y=250)

def net():
    print("Inside network check")
    a.destroy()
    b = Tk()
    b.title("Network Intrusion Check")
    b.geometry("500x500")
    b.configure(bg="black")
    b.focus_force()

    # Heading
    head = Label(b, text="NETWORK INTRUSION CHECK")
    head.config(font=("Helvetica bold", 15, "bold"), fg="green", bg="black")
    head.place(x=110, y=10)

    # Inputting name of user
    lname = Label(b, text="Name")
    lname.config(font=("Helvetica bold", 12), fg="green", bg="black")
    lname.place(x=125, y=150)
    ename = Entry(b)
    ename.place(x=190, y=150)

    def netcheck():
        print("Inside network check function")
        name = ename.get()
        dataset = pd.read_csv('Train_data.csv')
        y = dataset['class']
        dataset.drop(columns=['class', 'src_bytes', 'land', 'num_failed_logins', 'urgent', 'srv_count'], inplace=True)
        y = pd.DataFrame(y)
        
        columns = ['protocol_type', 'service', 'flag']
        lb = LabelEncoder()
        
        for i in columns:
            dataset[i] = lb.fit_transform(dataset[i])
        y = lb.fit_transform(y)
        y = pd.DataFrame(y)
        
        X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.25, random_state=0)
        model = XGBClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        print(accuracy_score(y_test, y_pred))

        num = random.randint(0, 6298)
        print(y_pred)
        x = y_pred[num]
        
        if x:
            mb.showinfo("Network Intrusion Check", "Network is Safe")
            b.destroy()
            
            # We call client.py here
            def send(event=None):  # event is passed by binders.
                # Handles sending of messages.
                msg = my_msg.get()
                my_msg.set("")  # Clears input field.
                msg_list.insert("end", name + " : " + msg)
                client.send_message(msg)
                if msg == "{quit}":
                    top.quit()

            def on_closing(event=None):
                # This function is to be called when the window is closed.
                my_msg.set("{quit}")
                send()

            top = Tk()
            top.title("Chatter")
            top.configure(bg="white")
            messages_frame = Frame(top)
            my_msg = StringVar()  # For the messages to be sent.
            my_msg.set("Type your messages here.")
            scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
            # Following will contain the messages.
            msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)
            msg_list.pack(side=LEFT, fill=BOTH)
            msg_list.pack()
            msg_list.configure(bg="black", fg="green")
            messages_frame.pack()
            entry_field = Entry(top, textvariable=my_msg)
            entry_field.bind("<Return>", send)
            entry_field.pack()
            entry_field.configure(fg="green")
            send_button = Button(top, text="Send", command=send)
            send_button.pack()
            send_button.configure(fg="green")
            
            s = "Welcome " + name
            msg_list.insert("end", s)
            top.protocol("WM_DELETE_WINDOW", on_closing)
            print("Generating key...")
            client = Client("localhost", 5000)
            client.establish_session()
            top.mainloop()
        else:
            mb.showerror("Network Intrusion Check", "Network is not safe")
            b.destroy()

    butnetintcheck = Button(b, text="Check Network Intrusion", command=netcheck).place(x=185, y=400)
    
butnetintcheck = Button(a, text="Check Network Intrusion", command=net)
butnetintcheck.config(fg="green")
butnetintcheck.place(x=400, y=550)

a.mainloop()
