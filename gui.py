# --------------------------------------------------------------------------------------------
#
#       Graphical User Interface for CSU HEP Lab Inventory System
#
#             created by: Ross Stauder and Nikola Durand
#                           rev: July 2022
#             DUNE - Deep Underground Neutrino Experiment
# --------------------------------------------------------------------------------------------

#  Starting points are called from main and wait for a text entry to be updated, then return the result to main
#  Setup Methods initialize all the widgets on each Tkinter frame
#  Submit methods decide what values need to be fetched and fetch them for the starting point to return to main

# TODO: Make Everything Look Nicer
# TODO: Add Mechanical QC Methods and Frames
# TODO: Add SASEBO QC

import tkinter as tk
from Student import Student
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os

# --------------SETUP VARIABLES AND OBJECTS---------------- #
# setup root
root = tk.Tk()
root.configure(background='#F0F8FF')
root.title('Colorado State University HEP Lab')

# ---------------------setup a canvas----------------------- #

# set up background image
bg = Image.open('CSU-Ram-357-617.png')
resized_image= bg.resize((480, 480), Image.ANTIALIAS)
backdrop= ImageTk.PhotoImage(resized_image)

# setup canvas

height = 480
width = 800

canvas = tk.Canvas(root, width=width, height=height)
canvas.create_image(0, 0, image = backdrop, anchor = "nw")
canvas.grid(columnspan=1, rowspan=1)



# global variable to pass to main
current_entry = tk.StringVar()
current_csuid = tk.StringVar()
current_barcode = tk.StringVar()
current_qty = tk.IntVar()
current_operation = tk.StringVar()
current_object = None
current_database_qty = 0

# variables for radio buttons
v = tk.IntVar()
v.set(1)

r = tk.IntVar()
r.set(1)

# ------HELPER METHODS FOR MISC TKINTER STUFF----- #


# clears whatever frame is passed in
def clearFrame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


# Method For Sign Out, returns to Sign In Page
def exit():
    root.destroy()
    args = sys.argv[1:]
    while(len(args) > 0):
        sys.argv.pop()
        args = sys.argv[1:]
    os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the current program


# displays a message in the TKinter window
def showMessage(message, title):
    messagebox.showinfo(title, message)

# ---------------------------METHODS FOR SUBMIT BUTTONS ON EACH FRAME-------------------------- #

# submit button method for scanID Frame
def submitID(value):
    # -----CHECK INPUT---- #

    # check length of input
    if len(value) == 10:
        value = value[0:-1]
    value = value.strip()
    flag = True  # set to false once fixed

    # TODO: Fix this to work with user data saved to database instead of locally

    # check if employee/student exists in the database
    # for item in Student.users:
    #    if value in item:
    #       flag = True
    # raise exception if an ID of incorrect value is entered
    if len(value) != 9 and len(value) != 10:
        messagebox.showinfo('Invalid Code', 'Error: The Barcode you Entered is Invalid')
        raise ValueError('The ID that was entered contains the wrong number of digits (expected: 9)')
    # raise exceptions if employee does not exist in database
    elif not flag:
        messagebox.showinfo('Invalid Code', 'Error: The Barcode you Entered is Invalid')
        raise KeyError('ID number not recognized, scan again or update employee info')

    # --------SIGN USER IN AND RETURN TO MAIN-------#
    else:
        current_csuid.set(value)  # pass the CSU id back to main
        print(current_csuid.get())
        scanIDFrame.forget()  # remove the current frame
    return None


# submit button method for scanItem Frame
def submitItem(code):
    # check for correct barcode length
    if len(code) != 12:
        messagebox.showinfo('Invalid Code', 'Error: The Barcode you Entered is Invalid')
        raise ValueError('Incorrect Barcode: Wrong Number of Digits')
    # send barcode back to main
    else:
        current_barcode.set(code)
        print(current_barcode.get())
        scanItemFrame.forget()


def submitMech(qty):
    # check that a valid qty was entered
    try:
        qty = int(qty.get())
    except ValueError as e:
        print(e)
        exit()
    # determine whether to add or subtract the qty
    if v.get() == 1:
        current_qty.set(qty)
    elif v.get() == 2:
        current_qty.set(qty*-1)
    print(current_qty.get())
    # cableFrame.grid(column=0, row=0)
    mechanicalItemFrame.forget()
    scanItemFrame.grid(column=0, row=0)


def submitCable(operation):
    global current_operation
    # set the global variable current_operation to whatever cable step is being signed off on
    if operation == 1:
        # Cut
        current_operation.set('Cut to Length')
    elif operation == 2:
        # Labeled
        current_operation.set('Labeled')
    elif operation == 3:
        # Headers
        current_operation.set('Headers')
    elif operation == 4:
        # Stripped
        current_operation.set('Stripped')
    elif operation == 5:
        # Connector
        current_operation.set('Connector')
    elif operation == 6:
        # Prelim Test
        current_operation.set('Prelim Test')
    elif operation == 7:
        # Heat Shrink
        current_operation.set('Heat Shrink')
    elif operation == 8:
        # Final Test
        current_operation.set('Final Test')
    elif operation == 9:
        current_operation.set('QC Verified')
    print(current_operation.get())


# ----------------------SETUP METHODS TO ADD WIDGETS TO EACH FRAME--------------------------------- #

def setupScan():
    # first frame
    label = tk.Label(scanIDFrame, text='Scan ID or enter ID to continue', bg='#F0F8FF', font=('arial', 14, 'normal'))
    label.grid(column=1, row=0)
    global current_entry
    current_entry = tk.Entry(scanIDFrame)
    current_entry.grid(column=1, row=1)
    current_entry.focus_force()
    btn = tk.Button(scanIDFrame, text=' Submit ', command=lambda: submitID(current_entry.get()))
    btn.config(height=2, width=10)
    btn.grid(column=1, row=3)


def setupItem(username):
    # second frame
    signedIn = tk.Label(scanItemFrame, text='Signed in as:', bg='#F0F8FF', font=('arial', 14, 'normal'))
    signedIn.grid(column=0,row=0)
    user = tk.Label(scanItemFrame, text=username, bg='#F0F8FF', font=('arial', 14, 'normal'))
    user.grid(column=1, row=0)
    label = tk.Label(scanItemFrame, text='Scan an Item or Cable to Continue', bg='#F0F8FF', font=('arial', 14, 'normal'))
    label.grid(column=1, row=1)
    code = tk.Entry(scanItemFrame)
    code.grid(column=1, row=2)
    code.focus_force()
    btn = tk.Button(scanItemFrame, text=' Submit ', command=lambda: submitItem(code.get()))
    btn.config(height=2, width=10)
    btn.grid(column=1, row=3)
    exitBtn = tk.Button(scanItemFrame, text= ' exit ', command=lambda: exit())
    exitBtn.grid(column=2, row=3)


def setupMech():
    # third frame p1
    label = tk.Label(mechanicalItemFrame, text='Item: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
    label.grid(column=0, row=0)
    itemLabel = tk.Label(mechanicalItemFrame, text=current_object.name, bg='#F0F8FF', font=('arial', 14, 'normal'))
    itemLabel.grid(column=1, row=0)
    currQtyLabel = tk.Label(mechanicalItemFrame, text='Current Quantity: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
    currQtyLabel.grid(column=0, row=1)
    currQty = tk.Label(mechanicalItemFrame, text=current_database_qty)
    currQty.grid(column=1, row=1)
    qtyLabel = tk.Label(mechanicalItemFrame, text='quantity: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
    qtyLabel.grid(column=1, row=2)
    qtyEntry = tk.Entry(mechanicalItemFrame)
    qtyEntry.grid(column=1, row=2)
    qtyEntry.focus_force()
    options = [
        ('+', 1),
        ('-', 2),
    ]
    for option, val in options:
        tk.Radiobutton(mechanicalItemFrame, text=option, variable=v, value=val, height=2, width=10).grid(column=2, row=val)
    btn = tk.Button(mechanicalItemFrame, text=' Submit ', command=lambda: submitMech(qtyEntry))
    btn.config(height=2, width=10)
    btn.grid(column=1, row=4)
    exitBtn = tk.Button(mechanicalItemFrame, text=' exit ', command=lambda: exit())
    exitBtn.config(height=2, width=10)
    exitBtn.grid(column=2, row=4)


def setupCable(curr_step):
    # third frame p2
    label = tk.Label(cableFrame, text='Cable: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
    label.grid(column=0, row=0)
    cableLabel = tk.Label(cableFrame, text=current_object.name, bg='#F0F8FF', font=('arial', 14, 'normal'))
    cableLabel.grid(column=1, row=0)
    tk.Label(cableFrame, text="Last Sign-Off: ", bg='#F0F8FF', font=('arial', 14, 'normal')).grid(column=0, row=1)
    curr_step_label = tk.Label(cableFrame, text=curr_step, bg='#F0F8FF', font=('arial', 14, 'normal'))
    curr_step_label.grid(column=1, row=1)
    options = [
        ('Cut to Length', 1),
        ('Labeled', 2),
        ('Headers*', 3),
        ('Stripped', 4),
        ('Connector', 5),
        ('Prelim Test', 6),
        ('Heat Shrink', 7),
        ('Final Test', 8),
        ('Verify QC', 9)
    ]
    for option, val in options:
        tk.Radiobutton(cableFrame, text=option, variable=r, value=val).grid(column=0, row=val+1)
    btn = tk.Button(cableFrame, text=' Submit ', command=lambda: submitCable(r.get()))
    btn.config(height=2, width=10)
    btn.grid(column=1, row=10)
    exitBtn = tk.Button(cableFrame, text=' exit ', command=lambda: exit())
    exitBtn.config(height=2, width=10)
    exitBtn.grid(column=2, row=10)


# ----------INITIALIZE FRAMES-------------- #

scanIDFrame = tk.Frame(root, height=height, width=width)
scanItemFrame = tk.Frame(root, height=height, width=width)
mechanicalItemFrame = tk.Frame(root, height=height, width=width)
cableFrame = tk.Frame(root, height=height, width=width)


# --------------------STARTING POINTS, CALLED FROM MAIN------------------- #

# Show the 'Sign In' Frame and wait for the user to hit submit
def begin():
    setupScan()  # setup widgets for frame
    scanIDFrame.grid(column=0, row=0)
    # while keyboard.read_key() == None:
    #    if(len(current_entry.get())) >= 9:
    #        submitID(current_entry.get())
    #        current_entry.set('')
    scanIDFrame.wait_variable(current_csuid)  # wait until user input is submitted
    return current_csuid.get()  # return the user input to the main program


# Show the 'Scan Item' Frame and wait for user to submit
def scanItem(username):
    setupItem(username)  # setup the scan item frame
    scanItemFrame.grid(column=0, row=0)
    scanItemFrame.tkraise()
    clearFrame(scanIDFrame)
    # root.lift()
    # while keyboard.read_key() == None:
    #    if len(current_entry.get()) >= 12:
    #        submitItem(current_entry.get())
    #        current_entry.set('')
    scanItemFrame.wait_variable(current_barcode)  # wait for a barcode to be scanned
    return current_barcode.get()   # return the barcode to main


# Show the 'Mechanical Item' Frame and wait for the user to submit
def addQuantity(obj, qty):
    global current_object
    global current_database_qty
    current_object = obj
    current_database_qty = qty
    setupMech()  # setup mechanical frame
    clearFrame(scanItemFrame)
    mechanicalItemFrame.grid(column=0, row=0)
    mechanicalItemFrame.tkraise()
    mechanicalItemFrame.wait_variable(current_qty)  # wait for user input
    return current_qty.get() # return user input to main


# Show the 'Cable QC' Frame and wait for the user to submit
def addCableQC(obj, ref):
    global current_object
    current_object = obj
    setupCable(obj.find_step(ref))
    cableFrame.grid(column=0, row=0)
    clearFrame(scanItemFrame)
    cableFrame.tkraise()
    cableFrame.wait_variable(current_operation)  # wait for user input
    return current_operation.get()  # return user input to main
