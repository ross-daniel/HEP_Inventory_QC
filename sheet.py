# --------------------------------------------------------------------------------------------
#
#       Google Sheets API class for CSU HEP Lab Inventory System
#
#                       created by: Ross Stauder
#                           rev: Nov 2022
#             DUNE - Deep Underground Neutrino Experiment
# --------------------------------------------------------------------------------------------

from __future__ import print_function
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import json

CLIENT_SECRET_FILE = 'sheets-example-368018-e62967577200.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None
creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)


try:
    service = discovery.build(API_NAME, API_VERSION, credentials=creds)
except HttpError as err:
    print(err)

class Sheet:
    def __init__(self, *inp):
        # members:
        # sheetId -- id for the sheet (comes from URL)
        # sheet_name -- the name of the specific sheet within the spreadsheet
        # rows -- number of rows
        # cols -- number of columns
        self.sheetId = inp[0]
        self.sheet_name = inp[1]
        self.rows = self.get_rows()
        self.cols = self.get_cols()

    # ------------  HELPERS --------------

    # finds the index of the current sheet within the current spreadsheet
    def get_sheet_index(self):
        return 0

        # helper method to convert a column number to a char identifier
    def convertColumn(self, col):
        if(col == 0):
            print("sheet is empty")
            return ""
        else:
            return chr(64 + col)

    # finds the row/column of the stock or cleaned cell for a given item
    def find_cell_rep(self, barcode, column):
        row = None
        col = None
        line_num = barcode[8:]
        line_num_list = list(line_num)
        line_num_list[len(line_num_list)-1] = 'x'
        line_num = ''.join(line_num_list)
        top_row = self.get_data_list(1, True) # returns the first row of the sheet
        first_column = self.get_data_list(1, False) # returns the first column in the sheet
        for index, item in enumerate(top_row):
            if item == column:
                col = index + 1
        for index, item in enumerate(first_column):
            if line_num in item:
                row = index + 1
        return [row, col]

    # -------------------------------------

    # returns the number of rows in a sheet
    def get_rows(self):
        new_request = service.spreadsheets().get(spreadsheetId=self.sheetId)
        try:
            new_response = new_request.execute()
        except HttpError as err:
            print(err)
            return 0
        row_count = new_response['sheets'][self.get_sheet_index()]['bandedRanges'][0]['range']['endRowIndex']
        return row_count

    # returns the number of columns in a sheet
    def get_cols(self):
        new_request = service.spreadsheets().get(spreadsheetId=self.sheetId)
        try:
            new_response = new_request.execute()
        except HttpError as err:
            print(err)
            return 0
        col_count = new_response['sheets'][self.get_sheet_index()]['bandedRanges'][0]['range']['endColumnIndex']
        return col_count

    # returns the data at a specified cell
    def get_data(self, row, col):
        range_arg = self.sheet_name + '!' + 'A1:' + self.convertColumn(self.cols) + str(self.get_rows())
        new_request = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range_arg)
        try:
            new_response = new_request.execute()
        except HttpError as err:
            print(err)
            return -1
        values = new_response.get('values', [])
        try:
            val = values[row-1][col-1]
        except IndexError as err:
            val = 0
            print(err)
        return val

    # returns an entire row (true) or column (false)
    def get_data_list(self, index, is_row):
        range_arg = self.sheet_name + '!' + 'A1:' + self.convertColumn(self.cols) + str(self.get_rows())
        new_request = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range_arg)
        try:
            new_response = new_request.execute()
        except HttpError as err:
            print(err)
            return -1
        values = new_response.get('values', [])
        if(is_row):
            return values[index-1]
        else:
            vals = []
            for item in values:
                vals.append(item[index-1])
            return vals

    # returns true if the spreadsheet exists
    def exists(self):
        ranges = []
        include_grid_data = False
        request = service.spreadsheets().get(spreadsheetId=self.sheetId, ranges=ranges, includeGridData=include_grid_data)
        try:
            request.execute()
        except HttpError as err:
            print("spreadsheet not found")
            print(err)
            return False
        return True

    # posts the given data to the specified cell in the current spreadsheet
    def post_data(self, row, column, data):
        range_arg = self.sheet_name + '!' + self.convertColumn(column) + str(row)
        val_in_opt = "USER_ENTERED"
        post_data = [[data]]
        request = service.spreadsheets().values().update(spreadsheetId=self.sheetId, range=range_arg, valueInputOption=val_in_opt, body={"values": post_data})
        try:
            result = request.execute()
        except HttpError as err:
            print("could not update cell value")
            print(err)
            return err
        return result
