#--------------------------------------------------------------------------------------------
#
#            Test Cases for CSU HEP Lab Inventory System
#
#                       created by: Ross Stauder
#                           rev: July 2022
#             DUNE - Deep Underground Neutrino Experiment
#--------------------------------------------------------------------------------------------

import unittest
import gui
from Student import Student
from Cable import Cable
from Item import Item
from sheet import Sheet

class MyTestCase(unittest.TestCase):

    def test_cable(self):
        #create a test cable
        testCable = Cable('140050000001')
        self.assertEqual(testCable.name, 'PD-U-R-04-005-2685')

    def test_item_mech(self):
        #M5x8 Screw
        testItem = Item('400001110041')
        self.assertEqual(testItem.name, 'M5-0.80x8mm Silver Plated Socket Head Captive Screw (SHCS SP)')
        self.assertEqual(testItem.distributor, 'Force Fasteners International')
        self.assertEqual(testItem.ship_quantity, '56')

    def test_item_electrical(self):
        #female hirose connector
        testItem = Item('500000009012')
        self.assertEqual(testItem.part_number, '798-HR10A-10R-12S71')
        self.assertEqual(testItem.line_number, '901')
        self.assertEqual(testItem.distributor, 'Mouser')

    def test_submit_id(self):
        with self.assertRaises(KeyError):
            gui.submitID('933068328')
        with self.assertRaises(ValueError):
            gui.submitID('6')


    def test_submit_item_noexist(self):
        with self.assertRaises(ValueError):
            gui.submitItem('90909090')

    def test_submit_item_exists(self):
        gui.submitItem('400001110041')
        self.assertEqual(gui.current_barcode.get(), '400001110041')

    def test_student(self):
        student = Student('833068328')
        self.assertEqual(student.name, 'Ross Stauder')

    #def test_sheet(self):
        #test_sheet = Sheet()
        #self.assertEqual(test_sheet)

# TODO: !!!!!!!! Write More Test Cases !!!!!!!!!

if __name__ == '__main__':
    unittest.main()
