import xlrd
import xlwt

def make_two_files(path_to_file):
    # workbook = xlrd.open_workbook('input.xlsm')
    workbook = xlrd.open_workbook(path_to_file)

    new_book1 = xlwt.Workbook(encoding="utf-8")
    new_book2 = xlwt.Workbook(encoding="utf-8")

    sheet1 = new_book1.add_sheet("Затратный")
    sheet2 = new_book2.add_sheet("Сравнительный")

    for sheet in workbook.sheets():
        if sheet.name == "ОЦЕНКА":
            for row in range(sheet.nrows):
                if row == 1 or row == 2:
                    continue

                for cell, index_col in zip(sheet.row_values(row), range(len(sheet.row_values(row)))):
                    if index_col >= 15:
                        sheet2.write(row, index_col - 15, cell)

                    elif index_col > 33:
                        continue

                    else:
                        sheet1.write(row, index_col, cell)
        else:
            continue    
        
        new_book1.save("zatratniy.xls")
        new_book2.save("sravnitelniy.xls")
    
    return ("./zatratniy.xls", "./sravnitelniy.xls")


def write_data_to_base(paths):
    flag = False

    try:
        parse_zatrat(paths[0])
        parse_sravnit(paths[1])

        flag = True

    except Exception as err:
        print("Has error! ", err)

    finally:
        return flag


def parse_sravnit(path_to_file):
    workbook = xlrd.open_workbook(path_to_file)
    pass


def parse_zatrat(path_to_file):
    workbook = xlrd.open_workbook(path_to_file)
    pass


def save_to_db():
    pass


if __name__ == "__main__":
    paths = make_two_files('input.xlsm')
