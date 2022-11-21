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
#import yagmail


class Item:

    file = 'Barcode_Sheet_FINAL.csv'
    mechFile = open(file, 'r')
    inventory_list = list(csv.reader(mechFile))

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

    def updateSpreadSheet(self, qty):
        # TODO: Write a method that automatically updates an inventory spreadsheet
        print("this method is not yet functional")

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
        target = f"y{self.product_code[8]}{self.product_code[9]}{self.product_code[10]}";
        print(target)
        for index, item in enumerate(Item.inventory_list):
            if target in item[0]:
                print(Item.inventory_list[index])
                return list(Item.inventory_list[index])

    # updates the inventory of the given item by a given quantity
    def postToDB(self, qty, reference):
        ref = reference.child('Mechanical')
        if self.name in ref.get().keys():
            # item already exists in the database
            # find the current quantity of the item
            currQty = self.getQty(reference)
            if (currQty + int(qty) < int(self.ship_quantity)*2) and currQty >= 2*int(self.ship_quantity):
                # send automated email to zach if quantity drops below shipment quantity
                self.sendEmail(currQty + int(qty))
            # update the quantity of the item
            ref.child(self.name).update({'qty': currQty+qty})
        else:
            # item has not yet been added to database
            ref.child(self.name).update({'qty': qty})

    def __init__(self, product_code):
        self.product_code = product_code
        properties = self.readProductCode()
        self.name = properties[2]
        print(self.name)
        self.line_number = properties[1]
        self.part_number = properties[3]
        self.ship_quantity = properties[4]
        self.distributor = properties[5]
