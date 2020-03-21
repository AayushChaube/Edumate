# -*- coding: utf-8 -*-
"""

@author: Aayush Chaube
"""

from tkinter import *
from tkinter import messagebox
import re, pymysql
from PIL import *

def adjustWindow(window):
    w = 600 # Width for the window size
    h = 600 # Height for the window size
    ws = screen.winfo_screenwidth() # Width of the screen
    hs = screen.winfo_screenheight() # Height of the screen
    x = (ws/2)-(w/2) # Calculate x and y coordinates for the Tk window
    y = (hs/2)-(h/2)
    window.geometry('%dx%d+%d+%d' %(w, h, x, y)) # Set the dimension of the screen and where it is placed
    window.resizable(True, True) # Disabling the resize option for the window
    window.configure(background = 'white') # Making the background white of the window

def enter_new_record(entryField, semester):
    found = 0
    for student in entryField:
        for field in student:
            if(field.get() == ""): # validating all fields entered or not
                found = 1
                break
    if found == 0:
        if semester.get() == '--0--':
            messagebox.showerror("Error", "Please select your current semester", parent=screen4) # displaying message for invalid details
        else:
            # enter new record
            connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate") # database connection
            cursor = connection.cursor()
            for fields in entryField:
                insert_query = "INSERT INTO student_records (subject_name, marks_scored, out_off, credit_point, semester, student_id) VALUES('"+ fields[0].get() + "', "+ str(fields[1].get()) + ", "+ str(fields[2].get()) + ", "+ str(fields[3].get()) + ", "+ str(semester.get()) + ", "+ str(studentID) + ");" # queries for inserting values
                cursor.execute(insert_query) # executing the queries
            connection.commit() # commiting the connection then closing it.
            connection.close() # closing the connection of the database
            messagebox.showinfo("Congratulation", "Entry Succesfull",parent=screen2) # displaying message for successful entry
            screen4.destroy()
    else:
        messagebox.showerror("Error", "Please fill all the details", parent=screen4) # displaying message for invalid details

def student_new_record():
    global screen4
    semester = StringVar()
    entryField = list()
    screen4 = Toplevel(screen)
    screen4.title("New Record")
    adjustWindow(screen4) # configuring the window
    Label(screen4, text="Enter New Record", width='31', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').grid(row=0, sticky=W, columnspan=4)
    Label(screen4, text="", bg='#174873', width='60', height='18').place(x=0, y=127)
    Label(screen4, text="", bg='white').grid(row=1,column=0)
    Label(screen4, text="Subject Name", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=0, pady=(5,10))
    Label(screen4, text="Your Marks", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=1, pady=(5,10))
    Label(screen4, text="Out of", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=2, pady=(5,10))
    Label(screen4, text="Credits Points", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=3, pady=(5,10))
    rowNo = 3
    for i in range(6): # this loop will generate all input field for taking input from the user
        temp = list()
        for j in range(4):
            e = Entry(screen4, width=14)
            e.grid(row=rowNo,column=j, padx=(3,0), pady=(0,25))
            temp.append(e)
        entryField.append(temp)
        rowNo += 2
    Label(screen4, text="Select Sem:", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=rowNo,column=0, pady=(15,0))
    list1 = ['1','2','3','4','5','6','7','8']
    droplist = OptionMenu(screen4, semester, *list1)
    semester.set('--0--')
    droplist.config(width=5)
    droplist.grid(row=rowNo, column=1, pady=(15,0))
    Button(screen4, text='Submit', width=20, font=("Open Sans", 13, 'bold'), bg='brown', fg='white', command=lambda: enter_new_record(entryField, semester)).grid(row=rowNo,columnspan=2,column=2, pady=(15,0))

def fetch_record(semester):
    if semester == '--0--':
        messagebox.showerror("Error", "Please select proper semester", parent=screen4) # displaying message for invalid details
    else:
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate") # database connection
        cursor = connection.cursor()
        select_query = "SELECT subject_name, marks_scored, out_off, credit_point FROM student_records where semester = " + str(semester.get()) + " AND student_id = " + str(studentID) + ";" # queries for retrieving values
        cursor.execute(select_query) # executing the queries
        student_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(student_record) > 0:
            for i in range(len(student_record)): # this loop will display the information to the user
                for j in range(4):
                    Label(screen3, text=student_record[i][j], font=("Open Sans", 11, 'bold'), fg='white', bg='#174873').grid(row=i+4,column=j, pady=(5,10))
            output = list() # calculation of cgpa starts from here
            for record in student_record:
                temp = list()
                per = (record[1]/record[2]) * 100.0
                per
                if per >= 80:
                    temp.append(10)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 75 and per < 80:
                    temp.append(9)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 70 and per < 75:
                    temp.append(8)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 60 and per < 70:
                    temp.append(7)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 50 and per < 60:
                    temp.append(6)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 45 and per < 50:
                    temp.append(5)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 40 and per < 45:
                    temp.append(4)
                    temp.append(record[3])
                    output.append(temp)
                else:
                    temp.append(0)
                    temp.append(record[3])
                    output.append(temp)
            credits_earned = total_credit_points = 0
            for result in output:
                credits_earned += result[0] * result[1]
                total_credit_points += result[1]
            cgpa = credits_earned/total_credit_points
            percentage = 7.1 * cgpa + 11 # cgpa calculation ends over here
            Label(screen3, text="Your CGPI", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=0, pady=(15,10))
            Label(screen3, text=cgpa, font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=1, pady=(15,10))
            Label(screen3, text="Percentage", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=2, pady=(15,10))
            Label(screen3, text=percentage, font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=3, pady=(15,10))
        else:
            messagebox.showerror("Error", "Entry not found", parent=screen3) # displaying message for invalid semester details

def student_records():
    global screen3
    semester = StringVar()
    screen3 = Toplevel(screen)
    screen3.title("Student Records")
    adjustWindow(screen3) # configuring the window
    Label(screen3, text="Your Record", width='31', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').grid(row=0, sticky=W, columnspan=4)
    Label(screen3, text="", bg='#174873', width='60', height='18').place(x=0, y=127)
    Label(screen3, text="", bg='white').grid(row=1,column=0)
    Label(screen3, text="Select Sem:", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=2,column=0, pady=(5,0))
    list1 = ['1','2','3','4','5','6','7','8']
    droplist = OptionMenu(screen3, semester, *list1, command=lambda x: fetch_record(semester))
    semester.set('--0--')
    droplist.config(width=5)
    droplist.grid(row=2, column=1, pady=(5,0))
    Label(screen3, text="Subject Name", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=0, pady=(15,10))
    Label(screen3, text="Your Marks", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=1, pady=(15,10))
    Label(screen3, text="Out of", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=2, pady=(15,10))
    Label(screen3, text="Credits Points", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=3,column=3, pady=(15,10))

def welcome_page(student_info):
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Welcome")
    adjustWindow(screen2) # configuring the window
    Label(screen2, text="Welcome " + student_info[0][1], width='32', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').place(x=0, y=0)
    Label(screen2, text="", bg='#174873', width='20', height='20').place(x=0, y=96)
    Message(screen2, text='" Some people dream of accomplishing great things. Others stay awake and make it happen. "\n\n - By Some Night Owl', width='180', font=("Helvetica", 10, 'bold', 'italic'), fg='white', bg='#174873', anchor = CENTER).place(x=10, y=100)
    photo = PhotoImage(file="hires.png") # opening left side image - Note: If image is in same folder then no need to mention the full path
    label = Label(screen2, image=photo, text="") # attaching image to the label
    label.place(x=10, y=270)
    label.image = photo # it is necessary in Tkinter to keep a instance of image to display image in label
    photo1 = PhotoImage(file="Slide1.1.PNG") # opening right side image - Note: If image is in same folder then no need to mention the full path
    label1 = Label(screen2, image=photo1, text="") # attaching image to the label
    label1.place(x=200, y=96)
    label1.image = photo1 # it is necessary in Tkinter to keep a instance of image to display image in label
    Button(screen2, text='Enter your grades', width=20, font=("Open Sans", 13, 'bold'), bg='brown', fg='white', command=student_new_record).place(x=270, y=250)
    Button(screen2, text='Check your result', width=20, font=("Open Sans", 13, 'bold'), bg='brown', fg='white', command=student_records).place(x=270, y=350)

def register_user():
    if fullname.get() and email.get() and password.get() and repassword.get() and gender.get(): # checking for all empty values in entry field
        if university.get() == "--select your university--": # checking for selection of university
            Label(screen1, text = "Please select your university", fg = "red", font = ("calibri", 11), width = '30', anchor = W, bg = 'white').place(x = 0, y = 570)
            return
        else:
            if tnc.get(): # checking for acceptance of agreement
                if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email.get()): # validating the email
                    if password.get() == repassword.get(): # checking both password match or not if u enter in this block everything is fine just enter the values in database
                        gender_value = 'male'
                        if gender.get() == 2:
                            gender_value = 'female'
                        connection = pymysql.connect(host = "localhost", user = "root", passwd = "", database = "edumate") # database connection
                        cursor = connection.cursor()
                        insert_query = "INSERT INTO student_details (fullname, email, password, gender, university) VALUES('"+ fullname.get() + "', '"+ email.get() + "', '"+ password.get() + "', '"+ gender_value + "', '"+ university.get() + "' );" # queries for inserting values
                        cursor.execute(insert_query) # executing the queries
                        connection.commit() # commiting the connection then closing it.
                        connection.close() # closing the connection of the database
                        Label(screen1, text = "Registration Sucess", fg = "green", font = ("calibri", 11), width = '30', anchor = W, bg = 'white').place(x = 0, y = 570) #printing successful registration message
                        Button(screen1, text = 'Proceed to Login ->', width = 20, font = ("Open Sans", 9, 'bold'), bg = 'brown', fg = 'white',command = screen1.destroy).place(x = 170, y = 565) # button to navigate back to login page
                    else:
                        Label(screen1, text = "Password does not match", fg = "red", font = ("calibri", 11), width = '30', anchor = W, bg = 'white').place(x = 0, y = 570)
                        return
                else:
                    Label(screen1, text = "Please enter valid email id", fg = "red", font = ("calibri", 11), width = '30', anchor = W, bg = 'white').place(x = 0, y = 570)
                    return
            else:
                Label(screen1, text = "Please accept the agreement", fg = "red", font = ("calibri", 11), width = '30', anchor = W, bg = 'white').place(x = 0, y = 570)
                return
    else:
        Label(screen1, text = "Please fill all the details", fg = "red", font = ("calibri", 11), width = '30', anchor = W, bg = 'white').place(x = 0, y = 570)
        return

def register():
    global screen1, fullname, email, password, repassword, university, gender, tnc # making all entry field variable global
    fullname = StringVar()
    email = StringVar()
    password = StringVar()
    repassword = StringVar()
    university = StringVar()
    gender = IntVar()
    tnc = IntVar()
    screen1 = Toplevel(screen)
    screen1.title("Registeration")
    adjustWindow(screen1) # configuring the window
    Label(screen1, text = "Registration Form", width = '32', height = "2", font = ("Calibri", 22, 'bold'), fg = 'white', bg = '#d9660a').place(x = 0, y = 0)
    Label(screen1, text = "", bg = '#174873', width = '50', height = '17').place(x = 45, y = 120)
    Label(screen1, text = "Full Name:", font = ("Open Sans", 11, 'bold'), fg = 'white', bg = '#174873', anchor = W).place(x = 150, y = 160)
    Entry(screen1, textvar = fullname).place(x = 300, y = 160)
    Label(screen1, text = "Email ID:", font = ("Open Sans", 11, 'bold'), fg = 'white', bg = '#174873', anchor = W).place(x = 150, y = 210)
    Entry(screen1, textvar = email).place(x = 300, y = 210)
    Label(screen1, text = "Gender:", font = ("Open Sans", 11, 'bold'), fg = 'white', bg = '#174873', anchor = W).place(x = 150, y = 260)
    Radiobutton(screen1, text = "Male", variable = gender, value = 1, bg = '#174873').place(x = 300, y = 260)
    Radiobutton(screen1, text = "Female", variable = gender, value = 2,bg = '#174873').place(x = 370, y = 260)
    Label(screen1, text = "University:", font = ("Open Sans", 11, 'bold'), fg = 'white', bg = '#174873', anchor = W).place(x = 150, y = 310)
    list1 = ['Mumbai University', 'Savitribai Phule Pune Univeristy', 'Gujarat Technological University', 'JNTU Kakinada', 'University of Delhi', 'Anna University']
    droplist = OptionMenu(screen1, university, *list1)
    droplist.config(width = 17)
    university.set('--select your university--')
    droplist.place(x = 300, y = 305)
    Label(screen1, text = "Password:", font = ("Open Sans", 11, 'bold'), fg = 'white', bg = '#174873', anchor = W).place(x = 150, y = 360)
    Entry(screen1, textvar = password, show = "*").place(x = 300, y = 360)
    Label(screen1, text = "Re-Password:", font = ("Open Sans", 11, 'bold'), fg = 'white', bg = '#174873', anchor = W).place(x = 150, y = 410)
    entry_4 = Entry(screen1, textvar = repassword, show = "*")
    entry_4.place(x = 300, y = 410)
    Checkbutton(screen1, text = "I accept all terms and conditions", variable = tnc, bg = '#174873', font = ("Open Sans", 9, 'bold'), fg = 'brown').place(x = 175, y = 450)
    Button(screen1, text = 'Submit', width = 20, font = ("Open Sans", 13, 'bold'), bg = 'brown', fg = 'white', command = register_user).place(x = 170, y = 490)

def login_verify():
    global studentID
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate") # database connection
    cursor = connection.cursor()
    select_query = "SELECT * FROM student_details where email = '" + username_verify.get() + "' AND password = '" + password_verify.get() + "';" # queries for retrieving values
    cursor.execute(select_query) # executing the queries
    student_info = cursor.fetchall()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if student_info:
        messagebox.showinfo("Congratulation", "Login Succesfull") # displaying message for successful login
        studentID = student_info[0][0]
        welcome_page(student_info) # opening welcome window
    else:
        messagebox.showerror("Error", "Invalid Username or Password") # displaying message for invalid details

def main_screen():
    global screen, username_verify, password_verify
    screen=Tk()
    username_verify=StringVar()
    password_verify=StringVar()
    screen.title("EDUMATE")
    adjustWindow(screen)
    Label(screen, text="EDUMATE - Student Manager", width="500", height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').pack()
    Label(screen, text="", bg='white').pack()
    Label(screen, text="", bg='#174873',width='50', height='17').place(x=45, y=120) # bluebackground in middle of window
    Label(screen, text="Please enter details below to login", bg='#174873', fg='white').pack()
    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    Label(screen, text="Username * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack()
    Entry(screen, textvar=username_verify).pack()
    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    Label(screen, text="Password * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack()
    Entry(screen, textvar=password_verify, show="*").pack()
    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    Button(screen, text="LOGIN", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white', command=login_verify).pack()
    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    Button(screen, text="New User? Register Here", height="2", width="30", bg='#e79700', font=("Open Sans", 10, 'bold'), fg='white', command=register).pack()
    screen.mainloop()

main_screen()
