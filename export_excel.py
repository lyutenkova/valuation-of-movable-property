import io
import pprint

from django.http.response import HttpResponse
from xlsxwriter.workbook import Workbook

import xlsxwriter

def export_to_excel(excel_dict):
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    format_for_data = workbook.add_format({'font_name': 'Times New Roman' , 'font_size': 10 })
    header_format = workbook.add_format({"bold": True, "font_name": "Times New Roman" , "font_size": 10, 'bg_color': '#4CB486'})
    worksheet = workbook.add_worksheet()

    row=1
    col=0
    for k,v in excel_dict[0].items():
        worksheet.write(0, col, str(k), header_format)
        col +=1
    for e in excel_dict:
        col = 0
        for k,v in e.items():
            worksheet.write(row, col, str(v), format_for_data)
            col += 1
        row += 1
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    return response