import xlrd


# Example to run:
# path = ('your_xls_path.xls') #("./app/static/files/ddc22-summaries-eng.xls")
# sheet_index = your_sheet_index
# excel = Excel(path, sheet_index)
# excel.nrows # to get row total
# excel.ncols # to get col total
# excel.column_names # to get column names
# excel.get_data(column_id=column_index, row_id=row_index) # to get data based on given param
# excel.get_all_data() # to get all data

class Excel():
    path = ""
    sheet = 0
    nrows = 0
    ncols = 0
    column_names = []

    def __init__(self, path, sheet):
        self.mount_file(path, sheet)

    def mount_file(self, path, sheet):
        self.path = path
        self.sheet = sheet

        file_sheet = self.get_sheet()
        self.nrows = file_sheet.nrows
        self.ncols = file_sheet.ncols

        column_names = []
        for i in range(self.ncols):
            column_names.append(file_sheet.cell_value(0, i))
        self.column_names = column_names

    def get_sheet(self):
        wb = xlrd.open_workbook(self.path)
        return wb.sheet_by_index(self.sheet)

    def get_data(self, column_id=None, row_id=None):
        file_sheet = self.get_sheet()
        if column_id is None:
            return file_sheet.row_values(row_id)
        else:
            data = []
            if row_id is None:
                for i in range(self.nrows):
                    if i != 0:
                        data.append(file_sheet.cell_value(i, column_id))
            else:
                data.append(file_sheet.cell_value(row_id, column_id))
            return data

    def get_all_data(self):
        file_sheet = self.get_sheet()
        data = []
        for i in range(self.nrows):
            if i != 0:
                data.append(file_sheet.row_values(i))
        return data
