import os
from time import sleep

import xlwt

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import parse_excel
import export_data_to_exel

from export_excel import export_to_excel
from support import save_file_to_disk


@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            uploaded_path = save_file_to_disk(request)
            message = parse_excel.message_for_user(uploaded_path)

            return render(request, 'index.html', {'response': message})

        except Exception as e:
            print("views ", e)
            return render(request, 'index.html', {'response':'Ошибка обработки файла. Неверный формат.'})
    
    else:
        return render(request, 'index.html', {})


def mark(request):
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            d = plan_b_parse_egrn(fils)

            return export_to_excel(d)
        except Exception as e:
            print(e)
            return render(request, 'mark.html', {'response':'Ошибка обработки файла. Неверный формат.'})
    else:
        return render(request, 'mark.html', {})  #  рендер страницы html


def get_data_cost(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="zatratny.xls"'

        data = export_data_to_exel.data_from_db(export_data_to_exel.COST)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(export_data_to_exel.COST)

        xlwt.add_palette_colour("custom_colour", 0x21)
        wb.set_colour_RGB(0x21, 44, 176, 116)

        style = xlwt.easyxf(
        'pattern: pattern solid, fore_colour custom_colour;'
        'font: colour white, bold True;')

        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'
        
        name_of_cols = ['id', 'mark', 'cost_of_new', 'par1_name', 'par1_val', 'par2_name', 'par2_val', 'created_at']

        for index_col in range(len(data[0])):  #  заполняем названия столбцов
            ws.write(0, index_col, name_of_cols[index_col], style)

        for row, index_row in zip(data, range(1, len(data) + 1)):
            for el, index_col in zip(row, range(len(row))):
                if index_col == 7:
                    tmp = el.replace(tzinfo=None)
                    ws.write(index_row, index_col, tmp, date_format) 
                else:
                    ws.write(index_row, index_col, el) 

        wb.save(response)

        return response

def get_data_comparative(request):
        if request.method == 'GET':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="sravnitelny.xls"'

            data = export_data_to_exel.data_from_db(export_data_to_exel.COMPARATIVE)

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet(export_data_to_exel.COMPARATIVE)

            xlwt.add_palette_colour("custom_colour", 0x21)
            wb.set_colour_RGB(0x21, 44, 176, 116)

            style = xlwt.easyxf(
            'pattern: pattern solid, fore_colour custom_colour;'
            'font: colour white, bold True;')

            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd/mm/yyyy'
            
            name_of_cols = ['id', 'name', 'year', 'mileage', 'offer_price', 'par1_name', 'par1_val', 'par2_name', 'par2_val', 'created_at']

            for index_col in range(len(data[0])):  #  заполняем названия столбцов
                ws.write(0, index_col, name_of_cols[index_col], style)

            for row, index_row in zip(data, range(1, len(data) + 1)):
                for el, index_col in zip(row, range(len(row))):
                    if index_col == 9:
                        tmp = el.replace(tzinfo=None)
                        ws.write(index_row, index_col, tmp, date_format)
                    else:
                        ws.write(index_row, index_col, el)

            wb.save(response)

            return response