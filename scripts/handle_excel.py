import openpyxl
import os

from scripts.handle_path import DATAS_DIR
from scripts.handle_yaml import do_yaml


class CaseData:
    pass


class HandleExcel(object):
    def __init__(self, sheetname, filename=None):
        if filename is None:
            self.filename = os.path.join(DATAS_DIR, do_yaml.read_yaml('excel', 'cases_path'))
        else:
            self.filename = filename
        self.sheetname = sheetname

    def open(self):
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    def read_data_obj(self):
        self.open()
        rows = list(self.sh.rows)
        titles = [t.value for t in rows[0]]
        cases = []
        for k in rows[1:]:
            data = [j.value for j in k]
            case = CaseData()
            for i in zip(titles, data):
                setattr(case, i[0], i[1])
            cases.append(case)
        self.wb.close()
        return cases

    def write_data(self, row, column, value):
        self.open()
        self.sh.cell(row=row, column=column, value=value)
        self.wb.save(self.filename)
        self.wb.close()

if __name__ == "__main__":
    read = HandleExcel('register')
    read.read_data_obj()
    pass




