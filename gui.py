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

# ---------------------setup a canvas----------------------- #


def set_background(root):
    #make title and set bg
    root.configure(background='#F0F8FF')
    root.title('Colorado State University HEP Lab')

    # set up background image
    bg = Image.open('CSU-Ram-357-617.png')
    resized_image= bg.resize((480, 480), Image.ANTIALIAS)
    backdrop= ImageTk.PhotoImage(resized_image)

    # setup canvas

    height = 480
    width = 800

    canvas = tk.Canvas(root, width=width, height=height)
    canvas.create_image(0, 0, image=backdrop, anchor="nw")
    canvas.pack()

# -------------- Tkinter Frame Objects ---------------- #


class SignInFrame(tk.Frame):
    def __init__(self, parent):

        self.csuid = tk.StringVar()

        super().__init__(master=parent)

        # set up widgets
        frame_label = tk.Label(self, text='Scan ID or enter ID to continue', bg='#F0F8FF', font=('arial', 14, 'normal'))
        id_entry = tk.Entry(self)
        id_entry.focus_force()
        btn = tk.Button(self, text=' Submit ', height=2, width=10, command=lambda: self.submitID(id_entry.get()))

        # add widgets to grid (sets location)
        frame_label.grid(column=1, row=0)
        id_entry.grid(column=1, row=1)
        btn.grid(column=1, row=3)

    def submitID(self, id_num):
        # -----CHECK INPUT---- #

        # check length of input
        if len(id_num) == 10:
            id_num = id_num[0:-1]
        id_num = id_num.strip()
        flag = True  # set to false once fixed

        # TODO: Fix this to work with user data saved to database instead of locally

        # check if employee/student exists in the database
        # for item in Student.users:
        #    if value in item:
        #       flag = True
        # raise exception if an ID of incorrect value is entered
        if len(id_num) != 9 and len(id_num) != 12:
            messagebox.showinfo('Invalid Code', 'Error: The Barcode you Entered is Invalid')
            raise ValueError('The ID that was entered contains the wrong number of digits (expected: 9)')
        # raise exceptions if employee does not exist in database
        elif not flag:
            messagebox.showinfo('Invalid Code', 'Error: The Barcode you Entered is Invalid')
            raise KeyError('ID number not recognized, scan again or update employee info')

        # --------SIGN USER IN AND RETURN TO MAIN-------#
        else:
            self.csuid.set(id_num)  # pass the CSU id back to main
        return None

    def pack(self):
        super().pack()
        self.wait_variable(self.csuid)
        print("done waiting")


class ScanItemFrame(tk.Frame):
    def __init__(self, parent, username_):

        self.item_code = tk.StringVar()
        self.username = username_

        super().__init__(master=parent)

        # ------------------------- SETUP WIDGETS ------------------------------------- #
        signedIn = tk.Label(self, text='Signed in as:', bg='#F0F8FF', font=('arial', 14, 'normal'))
        user = tk.Label(self, text=self.username, bg='#F0F8FF', font=('arial', 14, 'normal'))
        label = tk.Label(self, text='Scan an Item or Cable to Continue', bg='#F0F8FF', font=('arial', 14, 'normal'))
        code = tk.Entry(self)
        code.focus_force()
        btn = tk.Button(self, text=' Submit ', command=lambda: self.submitItem(code.get()))
        btn.config(height=2, width=10)
        exitBtn = tk.Button(self, text=' exit ', command=lambda: exit())
        # -------------------------- ADD TO FRAME -------------------------------------- #
        signedIn.grid(column=0, row=0)
        user.grid(column=1, row=0)
        label.grid(column=1, row=1)
        code.grid(column=1, row=2)
        btn.grid(column=1, row=3)
        exitBtn.grid(column=2, row=3)

    def submitItem(self, code):
        # check for correct barcode length
        if len(code) > 12 or len(code) < 9:
            messagebox.showinfo('Invalid Code', 'Error: The Barcode you Entered is Invalid')
            raise ValueError('Incorrect Barcode: Wrong Number of Digits')
        # send barcode back to main
        else:
            self.item_code.set(code)
            print(self.item_code.get())

    def pack(self):
        super().pack()
        self.wait_variable(self.item_code)


class CableTraveler(tk.Frame):

    def __init__(self, parent, cable_obj_, curr_step_):

        self.cable_step = tk.StringVar()
        self.cable_obj = cable_obj_
        self.curr_step = curr_step_

        self.radio = tk.IntVar()
        self.radio.set(1)

        super().__init__(master=parent)

        # ------------ SETUP WIDGETS ------------------------------------------------ #
        label = tk.Label(self, text='Cable: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        cableLabel = tk.Label(self, text=self.cable_obj.name, bg='#F0F8FF', font=('arial', 14, 'normal'))
        tk.Label(self, text="Last Sign-Off: ", bg='#F0F8FF', font=('arial', 14, 'normal')).grid(column=0, row=1)
        curr_step_label = tk.Label(self, text=self.curr_step, bg='#F0F8FF', font=('arial', 14, 'normal'))
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
            tk.Radiobutton(self, text=option, variable=self.radio, value=val).grid(column=0, row=val+1)
        btn = tk.Button(self, text=' Submit ', command=lambda: self.submitCable(self.radio.get()))
        btn.config(height=2, width=10)
        exitBtn = tk.Button(self, text=' exit ', command=lambda: exit())
        exitBtn.config(height=2, width=10)

        # ------------ ADD TO GRID -------------------------------------------------- #
        label.grid(column=0, row=0)
        cableLabel.grid(column=1, row=0)
        curr_step_label.grid(column=1, row=1)
        btn.grid(column=1, row=10)
        exitBtn.grid(column=2, row=10)

    def submitCable(self, radio_value):
        # set the global variable current_operation to whatever cable step is being signed off on
        if radio_value == 1:
            # Cut
            self.cable_step.set('Cut to Length')
        elif radio_value == 2:
            # Labeled
            self.cable_step.set('Labeled')
        elif radio_value == 3:
            # Headers
            self.cable_step.set('Headers')
        elif radio_value == 4:
            # Stripped
            self.cable_step.set('Stripped')
        elif radio_value == 5:
            # Connector
            self.cable_step.set('Connector')
        elif radio_value == 6:
            # Prelim Test
            self.cable_step.set('Prelim Test')
        elif radio_value == 7:
            # Heat Shrink
            self.cable_step.set('Heat Shrink')
        elif radio_value == 8:
            # Final Test
            self.cable_step.set('Final Test')
        elif radio_value == 9:
            self.cable_step.set('QC Verified')

    def pack(self):
        super().pack()
        self.wait_variable(self.cable_step)


class ChooseAction(tk.Frame):
    def __init__(self, parent, obj_):

        self.action = tk.IntVar()  # 0 = inventory, 1 = QC
        self.obj = obj_

        super().__init__(master=parent)

        # ------------- SETUP WIDGETS ----------------------------------------------- #
        label = tk.Label(self, text=' Choose What To Do With Item: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        item_label = tk.Label(self, text=self.obj.name, bg='#F0F8FF', font=('arial', 14, 'normal'))
        inv_btn = tk.Button(self, text=' Update Inventory ', command=lambda: self.action.set(0))
        qc_btn = tk.Button(self, text=' Complete QC Doc ', command=lambda: self.action.set(1))
        # ------------- ADD TO GRID -------------------------------------------------- #
        label.grid(row=0, column=0)
        item_label.grid(row=1, column=0)
        inv_btn.grid(row=2, column=0)
        qc_btn.grid(row=3, column=0)

    def pack(self):
        super().pack()
        self.wait_variable(self.action)


class MechQC(tk.Frame):
    def __init__(self, parent, item):

        qc_steps = item.qc_steps

        self.step = tk.IntVar()
        self.line_items = []
        for i in range(4):
            self.line_items.append(tk.IntVar)
        self.passes = tk.IntVar()
        self.total_parts = tk.IntVar()
        self.notes = tk.StringVar()
        self.batch = tk.StringVar()

        super().__init__(master=parent)

        form_label = tk.Label(self, text=' QC Form: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        part_label = tk.Label(self, text=item.name, bg='#F0F8FF', font=('arial', 14, 'normal'))
        step_label = tk.Label(self, text=' Current Step: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        passes_label = tk.Label(self, text=' passes: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        total_parts_label = tk.Label(self, text=' total parts: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        line_item_label = tk.Label(self, text=' Line Number(s): ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        notes_label = tk.Label(self, text=' notes: ', bg='#F0F8FF', font=('arial', 14, 'normal'))
        batch_label = tk.Label(self, text=' batch: ', bg='#F0F8FF', font=('arial', 14, 'normal'))

        passes_entry = tk.Entry(self)
        total_parts_entry = tk.Entry(self)
        notes_entry = tk.Entry(self)
        batch_entry = tk.Entry(self)

        submit_button = tk.Button(self, text=' Submit ', command=lambda: self.submitMechQC())

        i = 0
        for line_num in item.line_numbers:
            tk.Checkbutton(self, text=line_num, variable=self.line_items[i], onvalue=1, offvalue=0).grid(row=2, column=i+2)
            i += 1

        options = []
        index = 1
        for step in qc_steps:
            options.append((step, index))
            index += 1
        for option, val in options:
            tk.Radiobutton(self, text=option, variable=self.step, value=val).grid(column=val+1, row=1)

        form_label.grid(row=0, column=2)
        part_label.grid(row=0, column=3)
        step_label.grid(row=1, column=1)
        passes_label.grid(row=2, column=0)
        total_parts_label.grid(row=3, column=1)
        line_item_label.grid(row=2, column=3, columnspan=2, sticky=tk.W+tk.E)
        notes_label.grid(row=3, column=3)
        batch_label.grid(row=4, column=2)
        passes_entry.grid(row=2, column=1)
        total_parts_entry.grid(row=3, column=2)
        notes_entry.grid(row=3, column=4)
        batch_entry.grid(row=4, column=3)
        submit_button.grid(row=5, column=2, columnspan=2, sticky=tk.W+tk.E)

    def submitMechQC(self):
        return None

    def pack(self):
        super().pack()
        self.wait_variable(self.batch)