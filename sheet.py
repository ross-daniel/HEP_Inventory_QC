# --------------------------------------------------------------------------------------------
#
#       Google Sheets API class for CSU HEP Lab Inventory System
#
#                       created by: Ross Stauder
#                           rev: Nov 2023
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

creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)


try:
    service = discovery.build(API_NAME, API_VERSION, credentials=creds)
except HttpError as err:
    print(err)


class Sheet:
    def __init__(self, sid="1cLLx9eAhPwMRBq-8NWbToL408jOAgZCuEcejaFOKW-k", name="InventorySheet"):
        # members:
        # sheetId -- id for the sheet (comes from URL)
        # sheet_name -- the name of the specific sheet within the spreadsheet
        # rows -- number of rows
        # cols -- number of columns
        self.sheetId = sid
        self.sheet_name = name
        self.rows = self.get_rows()
        self.cols = self.get_cols()
        self.identifiers = self.get_data_list(1, True)  # self.get_column_ids()
        self.barcodes = self.get_data_list(1, False)

    # ------------  HELPERS -------------------------------------------------------------------------------------------

    # finds the index of the current sheet within the current spreadsheet
    # filler method, may be modified if InventorySheet is not at index 0
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
    def find_cell_rep(self, item, identifier):
        row = self.find_row_index(item)
        col = self.find_column_index(identifier)
        return [row, col]

    def find_row_index(self, item):
        row = -1
        first_column = self.barcodes # returns the first column in the sheet
        for index, value in enumerate(first_column):
                if item.product_code == value:
                    row = index + 1
        return row

    def find_column_index(self, identifier):
        col = -1
        top_row = self.identifiers  # returns the first row of the sheet
        for index, value in enumerate(top_row):
                if value == identifier:
                    col = index + 1
        return col

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

    # -----------------------------------------------------------------------------------------------------------------
    # -------- CLASS FUNCTIONS ----------------------------------------------------------------------------------------

    # returns the data at a specified cell
    def get_data(self, item, identifier):
        col = self.identifiers.index(identifier)
        row = -1
        for index, value in enumerate(self.barcodes):
            if item.product_code == value:
                row = index + 1
                break
        full_row = self.get_data_list(row, True)
        return full_row[col]

    # returns an entire row (true) or column (false) at the index given
    def get_data_list(self, rc_index, is_row):
        if is_row:
            range_arg = self.sheet_name + '!' + str(rc_index) + ':' + str(rc_index)  # range arg for the entire row (A1 notation)
            new_request = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range_arg)
            try:
                new_response = new_request.execute()
                # return the values of each cell in the first row as an array
                return new_response.get('values')[0]
            except HttpError as err:
                print(err)
                return -1
        else:
            range_arg = self.sheet_name + '!' + self.convertColumn(rc_index) + ':' + self.convertColumn(rc_index)
            new_request = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range_arg)
            try:
                new_response = new_request.execute()
                column_values_list = new_response.get('values', [])  ## returns an array of arrays with only a single value [[col1_val], [col2_val], [col3_val] .... ]
                col_values = []
                # iterate through the list of 1D vectors that hold the column values and put them into a new list
                for col_list_1D in column_values_list:
                    col_values.append(col_list_1D[0])
                # return a list of all the values in the column
                return col_values
            except HttpError as err:
                print(err)
                return -1

    # posts the given data to the cell defined by the item and identifier passed
    def post_data(self, item, identifier, data):

        [row, col] = self.find_cell_rep(item, identifier)

        range_arg = self.sheet_name + '!' + self.convertColumn(col) + str(row)
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

    # -----------------------------------------------------------------------------------------------------------------

