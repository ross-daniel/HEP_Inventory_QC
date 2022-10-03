#--------------------------------------------------------------------------------------------
#
#       Student Class for CSU HEP Lab Inventory System, holds student employee info
#
#                              created by: Tabor Horrigan
#                                   rev: August 2022
#                     DUNE - Deep Underground Neutrino Experiment
#--------------------------------------------------------------------------------------------


# This code takes in the pathname of a csv file then takes in the CSV, adds \n to the end
# of a row and then takes all of these items and puts them into one joined string storing
# them into a new csv called "finalfile.csv".
# The csv package is necessary for this function to operate successfully.
# PLEASE NOTE THAT THE INPUT CSV CANNOT HAVE COMMAS WITHIN THE TITLES FOR ITEMS OR IT WILL BREAK

# Date: 08/25/2022
# Author: Tabor Horrigan
import csv


def convert(x, op_file):

    # This is an empty array to store all the individual items after the "/n" have been added
    totalitems = []
    with open(x) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        # This itterates through the input file and separates into rows and adds the "\n" to the end of it
        for row in spamreader:
            row.append("\\n")
            # This iterates through the row and pulls out each individual item to store in an array
            for i in row:
                totalitems.append(i)
            # Converting the array of items into one combined string
        "".join(totalitems)
        # Creating the csv file for storing the final output
        outputfile = op_file
        # This opens the newly created file to write to it
        with open(outputfile, "w") as newfile:
            # Creates an object with the ability to write to the new file
            playmaker = csv.writer(newfile)
            # Writes the combined string into the output csv file
            playmaker.writerow(totalitems)
            newfile.close()
    return newfile