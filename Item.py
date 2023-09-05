#--------------------------------------------------------------------------------------------
#
#       Item Class for CSU HEP Lab Inventory System, Represents all data
#      related to mechanical and electrical components used in production
#
#                       created by: Ross Stauder
#                           rev: July 2022
#               DUNE - Deep Underground Neutrino Experiment
#--------------------------------------------------------------------------------------------

import csv
import sheet
import gui
from googleapiclient.errors import HttpError
from datetime import datetime
#import yagmail


class Item:

    file = 'Barcode_Sheet_FINAL.csv'
    mechFile = open(file, 'r')
    inventory_list = list(csv.reader(mechFile))
    qc_table = open('MechQC_Steps.csv', 'r')
    qc_list = list(csv.reader(qc_table))

    # gets the current quantity of self in the DB
    def getQty(self, ref):
        ref = ref.child('Mechanical').child(self.name).get()
        try:
            print(ref.get('qty'))
        except AttributeError as e:
            print("Item has not been initialized")
            print(e)
            return 0
        return int(ref.get('qty'))

    def getClean(self, ref):
        ref = ref.child('Mechanical').child(self.name).get()
        num_cleaned = 0
        try:
            num_cleaned = int(ref.get('clean'))
        except Exception as e:
            print("Item has not been initialized")
            print(e)
            return 0
        return num_cleaned

    # sends an automated email to Zach Rautio when an items stock reaches a low quantity
    def sendEmail(self, stock):

        # TODO: Fix this method to work without Yagmail (library is deprecated)

        # create necessary parameters
        sender_addr = 'csuhighenergy@gmail.com'
        reciever_addr = 'stauderross@gmail.com'#'Zach.Rautio@colostate.edu'
        app_password = 'axrnygfpjpuuknir'
        subject = 'STOCK DEPLETION'

        # create the body of the email
        message = 'Stock for the following item has dropped below 2 shipment quantities: \n\n'
        message += 'Item: ' + self.name + '\n'
        message += 'Part Number: ' + self.part_number + '\n\n'
        message += 'Ship Quantity: ' + self.ship_quantity + '\n'
        message += 'Current Stock: ' + str(stock) + '\n'

        # send the email
        #with yagmail.SMTP(sender_addr, app_password) as yag:
        #    yag.send(reciever_addr, subject, message)
        #    print(message)
        #    print('Sent email successfully')

    # determines part details based on product code
    # reads csv file and creates a 2D array of product codes and their corresponding parameters
    def readProductCode(self):
        target = f"y{self.product_code[8]}{self.product_code[9]}{self.product_code[10]}"
        print(target)
        for index, item in enumerate(Item.inventory_list):
            if target in item[0]:
                self.product_code = item[0]  # make barcode exactly as it appears in the sheet
                print(Item.inventory_list[index])
                return list(Item.inventory_list[index])

    # updates the inventory of the given item by a given quantity
    def postToDB(self, qty, clean, reference):
        ref = reference.child('Mechanical')
        ssheet = sheet.Sheet('1cLLx9eAhPwMRBq-8NWbToL408jOAgZCuEcejaFOKW-k', 'InventorySheet')
        if self.name in ref.get().keys():
            # item already exists in the database
            # find the current quantity of the item
            currQty = self.getQty(reference)
            currClean = self.getClean(reference)
            if (currQty + int(qty) < int(self.ship_quantity)*2) and currQty >= 2*int(self.ship_quantity):
                # send automated email to zach if quantity drops below shipment quantity
                self.sendEmail(currQty + int(qty))
            # update the quantity of the item
            if clean:
                ref.child(self.name).update({'clean': currClean+qty})
            else:
                ref.child(self.name).update({'qty': currQty+qty})
        else:
            # item has not yet been added to database
            if clean:
                ref.child(self.name).update({'clean': qty})
            else:
                ref.child(self.name).update({'qty': qty})

        # ----------- update spreadsheet -------------------- #
        cell_rep = ssheet.find_cell_rep(self.product_code, 'Stock')
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
        if curr_qty != currQty:
            gui.showMessage("Database and Spreadsheet hold different values, please take a count of this item and update the proper location", "INVENTORY INCONSISTENCY")

    # adds the QC doc to the database
    def postQCtoDB(self, ref, batch_num, qc_step, passes, total_parts, line_items, notes, user):
        ref = ref.child('Mechanical QC Docs').child(self.name).child(batch_num).child(qc_step)
        ref.update({'passes': passes})
        ref.update({'total parts': total_parts})
        ref.update({'notes': notes})
        ref.update({'signature': user.name})
        ref.update({'date': str(datetime.date(datetime.now()))})

    def has_qc_form(self):
        if len(self.qc_steps) > 0:
            return True
        else:
            return False

    def get_qc_steps(self):
        qc_steps_list = []
        for part_list in Item.qc_list:  # iterate through all rows of the spreadsheet
            if part_list[0] == self.product_code:  # check the second column of each row until a matching part description is found
                qc_steps_list = part_list[3:7]  # save the qc steps into a new array
                self.line_numbers = part_list[2].split(",")  # grab line number while here
                index = 3
                for qc_step in qc_steps_list:  # iterate through the newly created list
                    if qc_step == 'x':
                        qc_steps_list[index-3] = Item.qc_list[0][index]  # if the cell has an 'x' replace it with the corresponding qc step
                    index += 1
                qc_steps_list = [i for i in qc_steps_list if i != '-']  # remove all steps not included for the part
        return qc_steps_list  # should return something like: ['Dimension Check', 'Deburr / Deglue', 'Bag and Label']

    def __init__(self, product_code):
        self.product_code = product_code
        properties = self.readProductCode()
        self.name = properties[2]
        print(self.name)
        self.line_number = properties[1]
        self.line_numbers = []
        self.part_number = properties[3]
        self.ship_quantity = properties[4]
        self.distributor = properties[5]
        self.qc_steps = self.get_qc_steps()
        self.has_qc = self.has_qc_form()
        # if ref is not None:
        #    self.ref = ref
        #    self.current_quantity = self.getQty(ref)
        #else:
        #    self.ref = None
        #    self.current_quantity = None
