# --------------------------------------------------------------------------------------------
#
#   Main program for CSU HEP Lab Inventory System, controls all data flow
#
#                       created by: Ross Stauder
#                           rev: October 2022
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

# get program arguments, used to keep a user signed in across multiple sessions
args = sys.argv[1:]
print(args)

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

# TODO: Check if GitHub Repo has been updated, if so, clone repo

# Check Barcode Sheet
# If the barcode sheet has been updated, update the .txt file used for the javascript front-end
tempFile = convert('Barcode_Sheet_FINAL.csv', 'temp_file.txt')
if(not filecmp.cmp('temp_file.txt', 'barcode.txt')):
    print("file converted")
    convert('Barcode_Sheet_FINAL.csv', 'barcode.txt')
os.remove('temp_file.txt')


# -------GUI CONTROL FLOW------- #


# if the user is not already signed in, prompt them to sign in
if(not len(args) > 0):
    # load first page of gui, asks for an ID to be scanned
    csuid = gui.begin()
    # create a student object from the csuid
    student = Student(csuid, ref)
    # find the students name
    username = student.name
# if user is already signed in, set the current Student object to the correct user
else:
    student = Student(args[-1], ref)
    csuid = student.csuid
    username = student.name
while True:
    # load second page of gui, asks for an item to be scanned
    barcode = gui.scanItem(username)
    obj = None  # initialize an object, used to pass either a cable or item object to gui.py

    # detect whether the barcode refers to a Cable or Mechanical Item
    if int(barcode[0]) < 4:
        # Cable
        obj = Cable(int(barcode))  # create object
        op = gui.addCableQC(obj, ref)  # display the cable QC form on the GUI
        obj.postToDB(op, username, ref)  # call the post to DB method of the cable class
        sys.argv.append(csuid)  # add the current user to program arguments to keep them signed in
        os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the current program
        print("Shouldn't get here")
    else:
        # Mechanical Item
        obj = Item(barcode)  # create object
        # choose whether to update inventory or QC Docs for the item
        action = gui.chooseAction()
        if action == 0:
            # ------ update database ------
            qty = gui.addQuantity(obj, obj.getQty(ref))  # display the inventory update screen on the GUI
            if gui.cleaned:
                curr_DBqty = obj.getClean(ref)
            else:
                curr_DBqty = obj.getQty(ref)
            obj.postToDB(qty, gui.cleaned, ref)
            # -----------------------------
            # ------ update spreadsheet ------
            ssheet = Sheet('1cLLx9eAhPwMRBq-8NWbToL408jOAgZCuEcejaFOKW-k', 'InventorySheet')

            # finds [row, col] for the required cell
            if gui.cleaned:
                cell_rep = ssheet.find_cell_rep(barcode, 'Cleaned')
            else:
                cell_rep = ssheet.find_cell_rep(barcode, 'Stock')

            curr_qty = ssheet.get_data(cell_rep[0], cell_rep[1])       # finds the current quantity of the item
            if curr_qty == '':
                curr_qty = 0
            else:
                curr_qty = int(curr_qty)
            print(f"cell_rep[0]: {cell_rep[0]}")
            print(f"cell_rep[1]: {cell_rep[1]}")
            print(f"total quantity: {curr_qty+qty}")
            try:
                ssheet.post_data(cell_rep[0], cell_rep[1], curr_qty+qty)    # updates the spreadsheet
            except HttpError as e:
                print(e)
            # make sure the spreadsheet and database show the same value
            if curr_qty != curr_DBqty:
                gui.showMessage("Database and Spreadsheet hold different values, please take a count of this item and update the proper location", "INVENTORY INCONSISTENCY")

            # --------------------------------
        else:
            # ------ update QC database ------
            procedures = obj.findQCProcedures()
            pass_fail = gui.addMechQC(obj, procedures)
            obj.postQCtoDB(ref, procedures, pass_fail)
            print(obj.batch_num)
            # --------------------------------

        # ------ restart the program ------
        sys.argv.append(csuid)  # add the current user to program arguments to keep them signed in
        os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the current program
        # ---------------------------------
        print("Shouldn't get here")


#gui.root.mainloop()