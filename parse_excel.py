import xlrd
import xlwt
from django.forms.models import model_to_dict
from mainapp.models import ComparativeApproach, CostApproach
import psycopg2
import os

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
        cost_list = parse_cost(paths[0])
        save_to_db(cost_list, COST)

        comparative_list = parse_comparative(paths[1])
        save_to_db(comparative_list, COMPARATIVE)

        flag = True

    except Exception as err:
        print("Has error! ", err)

    finally:
        return flag


def parse_comparative(path_to_file):
    list_dicts = [] # список строк для разыменования в базу

    workbook = xlrd.open_workbook(path_to_file)
    sheet = workbook.sheet_by_index(0)
    k_rows = sheet.nrows # кол-во объектов в файле

    for row in range(5, k_rows):
        db_dict = {"name": None, "year": None, "mileage": None, "offer_price": None, "par1_name": None, "par1_val": None, "par2_name": None, "par2_val": None}
        
        db_dict['name'] = sheet.row_values(row)[0]
        db_dict['year'] = sheet.row_values(row)[1] 
        db_dict['mileage'] = sheet.row_values(row)[2] 
        db_dict['offer_price'] = sheet.row_values(row)[17] 
        db_dict['par1_name'] = sheet.row_values(5)[21] 
        db_dict['par1_val'] = sheet.row_values(row)[22] 
        db_dict['par2_name'] = sheet.row_values(5)[23] 
        db_dict['par2_val'] = sheet.row_values(row)[24] 

        list_dicts.append(db_dict)

    return list_dicts

def parse_cost(path_to_file):
    list_dicts = []
    
    workbook = xlrd.open_workbook(path_to_file)
    sheet = workbook.sheet_by_index(0)
    k_rows = sheet.nrows

    for row in range(5, k_rows):
        db_dict = {"mark": None, "cost_of_new": None, "par1_name": None, "par1_val": None, "par2_name": None, "par2_val": None}
        
        db_dict['mark'] = sheet.row_values(row)[1]
        db_dict['cost_of_new'] = sheet.row_values(row)[4]
        db_dict['par1_name'] = sheet.row_values(5)[6]
        db_dict['par1_val'] = sheet.row_values(row)[7]
        db_dict['par2_name'] = sheet.row_values(5)[8]
        db_dict['par2_val'] = sheet.row_values(row)[9]

        list_dicts.append(db_dict)

    return list_dicts


def save_to_db(list_dicts, param):
    if param == COST:
        for dict_row in list_dicts:
            print("СТРОКА_ЗАТРАТ", dict_row)
            CostApproach(**dict_row).save()

    if param == COMPARATIVE:
        for dict_row in list_dicts:
            print("СТРОКА_СРАВНИТ", dict_row)
            ComparativeApproach(**dict_row).save()


def message_for_user(path_to_file):
    # разбираем файл на два, возвращаем пути до них
    paths = make_two_files(path_to_file)
    # записываем данные из файлов в базу
    # - для этого парсим поочередно оба файла и вызываем функцию save для каждого
    flag = write_data_to_base(paths) # успешно ли прошла запись в базу?

    if flag:
        if (os.path.exists("cost.xls")):
            os.remove("cost.xls")
        if(os.path.exists("comparative.xls")):
            os.remove("comparative.xls")
        if(os.path.exists("input.xlsm")):
            os.remove("input.xlsm")

        return 'Данные из файла успешно загружены в базу!'

    else:
        return 'Произошла ошибка при загрузке данных из файла, пожалуйста проверьте формат файла и заполненные данные!'

