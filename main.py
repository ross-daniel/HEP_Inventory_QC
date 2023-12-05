# --------------------------------------------------------------------------------------------
#
#   Main program for CSU HEP Lab Inventory System, controls all data flow
#
#                       created by: Ross Stauder
#                           rev: 2023
#             DUNE - Deep Underground Neutrino Experiment
# --------------------------------------------------------------------------------------------

from Cable import Cable
from Item import Item
from Student import Student
from converter import convert
from sheet import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import filecmp
import gui
import os
import sys
import subprocess
import time


# function to check program arguments, ensuring the user stays signed in but no extra arguments are added
#  --- to be called before restarting the program ---
def update_args(employee_id_num):
    if len(sys.argv[1:]) > 0:
        while len(sys.argv) > 1:
            sys.argv.pop(-1)
    sys.argv.append(employee_id_num)

# -------DATABASE SETUP-------#

# TODO: Figure Out a way to more easily pass database references to other classes

# TODO: Shift from uploading data to a database and a spreadsheet to just a spreadsheet

#retrieve admin credentials
cred = credentials.Certificate('hep---dune-firebase-adminsdk-gtwlw-40673207a6.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hep---dune-default-rtdb.firebaseio.com'
})

# As an admin, the app has access to read and write all data
ref = db.reference('')

# -------------MISC SETUP------------ #
# makes sure important external files are configured properly

# TODO: Check if GitHub Repo has been updated, if so, prompt user to update

# Check Barcode Sheet
# If the barcode sheet has been updated, update the .txt file used for the javascript front-end
tempFile = convert('Barcode_Sheet_FINAL.csv', 'temp_file.txt')
if(not filecmp.cmp('temp_file.txt', 'barcode.txt')):
    convert('Barcode_Sheet_FINAL.csv', 'barcode.txt')
os.remove('temp_file.txt')


# -------GUI CONTROL FLOW------- #

if __name__ == "__main__":

    # --------------- SIGN IN PAGE --------------------------------------------------------- #
    # if the user is not already signed in, prompt them to sign in
    if not len(sys.argv) > 1:
        # load first page of gui, asks for an ID to be scanned
        scan_id_frame = gui.SignInFrame(gui.root)  # create the frame
        scan_id_frame.pack()  # load the frame
        scan_id_frame.lift()
        csuid = scan_id_frame.csuid.get()
        if not csuid:
            gui.showMessage('The ID number you entered was invalid or an error occurred', 'Sign In ERROR')
            os.execl(sys.executable, sys.executable, *sys.argv)  # end program and restart
        employee = Student(csuid, ref)  # create a Student object with the entered csuid
        scan_id_frame.destroy()  # destroy the ID frame
    # if user is already signed in, set the current Student object to the correct user
    else:
        employee = Student(sys.argv[-1], ref)
        csuid = employee.csuid
    # --------------------------------------------------------------------------------------- #
    # ------------------ SCAN ITEM PAGE ----------------------------------------------------- #
    scan_item_frame = gui.ScanItemFrame(gui.root, employee.name)  # create the scan item frame
    scan_item_frame.pack()  # load the scan item frame
    # wait for user to submit
    barcode = scan_item_frame.item_code.get()
    scan_item_frame.destroy()  # destroy the frame
    # --------------------------------------------------------------------------------------- #
    obj = None
    # ------------------- ELECTRICAL -------------------------------------------------------- #
    if int(barcode[0]) < 4:
        obj = Cable(int(barcode))
        cable_traveler_frame = gui.CableTraveler(gui.root, obj, obj.find_step(ref))  # create cable frame
        cable_traveler_frame.pack()  # load cable frame
        cable_step = cable_traveler_frame.cable_step.get()  # grab user input
        obj.postToDB(cable_step, employee.name, ref)  # post traveler step to DB
        update_args(csuid)  # update program arguments to keep the user signed in
        print(f"args: {sys.argv}")
        os.execl(sys.executable, sys.executable, *sys.argv)  # end program and restart
    # --------------------------------------------------------------------------------------- #
    # ------------------- MECHANICAL -------------------------------------------------------- #
    obj = Item(barcode)
    # decide whether the scanned item has a QC form or not

    if obj.has_qc:
        # if so, send the user to the choose action page
        choose_action_frame = gui.ChooseAction(gui.root, obj)
        choose_action_frame.pack()
        action = choose_action_frame.action.get()
        choose_action_frame.destroy()
        if action == 1:
            # ------------------- MECHANICAL QC ----------------------------------------------------- #
            mech_qc_frame = gui.MechQC(gui.root, obj)
            mech_qc_frame.pack()
            step = mech_qc_frame.clicked.get()
            line_num_list = []
            #for index in range(len(mech_qc_frame.line_items)):
            #    if mech_qc_frame.line_items[index].get() == 1:
            #        line_num_list.append(obj.line_numbers[index])
            passes = mech_qc_frame.passes.get()
            total_parts = mech_qc_frame.total_parts.get()
            notes = mech_qc_frame.notes.get()
            batch = mech_qc_frame.batch.get()
            print(f"Step: {step}")
            #print(f"Line Numbers: {line_num_list}")
            print(f"Passes: {passes}")
            print(f"Total Parts: {total_parts}")
            print(f"Notes: {notes}")
            print(f"Batch: {batch}")
            mech_qc_frame.destroy()
            # post QC to DB
            obj.postQCtoDB(ref, batch, step, passes, total_parts, line_num_list, notes, employee.name)
            update_args(csuid)  # update program arguments to keep the user signed in
            os.execl(sys.executable, sys.executable, *sys.argv)  # end program and restart
        # --------------------------------------------------------------------------------------- #
    # else send them to inventory frame
    # ------------------- INVENTORY --------------------------------------------------------- #
    inventory_frame = gui.MechInventoryFrame(gui.root, obj)
    inventory_frame.pack()
    qty = inventory_frame.quantity.get()
    if inventory_frame.sign.get() == 1:
        qty = qty*-1
    inventory_frame.destroy()
    obj.postToDB(qty, 'Stock', ref)
    update_args(csuid)  # update program arguments to keep the user signed in
    os.execl(sys.executable, sys.executable, *sys.argv)  # end program and restart
    # --------------------------------------------------------------------------------------- #

    # --------------------------------------------------------------------------------------- #

    gui.root.mainloop()
