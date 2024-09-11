import tkinter
from tkinter import *
import csv
import pandas as pd
from twilio.rest import Client
import os


account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

contact_numbers = []


def add_recipient_to_list():
    number = number_entry.get()
    name = name_entry.get()
    name_and_number = [name, number]
    if number not in contact_numbers:
        contact_numbers.append(number)
        name_entry.delete(0, END)
        number_entry.delete(0, END)
        with open("contactlist.csv", "a", newline="") as contact_details:
            df = pd.DataFrame([name_and_number])
            df.to_csv(contact_details, mode="a", index=False, header=False)
        waiting_label.config(text="Contact details added!")
        number_entry.insert(tkinter.END, "+353")


def show_recipient_list():
    new_window = Toplevel(window)
    new_window.title("Recipients")
    text_display = Text(new_window, width=20, height=20)
    text_display.grid()
    with open("contactlist.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            text_display.insert(END, " | ".join(row) + "\n")


def send_message():
    client = Client(account_sid, auth_token)
    with open("contactlist.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, phone_number = row
            message = client.messages.create(
                body=f"Hey {name}! Our next hike is at {location_entry.get()}. \n"
                     f"The starting point is {start_point.get()}.\n"
                     f"{start_date.get()}\n"
                     f"{start_time.get()}\n"
                     f"ᨒ↟",
                from_="+12564821816",
                to=phone_number,
            )
            print(f"Message sent to {name} ({phone_number}) - SID: {message.sid}")
            print(message.body)

    waiting_label.config(text="Text Sent to all recipients!")


window = Tk()
window.title("Event notifier")
window.config(padx=50, pady=50)

Label(window, text="Contact Name").grid(row=0, column=0)
Label(window, text="Phone number").grid(row=1, column=0)
Label(window, text="Location").grid(row=4, column=0)
Label(window, text="Start Point").grid(row=5, column=0)
Label(window, text="Date").grid(row=6, column=0)
Label(window, text="Time").grid(row=7, column=0)


name_entry = Entry(window)
number_entry = Entry(window)
location_entry = Entry(window)
start_point = Entry(window)
start_date = Entry(window)
start_time = Entry(window)

name_entry.grid(row=0, column=1)
number_entry.insert(tkinter.END, "+353")
number_entry.grid(row=1, column=1)
location_entry.grid(row=4, column=1)
start_point.grid(row=5, column=1)
start_date.grid(row=6, column=1)
start_time.grid(row=7, column=1)

add_recipient = tkinter.Button(text="Add person to recipient list",
                               relief=GROOVE,
                               width=25,
                               command=add_recipient_to_list,
                               pady=10,
                               highlightthickness=0,
                               bd=2)
add_recipient.grid(row=2, columnspan=2)
show_recipients = tkinter.Button(text="Show Recipient list",
                                 relief=GROOVE,
                                 width=25,
                                 command=show_recipient_list,
                                 pady=10,
                                 highlightthickness=0,
                                 bd=2)
show_recipients.grid(row=3, columnspan=2)
send_button = tkinter.Button(text="Send text",
                             relief=GROOVE,
                             width=25,
                             command=send_message,
                             pady=10,
                             highlightthickness=0,
                             bd=2)
send_button.grid(row=9, columnspan=2)

waiting_label = Label(window, text="Waiting...")
waiting_label.grid(row=10, columnspan=2)


window.mainloop()
