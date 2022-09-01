#--------------------------------------------------------------------------------------------
#
#   Main program for CSU HEP Lab Inventory System, controls all data flow
#
#                       created by: Ross Stauder
#                           rev: August 2022
#             DUNE - Deep Underground Neutrino Experiment
#--------------------------------------------------------------------------------------------

from Cable import Cable
from Item import Item
from Student import Student
from converter import convert
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import filecmp
import gui
import os
import sys

#get program arguments, used to keep a user signed in across multiple sessions
args = sys.argv[1:]
print(args)

#-------DATABASE SETUP-------#

# TODO: Figure Out a way to more easily pass database references to other classes

#retrieve admin credentials
cred = credentials.Certificate('ENTER JSON CREDENTIALS FILENAME HERE')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hep-test-eef24-default-rtdb.firebaseio.com/'
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
        op = gui.addCableQC(obj)  # display the cable QC form on the GUI
        obj.postToDB(op, username, ref)  # call the post to DB method of the cable class
        sys.argv.append(csuid)  # add the current user to program arguments to keep them signed in
        os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the current program
    else:
        # Mechanical Item
        obj = Item(barcode)  # create object
        qty = gui.addQuantity(obj, obj.getQty(ref))  # display the inventory update screen on the GUI
        obj.postToDB(qty, ref)  # call the post to DB method of the Item class
        sys.argv.append(csuid)  # add the current user to program arguments to keep them signed in
        os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the current program

gui.root.mainloop()




