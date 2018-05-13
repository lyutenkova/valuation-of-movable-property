import os
from time import sleep

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from export_excel import export_to_excel
from main import get_documents_for_organization
from parser_egrn import plan_b_parse_egrn
from parsing_exel import get_dict_from_exel_kostyl
from support import save_file_to_disk, save_files_to_disk


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            uploaded_path = save_file_to_disk(request)
            excel_dict = get_dict_from_exel_kostyl(uploaded_path)
            res_dicts=[]
            for e in excel_dict:
                is_correct = is_INN_correct(e['ИНН Залогодателя'], e['Залогодатель'])
                print(is_correct)
                info = None
                while info is None:
                    info = get_documents_for_organization(inn=e['ИНН Залогодателя'])
                    sleep(1)
                    print("INF",info)
                for k, v in info.items():
                    print(k,v)
                    print(e)
                    e[str(k)] = v

                res_dicts += [e]

            return export_to_excel(res_dicts)
        except Exception as e:
            print(e)
            return render(request, 'index.html', {'response':'Ошибка обработки файла. Неверный формат.'})
    else:
        return render(request, 'index.html', {})


def fed(request):
    # context = {}
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            fils = save_files_to_disk(request)
            d = plan_b_parse_egrn(fils)

            return export_to_excel(d)
        except Exception as e:
            print(e)
            return render(request, 'fed.html', {'response':'Ошибка обработки файла. Неверный формат.'})
    else:
        return render(request, 'fed.html', {})  #  рендер страницы html