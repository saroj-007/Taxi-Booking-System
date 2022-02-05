from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.ttk import Combobox, Treeview
import random
import time
import datetime
from tkinter import messagebox as ms
import sqlite3
from tkcalendar import DateEntry
from PIL import ImageTk, Image


# *************************************************Database Structure Set****************************************

# create a User table with username and password
with sqlite3.connect('database.db') as db:
    c = db.cursor()

c.execute(
    '''CREATE TABLE IF NOT EXISTS user (userId INTEGER PRIMARY KEY AUTOINCREMENT,
                                        useremail VARCHAR(100) NOT NULL ,
                                        password VARCHAR(255) NOT NULL,
                                        username VARCHAR(100) NOT NULL, 
                                        useraddress VARCHAR(255) NOT NULL, 
                                        phone_number VARCHAR(55) NOT NULL,
                                        paymentmethod VARCHAR(100) NOT NULL, 
                                        cardnumber VARCHAR(55) NOT NULL, 
                                        CVV_number VARCHAR(55) NOT NULL)''')
db.commit()

# create a Driver table with drivername and password
c.execute(
    '''CREATE TABLE IF NOT EXISTS taxidriver(driverId INTEGER PRIMARY KEY AUTOINCREMENT,
                                              driveremail VARCHAR(255) NOT NULL ,
                                              driverpassword VARCHAR(255) NOT NULL,
                                              drivername VARCHAR(100) NOT NULL ,
                                              phone_number VARCHAR(55) NOT NULL,
                                              licenseplate VARCHAR(255) NOT NULL)''')
db.commit()


# create a UserReservation table with userId, date, current_location and destination, driverId
c.execute('''CREATE TABLE IF NOT EXISTS userReservation(date VARCHAR(255) NOT NULL,
                                                      cur_location VARCHAR(255) NOT NULL,
                                                      destination VARCHAR(255) NOT NULL,
                                                      pickup_time VARCHAR(255) NOT NULL,
                                                      
                                                      userId INTEGER PRIMARY KEY,
                                                      driverId INTEGER,
                                                      status VARCHAR(255) NOT NULL,
                                                      FOREIGN KEY (userId) REFERENCES user(userId),
                                                      FOREIGN KEY (driverId) REFERENCES taxidriver(driverId))''')
db.commit()


# create a DriverReservation table with driverId, date, current_location and destination, userId
c.execute(
    '''CREATE TABLE IF NOT EXISTS driverReservation ( availabelDate VARCHAR(255) NOT NULL ,
                                                      driverId INTEGER PRIMARY KEY,
                                                      userId INTEGER,
                                                      FOREIGN KEY (driverId) REFERENCES taxidriver(driverId),
                                                      FOREIGN KEY (userId) REFERENCES user(userId)
                                                      )''')
db.commit()


# create a Admin table with usename and password
c.execute(
    '''CREATE TABLE IF NOT EXISTS admin (adminId INTEGER PRIMARY KEY AUTOINCREMENT, 
                                       username VARCHAR(25) NOT NULL ,
                                       password VARCHAR(255) NOT NULL)''')
db.commit()
db.close()


# *******************************functionalities of the system*************************************

# Define display frame to show different frames
def display_frames(frame):
    frame.tkraise()

# Validating email, password and phone number


def check_email(email):
    regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False


def check_password(pw):
    if len(pw) > 6:
        return True
    else:
        return False


def check_phone_length(number):
    if(len(number)) == 10:
        return True
    else:
        return False


def check_cardnumber_length(number):
    if(len(number)) == 19:
        return True
    else:
        return False


def check_cvvnumber_length(number):
    if(len(number) == 4):
        return True
    else:
        return False

# ******************* create new user *******************************


def new_user():
    global username
    global useremail
    global userpassword
    global userphone_number
    global useraddress
    global userpayment
    global useraccountno

    address = useraddress.get()
    payment = userpayment.get()
    email = useremail.get()
    name = username.get()
    phone_number = userphone_number.get()
    password = userpassword.get()
    account = useraccountno.get()
    cvv = usercvvnumber.get()

    chk_email = check_email(email)
    chk_password = check_password(password)
    chk_phone = check_phone_length(phone_number)
    chk_cardnumber = check_cardnumber_length(account)
    chk_ccvnumber = check_cvvnumber_length(cvv)

    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # Find Existing username if any take proper action
    find_user = ('SELECT * FROM user WHERE useremail = ?')
    c.execute(find_user, [email])
    if address == "" or payment == "" or email == "" or name == "" or phone_number == "" or password == "" or account == "" or cvv == "":
        c.close()
        ms.showerror("Error", "All fields are required to fill")
    elif c.fetchall():
        c.close()
        ms.showerror('Error!', 'User Already Registered!')
    elif not chk_email:
        ms.showerror("Invalid", "Email not valid")
    elif not chk_password:
        ms.showerror("Error", "Password length must be greater than 6")
    elif not chk_phone:
        ms.showerror("Error", "Phone number must contain 10 digits")
    elif not chk_cardnumber:
        ms.showerror("Error", "Card number must contain 16 digits")
    elif not chk_ccvnumber:
        ms.showerror("Error", "CVV number must contain 4 digits")
    else:
        # Create New Account
        insert = 'INSERT INTO user(useremail,username,password,useraddress,paymentmethod,phone_number, cardnumber, CVV_number) VALUES(?,?,?,?,?,?,?,?)'
        c.execute(insert, [email, name, password, address,
                           payment, phone_number, account, cvv])

        db.commit()
        c.close()
        ms.showinfo('Success!', 'Registration successfull')
        customer_name_text.delete(0, END)
        customer_address_text.delete(0, END)
        customer_phone_text.delete(0, END)
        customer_email_text.delete(0, END)
        customer_password_text.delete(0, END)
        customer_payment_text.delete(0, END)
        display_frames(customer_home_frame)


# name = "ram"
# password = "ram"
# print(new_user(name, password))

# ******************* create new taxi-driver *******************************


def new_taxi_driver():
    global driveremail
    global driverpassword
    global drivername
    global driverlicenseplate
    global driverphone_number

    number = driverphone_number.get()
    email = driveremail.get()
    password = driverpassword.get()
    name = drivername.get()
    licenseplate = driverlicenseplate.get()

    chk_email = check_email(email)
    chk_password = check_password(password)
    chk_phone = check_phone_length(number)

    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # Find Existing username if any take proper action
    find_user = ('SELECT * FROM taxidriver WHERE driveremail = ?')
    c.execute(find_user, [email])
    if number == "" or email == "" or password == "" or name == "" or licenseplate == "":
        c.close()
        ms.showerror("Error", "All fields are required to fill")
    elif c.fetchall():
        c.close()
        ms.showerror('Error!', 'User Already Registered!')
    elif not chk_email:
        ms.showerror("Invalid", "Email not valid")
    elif not chk_password:
        ms.showerror("Error", "Password length must be greater than 6")
    elif not chk_phone:
        ms.showerror("Error", "Phone number must contain 10 digits.")
    else:
        ms.showinfo('Success!', 'Registration Successfull')
        # Create New Account
        insert = 'INSERT INTO taxidriver(driveremail,drivername,driverpassword,phone_number,licenseplate) VALUES(?,?,?,?,?)'
        c.execute(insert, [email, name, password, number, licenseplate])
        db.commit()
        c.close()
        driver_name_text.delete(0, END)
        driver_phone_text.delete(0, END)
        driver_email_text.delete(0, END)
        driver_password_text.delete(0, END)
        driver_license_text.delete(0, END)
        display_frames(driver_home_frame)


# name = "hari"
# password = "hari"
# new_taxi_driver(name, password)

# ********************* new admin ********************************
def new_admin(name, password):
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # Find Existing username if any take proper action
    find_user = ('SELECT * FROM admin WHERE username = ?')
    c.execute(find_user, [name])
    if c.fetchall():
        # just done
        c.close()
        a = 0
    else:

        # Create New Account
        insert = 'INSERT INTO admin(username,password) VALUES(?,?)'
        c.execute(insert, [name, password])
        db.commit()
        c.close()
        ms.showinfo('Success!', 'Account Created!')


name = "admin"
password = "admin"
new_admin(name, password)

# ******************* admin login *******************************

def admin_login():
    global adminname
    global adminpassword
    global seenusers
    seenusers = [" "]
    name = adminname.get()
    password = adminpassword.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # Find user If there is any take proper action
    find_user = ('SELECT * FROM admin WHERE username = ? and password = ?')
    c.execute(find_user, [name, password])
    result = c.fetchall()
    c.close()

    if adminname.get() == "" or adminpassword.get() == "":
        ms.showerror("Error", "Both fields required to fill")
    elif result:
        print("admin", name, " logged in")
        ms.showinfo("Success", "Login Successfull")
        view_admin_data()
        # admin_name_text.delete(0, END)
        # admin_password_text.delete(0, END)
        # admin_assign_page(admin_assign_frame)

    else:
        ms.showerror("Error", "Invalid username and password")

# ******************* user login *******************************


def user_login():
    global useremail
    global userpassword
    email = useremail.get()
    password = userpassword.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # Find user If there is any take proper action
    find_user = ('SELECT * FROM user WHERE useremail = ? and password = ?')
    c.execute(find_user, [email, password])
    result = c.fetchall()
    c.close()
    if useremail.get() == "" or userpassword.get() == "":
        ms.showerror("Error", "Both fields required to fill")
    elif result:
        print(email, "user logged in")
        ms.showinfo("Success", "Login Successfully")
        view_user_data()
        # customer_email_text.delete(0, END)
        customer_password_text.delete(0, END)
        # display_frames(customer_booking_frame)

    else:
        ms.showerror("Error", "Invalid email and password")


# name = "saroj"
# password = "saroj"
# user_login(name, password)

# ******************* driver login *******************************
def driver_login():
    global driveremail
    global driverpassword
    email = driveremail.get()
    password = driverpassword.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # Find user If there is any take proper action
    find_user = (
        'SELECT * FROM taxidriver WHERE driveremail = ? and driverpassword = ?')
    c.execute(find_user, [email, password])
    result = c.fetchall()
    c.close()
    if driveremail.get() == "" or driverpassword.get() == "":
        ms.showerror("Error", "Both fields required to fill")
    elif result:
        ms.showinfo("Success", "Login Successfully")
        view_driver_data()
        # driver_email_text.delete(0, END)
        driver_password_text.delete(0, END)

    else:
        ms.showerror("Error", "Invalid email and password")


# **************************user adds new destination*************************
def user_new_destination():
    global userdate
    global useremail
    global usertime
    global usercur_location
    global userdestination

    date = userdate.get()
    email = useremail.get()
    pickup_time = usertime.get()
    cur_loc = usercur_location.get()
    dest = userdestination.get()
    print("entered time:", pickup_time)
    print("email:", email)
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find userId
    find_userId = (
        'SELECT userId FROM user WHERE useremail = ?')
    c.execute(find_userId, [email])
    userid = c.fetchone()[0]
    print(userid)
    driverid = 0
    status = 'Pending'
    # Create New reservation
    if cur_loc == "" or dest == "" or pickup_time == "" or date == "":
        ms.showerror("Error", "All fields are required to fill")
    else:
        insert = 'INSERT INTO userReservation(date,cur_location,destination,pickup_time,status,userId,driverId) ' \
                 'VALUES(?,?,?,?,?,?,?)'
        c.execute(insert, [date, cur_loc, dest,
                           pickup_time, status, userid, driverid])
        db.commit()
        db.close()
        ms.showinfo('Success!', 'Regisration Successfull')

        # Deleting the text fields after reservation successfull
        # pick_text.delete(0, END)
        # drop_text.delete(0, END)
        # pick_time_text.delete(0, END)
        # d_entry.delete(0, END)

    view_user_data()

# date = "22/03/2021"
# username = "saroj"
# cur_loc = "thankot"
# destination = "kapilvastu"
# user_new_destination(username, date, cur_loc, destination)

# **************************** view user data *****************************


def view_user_data():
    global userdate
    global username
    global userphone_number
    global usercur_location
    global userdestination
    global assigneddriver
    global assigneddrivernumber
    global assignedtaxilicense
    global useremail
    global useraddress
    global userpayment
    global userstatus

    email = useremail.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find userId
    find_userId = ('SELECT * FROM user WHERE useremail = ?')
    c.execute(find_userId, [email])
    userdata = c.fetchall()
    print("user data: ", userdata)
    userid = userdata[0][0]
    username.set(userdata[0][3])
    userphone_number.set(userdata[0][5])
    print(userid)

    # find userReservation Data
    find_userdata = (
        'SELECT * FROM userReservation WHERE userId = ?')
    c.execute(find_userdata, [userid])
    userdata = c.fetchall()

    if userdata:
        print(userdata)
        userdate.set(userdata[0][0])
        usercur_location.set(userdata[0][1])
        userdestination.set(userdata[0][2])
        driverId = userdata[0][5]
        userstatus.set(userdata[0][6])
        if driverId != 0:
            # find drivername
            find_driver_name = (
                'SELECT * FROM taxidriver WHERE driverId = ?')
            c.execute(find_driver_name, [driverId])
            driverdata = c.fetchall()
            print("driver data:", driverdata)
            assigneddrivernumber.set(driverdata[0][4])
            assignedtaxilicense.set(driverdata[0][5])
            assigneddriver.set(driverdata[0][3])
        else:
            assigneddrivernumber.set(" ")
            assignedtaxilicense.set(" ")
            assigneddriver.set(" ")
        c.close()
        display_frames(customer_reserve_frame)

    else:
        c.close()
        display_frames(customer_booking_frame)


# username = "saroj"
# view_user_data(username)


# ******************************* update user status *************************
def update_user_status():
    global unassigned_userid
    global userstatus
    userid = unassigned_userid.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    status = "Accepted"
    update_userstatus = (
        'UPDATE userReservation SET status = ? WHERE userId = ?')
    c.execute(update_userstatus, [status, userid])

    db.commit()
    db.close()
    ms.showinfo('Success!', 'Status Changed!')
    userstatus.set('Accepted')
    admin_assign_frame_refresh()
    display_frames(admin_assign_frame)


# **************************** user deletes reservation *********************
def delete_user_reservation():
    global useremail
    email = useremail.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find userId
    find_userId = ('SELECT userId FROM user WHERE useremail = ?')
    c.execute(find_userId, [email])
    userid = c.fetchone()[0]

    # find driverId
    find_driverId = ('SELECT driverId FROM userReservation WHERE userId = ?')
    c.execute(find_driverId, [userid])
    driverid = c.fetchone()[0]

    if driverid != 0:
        # update  driverReservation table

        useridd = 0
        # update_drivertable = (
        #     'UPDATE driverReservation SET destination = ? WHERE driverId = ?')
        # c.execute(update_drivertable, [destination, driverid])
        update_drivertables = (
            'UPDATE driverReservation SET userId = ? WHERE driverId = ?')
        c.execute(update_drivertables, [useridd, driverid])

    # delete reservation
    delete_reservation = ('DELETE FROM userReservation WHERE userId = ?')
    c.execute(delete_reservation, [userid])
    db.commit()
    db.close()
    ms.showinfo('Success!', 'Reservation Deleted!')
    display_frames(customer_home_frame)


# **************************** driver deletes dateavailable *********************
def delete_driver_dateavailable():
    global driveremail
    email = driveremail.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find driverId
    find_driverId = ('SELECT driverId FROM taxidriver WHERE driveremail = ?')
    c.execute(find_driverId, [email])
    driverid = c.fetchone()[0]

    # find userId
    find_userId = ('SELECT userId FROM driverReservation WHERE driverId = ?')
    c.execute(find_userId, [driverid])
    userid = c.fetchone()[0]

    if userid != 0:
        # update  userReservation table
        driveridd = 0
        update_usertables = (
            'UPDATE userReservation SET driverId = ? WHERE userId = ?')
        c.execute(update_usertables, [driveridd, userid])

    # delete reservation
    delete_reservation = ('DELETE FROM driverReservation WHERE driverId = ?')
    c.execute(delete_reservation, [driverid])
    db.commit()
    db.close()
    ms.showinfo('Success!', 'Available Date Deleted!')
    display_frames(driver_home_frame)


# **************************driver adds data*************************
def driver_new_destination():
    # global driveravailabelDate

    global driveremail
    email = driveremail.get()

    # date = driveravailabelDate.get()
    date = ''

    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find driverId
    find_driverId = (
        'SELECT driverId FROM taxidriver WHERE driveremail = ?')
    c.execute(find_driverId, [email])
    driverid = c.fetchone()[0]
    print(driverid)
    userid = 0

    # Create New reservation
    inserts = 'INSERT INTO driverReservation(availabelDate,driverId,userId) VALUES(?,?,?)'
    c.execute(inserts, [date, driverid, userid])
    db.commit()
    db.close()
    ms.showinfo('Success!', 'Information Updated!')
    view_driver_data()


# date = "12/12/12"
# username = "samir"
# driver_new_destination(username, date)

# **************************** view driver data *****************************
def view_driver_data():
    global drivername
    global driverpassword
    global driveravailabelDate
    global driverphone_number
    global driverlicenseplate
    global assigneduser
    global driveremail
    global assignedusernumber
    global assigneduserlocation
    global assignedusertime
    global assigneduserdestination

    email = driveremail.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find driverId
    find_driverId = (
        'SELECT * FROM taxidriver WHERE driveremail = ?')
    c.execute(find_driverId, [email])
    driverdata = c.fetchall()
    driverid = driverdata[0][0]
    drivername.set(driverdata[0][3])
    driverphone_number.set(driverdata[0][4])
    driverlicenseplate.set(driverdata[0][5])
    print(driverid)
    # find driverReservation Data
    find_driverdata = (
        'SELECT * FROM driverReservation WHERE driverId = ?')
    c.execute(find_driverdata, [driverid])
    driverdata = c.fetchall()
    print("driverdata:", driverdata)

    if driverdata:

        driveravailabelDate.set(driverdata[0][0])

        userId = driverdata[0][2]
        if userId != 0:
            # find username
            find_user_name = (
                'SELECT username FROM user WHERE userId = ?')
            c.execute(find_user_name, [userId])
            user_name = c.fetchone()[0]
            print(user_name)
            assigneduser.set(user_name)
            # find usernumber
            find_user_number = (
                'SELECT phone_number FROM user WHERE userId = ?')
            c.execute(find_user_number, [userId])
            user_number = c.fetchone()[0]
            print(user_number)
            assignedusernumber.set(user_number)
            # find useraddress
            find_user_address = (
                'SELECT useraddress FROM user WHERE userId = ?')
            c.execute(find_user_address, [userId])
            user_address = c.fetchone()[0]
            print(user_address)
            assigneduserlocation.set(user_address)
            # find pickup time
            find_user_time = (
                'SELECT pickup_time FROM userReservation WHERE userId = ?')
            c.execute(find_user_time, [userId])
            user_time = c.fetchone()[0]
            print(user_time)
            assignedusertime.set(user_time)
            # find dropoff address
            find_drop_addr = (
                'SELECT destination FROM userReservation WHERE userId = ?')
            c.execute(find_drop_addr, [userId])
            dropoff_addr = c.fetchone()[0]
            print(dropoff_addr)
            assigneduserdestination.set(dropoff_addr)
        else:
            assigneduser.set(" ")
            assignedusernumber.set(" ")
            assigneduserlocation.set(" ")
            assignedusertime.set(" ")
            assigneduserdestination.set(" ")
        c.close()
        display_frames(driver_reserve_frame)

    else:
        c.close()
        # display_frames(driver_reserve_frame)
        display_frames(driver_dataupdate_frame)


# drivername = "samir"
# view_driver_data(drivername)


# **************************** show suitable drivers *****************************
def show_suitable_drivers(date):
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find driverId
    find_driverId = (
        'SELECT driverId FROM driverReservation WHERE availabelDate = ?')
    c.execute(find_driverId, [date])
    driverid = c.fetchall()
    for each in driverid:
        # print(each[0])
        driveriid = each[0]
        # find driverReservation Data
        find_driverdata = (
            'SELECT * FROM driverReservation WHERE driverId = ?')
        c.execute(find_driverdata, [driveriid])
        driverdata = c.fetchall()
        print("suitable driver:", driverdata)
    c.close()


# date = "12/12/12"
# show_suitable_drivers(date)

# *********************************** view admin data *****************************************
def view_admin_data():
    global unassigned_username
    global unassigned_date
    global selected_drivername
    global drivers_names
    global selected_drivername
    global unassigned_userid
    global userstatus
    global seenusers
    global unseenusers
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

    # find destination for single user
    drid = 0
    find_users = ('SELECT * FROM userReservation WHERE driverId = ?')
    c.execute(find_users, [drid])
    users = c.fetchall()

    if users:
        user = ()
        print("unassigned users", users)

        if len(seenusers) <= 1:
            user = users[0]

        # print(len(seenusers))
        for usr in users:
            print("seenusers:", seenusers)
            print(usr in seenusers)
            if (usr in seenusers) == FALSE:
                seenusers.append(usr)
                user = usr
                break

        # filter seen and unseen users and set variables to new / next user here
        # global drivers
        if user:

            unassigned_date.set(user[0])
            usrid = user[4]
            unassigned_userid.set(usrid)
            date = user[0]
            userstatus.set(user[6])
            find_username = ('SELECT username FROM user WHERE userId = ?')
            c.execute(find_username, [usrid])
            name = c.fetchone()
            # print("admin -> name:", name)
            unassigned_username.set(name[0])

            # select drivers
            usridd = 0
            driverID = 0
            drivers_names = [" "]
            # drivers_dicts = {}
            find_drivers = (
                'SELECT driverId FROM driverReservation WHERE userId = ?')
            c.execute(find_drivers, [usridd])
            drivers = c.fetchall()

            if drivers:
                for driverID in drivers:
                    # find_driver = (
                    #     'SELECT driverId FROM driverReservation WHERE driverId = ? AND availabelDate = ?')
                    # c.execute(find_driver, [drid[0], date])
                    # driverID = c.fetchone()
                    # if driverID:
                    find_drivername = (
                        'SELECT drivername FROM taxidriver WHERE driverId = ?')
                    c.execute(find_drivername, [driverID[0]])
                    driver = c.fetchone()
                    # drivers_dicts[drid[0]] = driver
                    drivers_names.append(driver[0])
                    print("drivers names: ", drivers_names)
                    admin_assign_frame_refresh()
                    display_frames(admin_assign_frame)

                    # else:
                    #     display_frames(admin_assign_nodriver_frame)
            else:
                display_frames(admin_assign_nodriver_frame)
        else:
            ms.showinfo('Error!', 'No Next User Found!')
    else:
        display_frames(admin_assign_nouser_frame)

    # display_frames(admin_signin_frame)

# ***********************************admin assigns driver to the user***************************


def assign_destination():
    global selected_drivername
    # global selected_driverid
    global unassigned_userid

    userid = unassigned_userid.get()
    drname = selected_drivername.get()
    # Establish Connection
    with sqlite3.connect('database.db') as db:
        c = db.cursor()
    # find driverId
    find_driverid = (
        'SELECT driverId FROM taxidriver WHERE drivername = ?')
    c.execute(find_driverid, [drname])
    driverid = c.fetchone()[0]

    # update driverId in userReservation table
    update_driverId = (
        'UPDATE userReservation SET driverId = ? WHERE userId = ?')
    c.execute(update_driverId, [driverid, userid])

    # update  driverReservation table
    # update_drivertable = (
    #     'UPDATE driverReservation SET destination = ? WHERE driverId = ?')
    # c.execute(update_drivertable, [destination, driverid])
    update_drivertables = (
        'UPDATE driverReservation SET userId = ? WHERE driverId = ?')
    c.execute(update_drivertables, [userid, driverid])

    db.commit()
    c.close()
    ms.showinfo('Success!', 'Driver Assigned!')

    # admin_assign_frame_refresh()
    view_admin_data()


# uid = 1
# did = 1
# assign_destination(uid, did)


# ******************************************************GUI Using Tkinter********************************


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Driver Part >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Driver registration function
def driver_registration_page(frame):
    global driveremail
    global driverpassword
    global drivername
    global driverlicenseplate
    global driverphone_number

    global driver_name_text
    global driver_phone_text
    global driver_email_text
    global driver_license_text
    global driver_password_text

    d_frame = Frame(frame, bd=2, relief=GROOVE)
    d_frame.place(x=175, y=55, width=500, height=430)

    # label
    label_registration = Label(d_frame, text="Registration Form", bg="green", font=(
        "times", 20, "bold")).pack(side=TOP, fill=X)
    name_label = Label(d_frame, text="Full Name", font=(
        "times", 15, "bold")).place(x=35, y=100)
    phone_label = Label(d_frame, text="Phone Number", font=(
        "times", 15, "bold")).place(x=35, y=140)
    license_label = Label(d_frame, text="License Plate", font=(
        "times", 15, "bold")).place(x=35, y=180)
    email_label = Label(d_frame, text="Email", font=(
        "times", 15, "bold")).place(x=35, y=220)
    password_label = Label(d_frame, text="Password", font=(
        "times", 15, "bold")).place(x=35, y=260)

    # Text
    driver_name_text = Entry(
        d_frame, textvariable=drivername, bd=2, relief=GROOVE, width=30, font=("", 12))
    driver_name_text.place(x=195, y=100, height=33)

    driver_phone_text = Entry(d_frame, textvariable=driverphone_number, bd=2, relief=GROOVE, width=30,
                              font=("", 12))
    driver_phone_text.place(x=195, y=140, height=33)

    driver_license_text = Entry(d_frame, textvariable=driverlicenseplate, bd=2, relief=GROOVE, width=30,
                                font=("", 12))
    driver_license_text.place(x=195, y=180, height=33)

    driver_email_text = Entry(d_frame, textvariable=driveremail, bd=2, relief=GROOVE, width=30,
                              font=("", 12))
    driver_email_text.place(x=195, y=220, height=33)

    driver_password_text = Entry(d_frame, textvariable=driverpassword, bd=2, show="*", relief=GROOVE, width=30,
                                 font=("", 12))
    driver_password_text.place(x=195, y=260, height=33)

    # Button
    submit_button = Button(d_frame, text="Submit", bd=1,
                           width=10, height=1, command=new_taxi_driver, font=("times", 15, "bold"))
    submit_button.place(x=130, y=345)

    exit_button = Button(d_frame, text="Exit", bd=1, width=10, height=1,
                         command=lambda: display_frames(home_frame), font=("times", 15, "bold"))
    exit_button.place(x=280, y=345)


# Driver home page function
def driver_home_page(frame):
    global driveremail
    global driverpassword

    global driver_email_text
    global driver_password_text

    frame2 = Frame(frame, relief=GROOVE, bd=3)
    frame2.place(x=180, y=70, width=530, height=480)

    login_label = Label(frame2, text="Driver Login system",
                        font=("times", 25, "bold")).place(x=110, y=75)
    name_label = Label(frame2, text="Email", font=(
        "times", 18, "bold")).place(x=30, y=210)
    password_label = Label(frame2, text="Password", font=(
        "times", 18, "bold")).place(x=30, y=260)

    # Text field
    driver_email_text = Entry(
        frame2, bd=2, width=30, textvariable=driveremail, relief=GROOVE, font=("", 12))
    driver_email_text.place(x=170, y=210, width=270, height=35)

    driver_password_text = Entry(
        frame2, bd=2, width=30, textvariable=driverpassword, show="*", relief=GROOVE, font=("", 12))
    driver_password_text.place(x=170, y=260, width=270, height=35)

    button_login = Button(frame2, text="Login", relief=GROOVE,
                          bd=2, fg="blue", width=18, command=driver_login, font=("times", 18, "bold"))
    button_login.place(x=170, y=350)
    button_register = Button(frame2, text="Signup", relief=GROOVE, bd=2, fg="green", width=18,
                             command=lambda: display_frames(driver_registration_frame), font=("times", 18, "bold"))
    button_register.place(x=170, y=400)
    button_back = Button(frame2, text="Back", relief=GROOVE, bd=2,
                         command=lambda: display_frames(home_frame), font=("times", 18, "bold"))
    button_back.grid(row=0, column=0, sticky="nw")


# Define a function customer booking page
def driver_dataupdate_page(frame):
    global driveravailabelDate

    f_login = Frame(frame, relief=GROOVE, bd=2)
    f_login.place(x=180, y=30, width=570, height=570)

    book_label = Label(f_login, text="Driver Panel",
                       relief=GROOVE, bg="blue", font=("times", 25, "bold"))
    book_label.pack(side=TOP, fill=X)

    date_label = Label(
        f_login, text="Click If You Are Available", font=("times", 18, "bold"))
    date_label.place(x=150, y=200)

    s1_button = Button(f_login, width=15, text="I'm Available",
                       command=driver_new_destination, font=("times", 15, "bold"))
    s1_button.place(x=150, y=270)

    s4_button = Button(f_login, text="Exit", width=7, command=lambda: display_frames(
        home_frame), font=("times", 15, "bold"))
    s4_button.place(x=410, y=470)

# Define a function driver reserve page


def driver_reserved_page(frame):
    global drivername
    global driveremail
    global driverphone_number
    global driverlicenseplate
    global driveravailabelDate
    global assigneduser
    global assignedusernumber
    global assigneduserlocation
    global assigneduserdestination
    global assignedusertime

    print("time:", assignedusertime.get())
    f_login = Frame(frame, relief=GROOVE, bd=2)
    f_login.place(x=180, y=30, width=570, height=570)

    book_label = Label(f_login, text="Trip Information",
                       relief=GROOVE, bg="blue", font=("times", 25, "bold"))
    book_label.pack(side=TOP, fill=X)

    name_label = Label(f_login, text="FullName: ", font=("times", 15, "bold"))
    name_label.place(x=5, y=75)

    name_text = Label(f_login, textvariable=drivername,
                      font=("times", 15, "bold"))
    name_text.place(x=200, y=75)

    phone_label = Label(f_login, text="My Number: ",
                        font=("times", 15, "bold"))
    phone_label.place(x=5, y=100)

    phone_text = Label(f_login, textvariable=driverphone_number,
                       font=("times", 15, "bold"))
    phone_text.place(x=200, y=100)

    usrphone_label = Label(f_login, text="Customer Name: ",
                           font=("times", 15, "bold"))
    usrphone_label.place(x=5, y=125)

    usrphone_text = Label(f_login, textvariable=assigneduser,
                          font=("times", 15, "bold"))
    usrphone_text.place(x=200, y=125)

    licenseplate_label = Label(
        f_login, text="Customer Phone:", font=("times", 15, "bold"))
    licenseplate_label.place(x=5, y=150)

    licenseplate_text = Label(
        f_login, textvariable=assignedusernumber, font=("times", 15, "bold"))
    licenseplate_text.place(x=200, y=150)

    pickup_label = Label(f_login, text="Pick-Up Address:",
                         font=("times", 15, "bold"))
    pickup_label.place(x=5, y=175)

    pickup_text = Label(
        f_login, textvariable=assigneduserlocation, font=("times", 15, "bold"))
    pickup_text.place(x=200, y=175)

    pickup_time_label = Label(
        f_login, text="Pick-Up Time:", font=("times", 15, "bold"))
    pickup_time_label.place(x=5, y=200)

    pickup_time_text = Label(
        f_login, textvariable=assignedusertime, font=("times", 15, "bold"))
    pickup_time_text.place(x=200, y=200)

    dropaddr_label = Label(
        f_login, text="Drop-Off Address:", font=("times", 15, "bold"))
    dropaddr_label.place(x=5, y=225)

    dropaddr_text = Label(
        f_login, textvariable=assigneduserdestination, font=("times", 15, "bold"))
    dropaddr_text.place(x=200, y=225)

    driver_label = Label(f_login, text="License Plate No.:",
                         font=("times", 15, "bold"))
    driver_label.place(x=5, y=275)

    driver_text = Label(
        f_login, textvariable=driverlicenseplate, font=("times", 15, "bold"))
    driver_text.place(x=200, y=275)

    s3_button = Button(f_login, text="Cancel", width=10,
                       command=delete_driver_dateavailable, font=("times", 15, "bold"))
    s3_button.place(x=250, y=470)

    s4_button = Button(f_login, text="Exit", width=7, command=lambda: display_frames(
        home_frame), font=("times", 15, "bold"))
    s4_button.place(x=410, y=470)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Customer Part >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Define a function customer registration page


def customer_registration_page(frame):
    global username
    global useremail
    global userpassword
    global userphone_number
    global useraddress
    global userpayment
    global useraccoutno
    global usercvvnumber

    global customer_name_text
    global customer_phone_text
    global customer_address_text
    global customer_email_text
    global customer_password_text
    global customer_payment_text
    global customer_accountno_text
    global customer_cardcvv_text

    # Creating a new frame inside frame
    frame3 = Frame(frame, relief=GROOVE, bd=3)
    frame3.place(x=180, y=50, width=530, height=500)

    # Label
    register_label = Label(frame3, text="Registration Panel", bg="green", font=(
        "times", 20, "bold")).pack(side=TOP, fill=X)
    customer_name_label = Label(frame3, text="Full Name", font=(
        "times", 15, "bold")).place(x=50, y=100)
    customer_phone_label = Label(frame3, text="Phone Number", font=(
        "times", 15, "bold")).place(x=50, y=140)
    customer_address_label = Label(frame3, text="Address", font=(
        "times", 15, "bold")).place(x=50, y=180)
    customer_email_label = Label(frame3, text="Email", font=(
        "times", 15, "bold")).place(x=50, y=220)
    customer_password_label = Label(frame3, text="Password", font=(
        "times", 15, "bold")).place(x=50, y=260)

    customer_payment_label = Label(frame3, text="Payment Method", font=(
        "times", 15, "bold")).place(x=50, y=300)

    customer_accountno_label = Label(frame3, text="Card Number", font=(
        "times", 15, "bold")).place(x=50, y=340)
    customer_cardcvv_label = Label(frame3, text="CVV Number", font=(
        "times", 15, "bold",)).place(x=50, y=380)

    # Text
    customer_name_text = Entry(frame3, textvariable=username,
                               bd=2, relief=GROOVE, bg="white", width=30, font=("", 12))
    customer_name_text.place(x=225, y=100, height=33)

    customer_phone_text = Entry(frame3, textvariable=userphone_number, bd=2, relief=GROOVE, bg="white", width=30,
                                font=("", 12))
    customer_phone_text.place(x=225, y=140, height=33)

    customer_address_text = Entry(frame3, textvariable=useraddress, bd=2, relief=GROOVE, bg="white", width=30,
                                  font=("", 12))
    customer_address_text.place(x=225, y=180, height=33)

    customer_email_text = Entry(frame3, textvariable=useremail, bd=2, relief=GROOVE, bg="white", width=30,
                                font=("", 12))
    customer_email_text.place(x=225, y=220, height=33)

    customer_password_text = Entry(frame3, textvariable=userpassword, bd=2, show="*", relief=GROOVE, bg="white", width=30,
                                   font=("", 12))

    customer_password_text.place(x=225, y=260, height=33)

    customer_payment_text = Combobox(
        frame3, width=20, textvariable=userpayment)
    customer_payment_text['values'] = ("Credit Card", "Master Card", "Pay Pal")
    customer_payment_text.place(x=225, y=300, height=33)

    customer_accountno_text = Entry(frame3, textvariable=useraccountno, bd=2, relief=GROOVE, bg="white", width=30,
                                    font=("", 12))
    customer_accountno_text.place(x=225, y=340, height=33)
    customer_cardcvv_text = Entry(frame3, textvariable=usercvvnumber, bd=2, relief=GROOVE, bg="white", width=30,
                                  font=("", 12))
    customer_cardcvv_text.place(x=225, y=380, height=33)

    # Button
    button_submit = Button(frame3, text="Submit", width=8, height=1, relief=GROOVE, command=new_user,
                           font=("times", 15, "bold"))

    button_submit.place(x=195, y=450)

    button_exit = Button(frame3, text="Exit", width=8, height=1, relief=GROOVE,
                         command=lambda: display_frames(customer_home_frame), font=("times", 15, "bold"))
    button_exit.place(x=350, y=450)


# Define a function customer home page
def customer_home_page(frame):
    global useremail
    global userpassword

    global customer_email_text
    global customer_password_text

    # Create a new frame inside frame
    frame2 = Frame(frame, relief=GROOVE, bd=3)
    frame2.place(x=180, y=70, width=530, height=480)

    # Label
    login_label = Label(frame2, text="Customer Login system",
                        font=("times", 25, "bold")).place(x=110, y=75)
    name_label = Label(frame2, text="Email", font=(
        "times", 18, "bold")).place(x=30, y=210)
    password_label = Label(frame2, text="Password", font=(
        "times", 18, "bold")).place(x=30, y=260)

    # Text field
    customer_email_text = Entry(
        frame2, bd=2, width=30, textvariable=useremail, relief=GROOVE, font=("", 12))
    customer_email_text.place(x=170, y=210, width=270, height=35)

    customer_password_text = Entry(
        frame2, bd=2, width=30, textvariable=userpassword, show="*", relief=GROOVE, font=("", 12))
    customer_password_text.place(x=170, y=260, width=270, height=35)

    # Button
    button_login = Button(frame2, text="Login", relief=GROOVE, bd=2, fg="blue",
                          width=18, command=user_login, font=("times", 18, "bold"))
    button_login.place(x=170, y=350)

    button_register = Button(frame2, text="Signup", relief=GROOVE, bd=2, fg="green", width=18,
                             command=lambda: display_frames(customer_registration_frame), font=("times", 18, "bold"))
    button_register.place(x=170, y=400)

    button_back = Button(frame2, text="Back", relief=GROOVE, bd=2,
                         command=lambda: display_frames(home_frame), font=("times", 18, "bold"))
    button_back.grid(row=0, column=0, sticky="nw")


# Define a function customer booking page
def customer_booking_page(frame):
    global userdate
    global usercur_location
    global userdestination
    global usertime

    global pick_text
    global drop_text
    global pick_time_text
    global d_entry

    f_login = Frame(frame, relief=GROOVE, bd=2)
    f_login.place(x=180, y=30, width=570, height=570)

    book_label = Label(f_login, text="Booking Page",
                       relief=GROOVE, bg="blue", font=("times", 25, "bold"))
    book_label.pack(side=TOP, fill=X)
    pick_label = Label(f_login, text="Pick-Up Address",
                       font=("times", 18, "bold"))
    pick_label.place(x=5, y=100)
    drop_label = Label(f_login, text="Drop-Off Address",
                       font=("times", 18, "bold"))
    drop_label.place(x=5, y=150)

    pick_time_label = Label(f_login, text="Pick-Up Time",
                            font=("times", 18, "bold"))
    pick_time_label.place(x=5, y=200)

    date_label = Label(f_login, text="Pick-Up Date",
                       font=("times", 18, "bold"))
    date_label.place(x=5, y=250)

    pick_text = Entry(f_login, bd=2, width=30,
                      textvariable=usercur_location, relief=GROOVE, font=("", 12))
    pick_text.place(x=240, y=100, height=35)
    drop_text = Entry(f_login, bd=2, width=30,
                      textvariable=userdestination, relief=GROOVE, font=("", 12))
    drop_text.place(x=240, y=150, height=35)
    pick_time_text = Entry(f_login, bd=2, width=15,
                           textvariable=usertime, relief=GROOVE, font=("", 12))
    pick_time_text.place(x=240, y=200, height=35)

    x = datetime.datetime.now()
    d_entry = DateEntry(f_login, bd=2, width=15, year=x.year,
                        month=x.month, day=x.day, textvariable=userdate, font=("", 12))

    d_entry.delete(0, END)
    d_entry.place(x=240, y=250, height=35)

    # Button
    s1_button = Button(f_login, width=7, text="Reserve",
                       command=user_new_destination, font=("times", 15, "bold"))
    s1_button.place(x=250, y=340)

    s4_button = Button(f_login, text="Exit", width=7, command=lambda: display_frames(
        home_frame), font=("times", 15, "bold"))
    s4_button.place(x=410, y=340)


# Define a function customer reserved page
def customer_reserved_page(frame):
    global userdate
    global username
    global userphone_number
    global usercur_location
    global userdestination
    global assigneddriver
    global assigneddrivernumber
    global assignedtaxilicense
    global usertime
    global userstatus

    f_login = Frame(frame, relief=GROOVE, bd=2)
    f_login.place(x=180, y=30, width=570, height=570)

    book_label = Label(f_login, text="Booking Information",
                       relief=GROOVE, bg="blue", font=("times", 25, "bold"))
    book_label.pack(side=TOP, fill=X)

    name_label = Label(f_login, text="FullName: ", font=("times", 15, "bold"))
    name_label.place(x=5, y=100)

    name_text = Label(f_login, textvariable=username,
                      font=("times", 15, "bold"))
    name_text.place(x=240, y=100)

    phone_label = Label(f_login, text="Phone Number: ",
                        font=("times", 15, "bold"))
    phone_label.place(x=5, y=125)

    phone_text = Label(f_login, textvariable=userphone_number,
                       font=("times", 15, "bold"))
    phone_text.place(x=240, y=125)

    pick_label = Label(f_login, text="Pick-Up Address: ",
                       font=("times", 15, "bold"))
    pick_label.place(x=5, y=150)

    pick_text = Label(f_login, textvariable=usercur_location,
                      font=("times", 15, "bold"))
    pick_text.place(x=240, y=150)

    drop_label = Label(f_login, text="Drop-Off Address:",
                       font=("times", 15, "bold"))
    drop_label.place(x=5, y=175)

    drop_text = Label(f_login, textvariable=userdestination,
                      font=("times", 15, "bold"))
    drop_text.place(x=240, y=175)

    date_label = Label(f_login, text="Pick-Up Date:",
                       font=("times", 15, "bold"))
    date_label.place(x=5, y=200)

    date_text = Label(f_login, textvariable=userdate,
                      font=("times", 15, "bold"))
    date_text.place(x=240, y=200)

    driver_label = Label(f_login, text="Driver Name:",
                         font=("times", 15, "bold"))
    driver_label.place(x=5, y=225)

    driver_text = Label(f_login, textvariable=assigneddriver,
                        font=("times", 15, "bold"))
    driver_text.place(x=240, y=225)

    driver_label = Label(f_login, text="Driver Phone:",
                         font=("times", 15, "bold"))
    driver_label.place(x=5, y=250)

    driver_text = Label(
        f_login, textvariable=assigneddrivernumber, font=("times", 15, "bold"))
    driver_text.place(x=240, y=250)

    driver_label = Label(f_login, text="Taxi License:",
                         font=("times", 15, "bold"))
    driver_label.place(x=5, y=275)

    driver_text = Label(
        f_login, textvariable=assignedtaxilicense, font=("times", 15, "bold"))
    driver_text.place(x=240, y=275)

    driver_time = Label(f_login, text="Pick-Up Time:",
                        font=("times", 15, "bold"))
    driver_time.place(x=5, y=300)

    driver_time = Label(f_login, textvariable=usertime,
                        font=("times", 15, "bold"))
    driver_time.place(x=240, y=300)

    user_status = Label(f_login, text="Booking Status:",
                        font=("times", 15, "bold"))
    user_status.place(x=5, y=325)

    user_status = Label(f_login, textvariable=userstatus,
                        font=("times", 15, "bold"))
    user_status.place(x=240, y=325)

    # Buttons
    s3_button = Button(f_login, text="Cancel", width=10,
                       command=delete_user_reservation, font=("times", 15, "bold"))
    s3_button.place(x=250, y=470)

    s4_button = Button(f_login, text="Exit", width=7, command=lambda: display_frames(
        home_frame), font=("times", 15, "bold"))
    s4_button.place(x=410, y=470)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Admin Part >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# admin signin page


def admin_signin_page(frame):
    global adminname
    global adminpassword

    global admin_name_text
    global admin_password_text
    # load = Image.open("Images\\login.png")
    # ren = ImageTk.PhotoImage(load)
    # img = Label(root, image=ren)
    # img.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a new frame inside frame
    frame2 = Frame(frame, relief=GROOVE, bd=3)
    frame2.place(x=180, y=70, width=530, height=480)

    # Label
    login_label = Label(frame2, text="Admin Login system",
                        font=("times", 25, "bold"))
    login_label.place(x=110, y=75)

    name_label = Label(frame2, text="User Name", font=("times", 18, "bold"))
    name_label.place(x=30, y=210)

    password_label = Label(frame2, text="Password", font=("times", 18, "bold"))
    password_label.place(x=30, y=260)

    # Entry
    admin_name_text = Entry(frame2, bd=2, width=28,
                            textvariable=adminname, relief=GROOVE, font=("", 12))
    admin_name_text.place(x=170, y=210, width=270, height=35)

    admin_password_text = Entry(frame2, bd=2, width=28,
                                textvariable=adminpassword, show="*", relief=GROOVE, font=("", 12))
    admin_password_text.place(x=170, y=260, width=270, height=35)

    # Button
    button_login = Button(frame2, text="Login", relief=GROOVE, bd=2, fg="blue",
                          width=18, command=admin_login, font=("times", 18, "bold"))
    button_login.place(x=170, y=350)

    button_back = Button(frame2, text="Back", relief=GROOVE, bd=2,
                         command=lambda: display_frames(home_frame), font=("times", 18, "bold"))
    button_back.grid(row=0, column=0, sticky="nw")


# refresh admin frame
def admin_assign_frame_refresh():
    global admin_assign_frame
    global root
    admin_assign_frame.destroy()
    admin_assign_frame = tk.Frame(root)
    admin_assign_frame.grid(row=0, column=0, sticky="nsew")
    admin_assign_page(admin_assign_frame)


# admin assign page

def admin_assign_page(frame):
    global unassigned_username
    global unassigned_date
    global selected_drivername
    global drivers_names
    global userstatus
    f_login = Frame(frame, relief=GROOVE, bd=2)
    f_login.place(x=180, y=30, width=570, height=570)

    book_label = Label(f_login, text="Admin Page",
                       relief=GROOVE, bg="blue", font=("times", 25, "bold"))
    book_label.pack(side=TOP, fill=X)
    y1 = 80
    name_label = Label(f_login, text="Customer Name: ",
                       font=("times", 15, "bold"))
    name_label.place(x=5, y=y1)
    name_text = Label(f_login, textvariable=unassigned_username,
                      font=("times", 15, "bold"))
    name_text.place(x=170, y=y1)

    date_label = Label(f_login, text="Date:",
                       font=("times", 15, "bold"))
    date_label.place(x=5, y=y1+50)
    date_text = Label(f_login, textvariable=unassigned_date,
                      font=("times", 15, "bold"))
    date_text.place(x=170, y=y1+50)

    user_status = Label(f_login, text="Status:",
                        font=("times", 15, "bold"))
    user_status.place(x=5, y=y1+100)
    user_status = Label(f_login, textvariable=userstatus,
                        font=("times", 15, "bold"))
    user_status.place(x=170, y=y1+100)

    driver_label = Label(f_login, text="Available Drivers:",
                         font=("times", 15, "bold"))
    driver_label.place(x=5, y=y1+200)
    driver_combo = ttk.Combobox(f_login, textvariable=selected_drivername,
                                state='readonly', font=('arial', 20, 'bold'), width=11)
    driver_combo['value'] = drivers_names
    driver_combo.current(0)
    driver_combo.place(x=190, y=y1+200)

    # Button
    s3_button = Button(f_login, text="Assign Driver", width=12, command=assign_destination,
                       font=("times", 15, "bold"))
    s3_button.place(x=10, y=y1+300)

    s2_button = Button(f_login, text="Accept Request", width=12, command=update_user_status,
                       font=("times", 15, "bold"))
    s2_button.place(x=170, y=y1+300)

    s5_button = Button(f_login, text="Next User", width=10, command=view_admin_data,
                       font=("times", 15, "bold"))
    s5_button.place(x=330, y=y1+300)
    s4_button = Button(f_login, text="Exit", width=7, command=lambda: display_frames(
        home_frame), font=("times", 15, "bold"))
    s4_button.place(x=460, y=y1+300)

# admin nodriver assign page


def admin_assign_nodriver_page(frame):
    global unassigned_username
    global unassigned_date
    global userstatus

    f_login = Frame(frame, relief=GROOVE, bd=2)
    f_login.place(x=180, y=30, width=570, height=570)

    book_label = Label(f_login, text="Admin Page",
                       relief=GROOVE, bg="blue", font=("times", 25, "bold"))
    book_label.pack(side=TOP, fill=X)
    y1 = 80
    name_label = Label(f_login, text="Customer Name:",
                       font=("times", 15, "bold"))
    name_label.place(x=5, y=y1)
    name_text = Label(f_login, textvariable=unassigned_username,
                      font=("times", 15, "bold"))
    name_text.place(x=170, y=y1)

    date_label = Label(f_login, text="Date:",
                       font=("times", 15, "bold"))
    date_label.place(x=5, y=y1+50)
    date_text = Label(f_login, textvariable=unassigned_date,
                      font=("times", 15, "bold"))
    date_text.place(x=170, y=y1+50)

    user_status = Label(f_login, text="Status:",
                        font=("times", 15, "bold"))
    user_status.place(x=5, y=y1+100)
    user_status = Label(f_login, textvariable=userstatus,
                        font=("times", 15, "bold"))
    user_status.place(x=170, y=y1+100)

    s2_button = Button(f_login, text="Confirm", width=10, command=update_user_status,
                       font=("times", 15, "bold"))
    s2_button.place(x=160, y=y1+200)

    name_label = Label(f_login, text="No Driver Available",
                       font=("times", 20, "bold"))
    name_label.place(x=5, y=y1+320)
    s4_button = Button(f_login, text="Exit", width=7, command=lambda: display_frames(
        home_frame), font=("times", 15, "bold"))
    s4_button.place(x=410, y=470)


# admin nouser assign page
def admin_assign_nouser_page(frame):
    f_login = Frame(frame, relief=GROOVE, bd=2)
    f_login.place(x=180, y=30, width=570, height=570)

    book_label = Label(f_login, text="Admin Page",
                       relief=GROOVE, bg="blue", font=("times", 25, "bold"))
    book_label.pack(side=TOP, fill=X)

    name_label = Label(f_login, text="No New User To Be Assigned Driver",
                       font=("times", 20, "bold"))
    name_label.place(x=5, y=200)

    s4_button = Button(f_login, text="Exit", width=7, command=lambda: display_frames(
        home_frame), font=("times", 15, "bold"))
    s4_button.place(x=410, y=470)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Home Page >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Define  home page function


def home_page(frame):
    frame1 = Frame(frame, bd=2, relief=GROOVE)
    frame1.place(x=180, y=60, width=530, height=480)

    # Create a label taxi booking system
    label1 = Label(frame1, text="Taxi Booking System", bd=4, bg="blue", font=(
        "times", 20, "bold"), relief=SUNKEN, height=2)
    label1.pack(side=TOP, fill=X)

    # create a button admin, customer and driver
    button_admin = Button(frame1, text="Admin", bd=2, height=1,
                          width=20, bg="red", command=lambda: display_frames(admin_signin_frame), font=("times", 20, "bold"))
    button_admin.pack(pady=20)

    button_customer = Button(frame1, text="Customer", bd=2, height=1, width=20, bg="green",
                             command=lambda: display_frames(customer_home_frame), font=("times", 20, "bold"))
    button_customer.pack()

    button_driver = Button(frame1, text="Driver", bd=2, height=1, width=20, command=lambda: display_frames(
        driver_home_frame), bg="yellow", font=("times", 20, "bold"))
    button_driver.pack(pady=20)

    button_exit = Button(frame1, text="Quit", bd=2, height=1, width=20,
                         command=lambda: root.destroy(), bg="yellow", font=("times", 20, "bold"))
    button_exit.pack(pady=30)


# Creating a new window
root = tk.Tk()

root.title("Taxi Login System")
# root.state("zoomed")
root.geometry("850x650+250+20")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.configure(bg="lightblue")
root.resizable(False, False)

# Global variables of admin
adminname = StringVar()
adminpassword = StringVar()

unassigned_username = StringVar()
unassigned_date = StringVar()
selected_drivername = StringVar()
drivers_names = [" "]
# drivers = []
selected_drivername = StringVar()
unassigned_userid = IntVar()

seenusers = [" "]
unseenusers = [" "]
unassigned_user_names = [" "]

# Global variables of customers
useremail = StringVar()
username = StringVar()
userpassword = StringVar()
useraddress = StringVar()
userpayment = StringVar()
useraccountno = StringVar()
userphone_number = StringVar()
usercvvnumber = StringVar()
usercur_location = StringVar()
userdestination = StringVar()
userdate = StringVar()
usertime = StringVar()
assigneddriver = StringVar()
assigneddrivernumber = StringVar()
assignedtaxilicense = StringVar()
userstatus = StringVar()

# Global variables of drivers
driveremail = StringVar()
drivername = StringVar()
driverpassword = StringVar()
driverlicenseplate = StringVar()

driveravailabelDate = StringVar()
driverphone_number = StringVar()
assigneduser = StringVar()
assignedusernumber = StringVar()
assigneduserlocation = StringVar()
assignedusertime = StringVar()
assigneduserdestination = StringVar()

# Frames for customer, driver and admin system
home_frame = tk.Frame(root, bg="red")
# admin_login_frame = tk.Frame(root, bg="lightblue")
customer_home_frame = tk.Frame(root, bg="green")
driver_home_frame = tk.Frame(root, bg="blue")

admin_signin_frame = tk.Frame(root)
customer_registration_frame = tk.Frame(root)
customer_booking_frame = tk.Frame(root)
customer_reserve_frame = tk.Frame(root)
driver_reserve_frame = tk.Frame(root)
driver_dataupdate_frame = tk.Frame(root)

driver_registration_frame = tk.Frame(root)

admin_assign_frame = tk.Frame(root)
admin_assign_nodriver_frame = tk.Frame(root)
admin_assign_nouser_frame = tk.Frame(root)
# Creating a list to store all the frames
my_frames = [home_frame, customer_home_frame, driver_home_frame, admin_assign_frame, admin_signin_frame, customer_registration_frame,
             customer_booking_frame, admin_assign_nouser_frame, admin_assign_nodriver_frame, customer_reserve_frame, driver_dataupdate_frame, driver_reserve_frame,  driver_registration_frame, ]


# Creating a loop for frames
for frame in my_frames:
    frame.grid(row=0, column=0, sticky="nsew")


home_page(home_frame)
admin_signin_page(admin_signin_frame)
customer_home_page(customer_home_frame)
customer_registration_page(customer_registration_frame)
customer_booking_page(customer_booking_frame)
customer_reserved_page(customer_reserve_frame)
driver_home_page(driver_home_frame)
driver_registration_page(driver_registration_frame)
driver_dataupdate_page(driver_dataupdate_frame)
driver_reserved_page(driver_reserve_frame)
admin_assign_page(admin_assign_frame)
admin_assign_nodriver_page(admin_assign_nodriver_frame)
admin_assign_nouser_page(admin_assign_nouser_frame)

display_frames(home_frame)

root.mainloop()
