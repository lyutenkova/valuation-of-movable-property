import xlrd
import xlwt
from django.forms.models import model_to_dict
from main_app.models import ComparativeApproach, CostApproach

COST = 'cost_approach'
COMPARATIVE = 'comparative_approach'

def make_two_files(path_to_file):
    workbook = xlrd.open_workbook(path_to_file)

    new_book1 = xlwt.Workbook(encoding="utf-8")
    new_book2 = xlwt.Workbook(encoding="utf-8")

    sheet1 = new_book1.add_sheet(COST)
    sheet2 = new_book2.add_sheet(COMPARATIVE)

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
        
        new_book1.save("cost.xls")
        new_book2.save("comparative.xls")
    
    return ("./cost.xls", "./comparative.xls")


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


def parse_comparative(path_to_file):
    db_dict = {"name": [], "year": [], "mileage": [], "offer_price": [], "par1_name": [], "par1_val": [], "par2_name": [], "par2_val": []}
    
    workbook = xlrd.open_workbook(path_to_file)
    sheet = rb.sheet_by_index(0)
    k_rows = sheet.nrows

    db_dict['name'] = [sheet.row_values(i)[0] for i in range(5, k_rows)]
    db_dict['year'] = [sheet.row_values(i)[1] for i in range(5, k_rows)]
    db_dict['mileage'] = [sheet.row_values(i)[2] for i in range(5, k_rows)]
    db_dict['offer_price'] = [sheet.row_values(i)[17] for i in range(5, k_rows)]
    db_dict['par1_name'] = [sheet.row_values(i)[21] for i in range(5, k_rows)]
    db_dict['par1_val'] = [sheet.row_values(i)[22] for i in range(5, k_rows)]
    db_dict['par2_name'] = [sheet.row_values(i)[23] for i in range(5, k_rows)]
    db_dict['par2_val'] = [sheet.row_values(i)[24] for i in range(5, k_rows)]

    return db_dict

def parse_cost(path_to_file):
    db_dict = {"mark": [], "cost_of_new": [], "par1_name": [], "par1_val": [], "par2_name": [], "par2_val": []}
    
    workbook = xlrd.open_workbook(path_to_file)
    sheet = workbook.sheet_by_index(0)
    k_rows = sheet.nrows

    db_dict['mark'] = [sheet.row_values(i)[1] for i in range(5, k_rows)]
    db_dict['cost_of_new'] = [sheet.row_values(i)[4] for i in range(5, k_rows)]
    db_dict['par1_name'] = [sheet.row_values(i)[6] for i in range(5, k_rows)]
    db_dict['par1_val'] = [sheet.row_values(i)[7] for i in range(5, k_rows)]
    db_dict['par2_name'] = [sheet.row_values(i)[8] for i in range(5, k_rows)]
    db_dict['par2_val'] = [sheet.row_values(i)[9] for i in range(5, k_rows)]

    return db_dict


def save_to_db(db_dict, param):
    if param == COST:
        for row in db_dict:
            CostApproach(**db_dict).save()

    if param == COMPARATIVE:
        for row in db_dict:
            ComparativeApproach(**db_dict).save()


def data_from_db():
    pass