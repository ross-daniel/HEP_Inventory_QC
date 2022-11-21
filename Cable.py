#--------------------------------------------------------------------------------------------
#
#       Cable Class for CSU HEP Lab Inventory System, Represents all data
#                           related to cables
#
#                       created by: Ross Stauder
#                           rev: July 2022
#              DUNE - Deep Underground Neutrino Experiment
#--------------------------------------------------------------------------------------------


from datetime import datetime


class Cable:

    # length of each cable by number and type
    upperLen = ['6570', '0780', '1390', '2075', '2685', '3370', '3980', '4665', '5275', '5960']
    lowerLen = ['6109', '0579', '1219', '1778', '2438', '2985', '3632', '4197', '4851', '5436']

    # QC steps

    steps = ['Cut to Length', 'Labeled', 'Headers', 'Stripped', 'Connector', 'Prelim Test', 'Heat Shrink', 'Final Test']

    # determines the value of class variables based on the product code
    def readProductCode(self):
        # convert the number into a list of integers
        code = list(map(int, str(self.product_code)))

        # check the 2nd most significant digit (denotes cable number)
        self.cableNumber = code[1]

        # check most significant digit (denotes type of cable)
        # once type of cable is determined, find the length
        if code[0] == 1:
            self.cableType = 'Uppers'
            self.length = Cable.upperLen[self.cableNumber]
        elif code[0] == 2:
            self.cableType = 'Lowers'
            self.length = Cable.lowerLen[self.cableNumber]
        elif code[0] == 3:
            self.cableType = 'Passthroughs'
            self.length = '7850'
        else:
            print("Invalid Barcode")
        # detect batch number
        self.batch = str(code[2]) + str(code[3]) + str(code[4])

    # creates a string that resembles the physical label on a cable
    def makeLabel(self):
        name = 'PD-'
        if(self.cableType == 'Uppers'):
            name += 'U-R-'
        elif(self.cableType == 'Lowers'):
            name += 'L-R-'
        elif(self.cableType == 'Passthroughs'):
            name += 'U-P-'
        if(self.cableNumber == 0):
            name += '1'
        else:
            name += '0'
        name += str(self.cableNumber)
        name += '-'
        name += self.batch
        name += '-'
        name += self.length

        return name

    # sends a JSON packet to firebase and stores the data in the proper part of the tree
    def postToDB(self, operation, name, reference):
        date = str(datetime.date(datetime.now()))
        if(self.cableNumber == 0):
            num = 10
        else:
            num = self.cableNumber
        ref = reference.child(self.cableType).child('Batch').child(self.batch).child(str(num))  # finds proper reference
        ref.update({operation: name + " -- " + date})  # updates database
        print("Database Updated")

    # finds the most recent step signed off on for a given cable
    def find_step(self, reference):
        if self.cableNumber == 0:
            num = 10
        else:
            num = self.cableNumber
        try:
            keys = reference.child(self.cableType).child('Batch').child(self.batch).child(str(num)).get().keys()
        except AttributeError as err:
            print(err)
            return "None"
        recent = "None"
        index = -1
        for item in keys:
            indx = Cable.steps.index(item)
            if indx > index:
                index = indx
        if index >= 0:
            recent = Cable.steps[index]
        return recent

    def __init__(self, code):
        self.product_code = code
        self.readProductCode()
        self.name = self.makeLabel()

