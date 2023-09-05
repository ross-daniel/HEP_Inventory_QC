# --------------------------------------------------------------------------------------------
#
#       Graphical User Interface for CSU HEP Lab Inventory System
#
#             created by: Ross Stauder and Nikola Durand
#                           rev: July 2023
#             DUNE - Deep Underground Neutrino Experiment
# --------------------------------------------------------------------------------------------

#  Starting points are called from main and wait for a text entry to be updated, then return the result to main
#  Setup Methods initialize all the widgets on each Tkinter frame
#  Submit methods decide what values need to be fetched and fetch them for the starting point to return to main

# TODO: Make Everything Look Nicer
# TODO: Add SASEBO QC
# TODO: Add Quit Buttons

import tkinter as tk
from Student import Student
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os

# --------------SETUP VARIABLES AND OBJECTS---------------- #
# setup root
root = tk.Tk()
root.geometry("1200x600")
root.option_add('*Font', ('Inter', 20, 'bold'))
image = Image.open("CSU-Ram-357-617.png")
resized_image = image.resize((600, 600))
bg = ImageTk.PhotoImage(resized_image)
label1 = tk.Label(root, image=bg)
label1.place(x=200, y=0)

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


# -------------- Tkinter Frame Objects ---------------- #

class SignInFrame(tk.Frame):
    def __init__(self, parent):

        self.csuid = tk.StringVar()

        super().__init__(master=parent)

        # set up widgets
        frame_label = tk.Label(self, text='Scan ID or enter ID to continue')
        id_entry = tk.Entry(self)
        id_entry.focus_force()
        btn = tk.Button(self, text=' Submit ', height=2, width=10, command=lambda: self.submitID(id_entry.get()))

        # add widgets to grid (sets location)
        frame_label.grid(column=1, row=0, padx=20, pady=20)
        id_entry.grid(column=1, row=1, padx=20, pady=20)
        btn.grid(column=1, row=3, padx=20, pady=20)

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


class ScanItemFrame(tk.Frame):
    def __init__(self, parent, username_):

        self.item_code = tk.StringVar()
        self.username = username_

        super().__init__(master=parent)

        # ------------------------- SETUP WIDGETS ------------------------------------- #
        signedIn = tk.Label(self, text='Signed in as:')
        user = tk.Label(self, text=self.username)
        label = tk.Label(self, text='Scan an Item or Cable to Continue')
        code = tk.Entry(self)
        code.focus_force()
        btn = tk.Button(self, text=' Submit ', command=lambda: self.submitItem(code.get()))
        btn.config(height=2, width=10)
        exitBtn = tk.Button(self, text=' exit ', command=lambda: exit())
        # -------------------------- ADD TO FRAME -------------------------------------- #
        signedIn.grid(column=0, row=0, padx=20, pady=20)
        user.grid(column=1, row=0, padx=20, pady=20)
        label.grid(column=1, row=1, padx=20, pady=20)
        code.grid(column=1, row=2, padx=20, pady=20)
        btn.grid(column=1, row=3, padx=20, pady=20)
        exitBtn.grid(column=2, row=3, padx=20, pady=20)

    def submitItem(self, code):
        # check for correct barcode length
        if len(code) > 12 or len(code) < 9:
            messagebox.showinfo('Invalid Code', 'Error: The Barcode you Entered is Invalid')
            raise ValueError('Incorrect Barcode: Wrong Number of Digits')
        # send barcode back to main
        else:
            self.item_code.set(code)

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
        label = tk.Label(self, text='Cable: ')
        cableLabel = tk.Label(self, text=self.cable_obj.name)
        tk.Label(self, text="Last Sign-Off: ").grid(column=0, row=1)
        curr_step_label = tk.Label(self, text=self.curr_step)
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
        label.grid(column=0, row=0, padx=20, pady=20)
        cableLabel.grid(column=1, row=0, padx=20, pady=20)
        curr_step_label.grid(column=1, row=1, padx=20, pady=20)
        btn.grid(column=1, row=10, padx=20, pady=20)
        exitBtn.grid(column=2, row=10, padx=20, pady=20)

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
        label = tk.Label(self, text=' Choose What To Do With Item: ')
        item_label = tk.Label(self, text=self.obj.name)
        inv_btn = tk.Button(self, text=' Update Inventory ', command=lambda: self.action.set(0))
        qc_btn = tk.Button(self, text=' Complete QC Doc ', command=lambda: self.action.set(1))
        # ------------- ADD TO GRID -------------------------------------------------- #
        label.grid(row=0, column=0, padx=20, pady=20)
        item_label.grid(row=1, column=0, padx=20, pady=20)
        inv_btn.grid(row=2, column=0, padx=20, pady=20)
        qc_btn.grid(row=3, column=0, padx=20, pady=20)

    def pack(self):
        super().pack()
        self.wait_variable(self.action)


class MechQC(tk.Frame):
    def __init__(self, parent, item):

        qc_steps = item.qc_steps

        self.clicked = tk.StringVar()
        self.line_items = []
        for i in range(4):
            self.line_items.append(tk.IntVar())
        self.passes = tk.IntVar()
        self.total_parts = tk.IntVar()
        self.notes = tk.StringVar()
        self.batch = tk.StringVar()

        super().__init__(master=parent)

        form_label = tk.Label(self, text=' QC Form: ')
        part_label = tk.Label(self, text=item.name)
        step_label = tk.Label(self, text=' Current Step: ')
        passes_label = tk.Label(self, text=' passes: ')
        total_parts_label = tk.Label(self, text=' total parts: ')
        #line_item_label = tk.Label(self, text=' Line Number(s): ')
        notes_label = tk.Label(self, text=' notes: ')
        batch_label = tk.Label(self, text=' batch: ')

        passes_entry = tk.Entry(self)
        total_parts_entry = tk.Entry(self)
        notes_entry = tk.Entry(self)
        batch_entry = tk.Entry(self)

        submit_button = tk.Button(self, text=' Submit ', command=lambda: self.submitMechQC(passes_entry.get(), total_parts_entry.get(), notes_entry.get(), batch_entry.get()))

        #i = 0
        #for line_num in item.line_numbers:
        #    tk.Checkbutton(self, text=line_num, variable=self.line_items[i], onvalue=1, offvalue=0).grid(row=2, column=i+2)
        #    i += 1

        options = []
        for step in qc_steps:
            options.append(step)
        default_opt = options[0]
        self.clicked.set(default_opt)

        dropdown = tk.OptionMenu(self, self.clicked, *options)

        form_label.grid(row=0, column=1, pady=20)
        part_label.grid(row=0, column=2, pady=20)
        step_label.grid(row=1, column=0, pady=20)
        dropdown.grid(row=1, column=1, pady=20)
        passes_label.grid(row=2, column=2, pady=20)
        total_parts_label.grid(row=2, column=0, pady=20)
        #line_item_label
        notes_label.grid(row=3, column=2, pady=20)
        batch_label.grid(row=3, column=0, pady=20)
        passes_entry.grid(row=2, column=3, pady=20)
        total_parts_entry.grid(row=2, column=1, pady=20)
        notes_entry.grid(row=3, column=3, pady=20)
        batch_entry.grid(row=3, column=1, pady=20)
        submit_button.grid(row=4, column=2, columnspan=2, sticky=tk.W+tk.E, pady=20)

    def submitMechQC(self, passes_, total_parts_, notes_, batch_):
        self.passes.set(passes_)
        self.total_parts.set(total_parts_)
        self.notes.set(notes_)
        self.batch.set(batch_)

    def pack(self):
        super().pack()
        self.wait_variable(self.batch)


class MechInventoryFrame(tk.Frame):
    def __init__(self, parent, item):

        self.quantity = tk.IntVar()
        self.sign = tk.IntVar()

        super().__init__(master=parent)

        label = tk.Label(self, text=' Update Item Inventory: ')
        item_label = tk.Label(self, text=item.name)
        qty_entry = tk.Entry(self)
        options = ['+', '-']
        submit_btn = tk.Button(self, text=' Submit ', command=lambda: self.submitInventory(qty_entry.get()))

        for index, opt in enumerate(options):
            tk.Radiobutton(self, text=opt, variable=self.sign, val=index).grid(row=1+index, column=1)

        label.grid(row=0, column=0, padx=20, pady=20)
        item_label.grid(row=0, column=1, padx=20, pady=20)
        qty_entry.grid(row=2, column=0, padx=20, pady=20)
        submit_btn.grid(row=4, column=1, padx=20, pady=20)

    def submitInventory(self, qty):
        self.quantity.set(qty)

    def pack(self):
        super().pack()
        self.wait_variable(self.quantity)
