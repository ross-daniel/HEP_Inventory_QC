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
    def find_cell_rep(self, item, identifier):
        row = None
        col = None
        top_row = self.identifiers  # returns the first row of the sheet
        first_column = self.barcodes # returns the first column in the sheet
        for index, value in enumerate(top_row):
            if item == identifier:
                col = index + 1
        for index, value in enumerate(first_column):
            if item.target in value:
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

    def get_column_ids(self):
        range_arg = self.sheet_name + '!1:1'  # range arg for the entire top row (A1 notation)
        new_request = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range_arg)
        try:
            new_response = new_request.execute()
            return new_response.get('values', [])
        except HttpError as err:
            print(err)
            return []

    # returns the data at a specified cell
    def get_data(self, item, indentifier):
        col = indentifier.index(indentifier)
        row = -1
        for index, value in enumerate(self.barcodes):
            if item.product_code == value[0]:
                row = index + 1
                break
        full_row = self.get_data_list(row, True)
        print(full_row)
        return full_row[col-1]

    # returns an entire row (true) or column (false)
    def get_data_list(self, rc_index, is_row):
        if is_row:
            range_arg = self.sheet_name + '!' + str(rc_index) + ':' + str(rc_index)  # range arg for the entire row (A1 notation)
            new_request = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range_arg)
            try:
                new_response = new_request.execute()
                return new_response.get('values', [])[0]
            except HttpError as err:
                print(err)
                return -1
        else:
            range_arg = self.sheet_name + '!' + self.convertColumn(rc_index) + ':' + self.convertColumn(rc_index)
            new_request = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=range_arg)
            try:
                new_response = new_request.execute()
                return new_response.get('values', [])[0]
            except HttpError as err:
                print(err)
                return -1

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
