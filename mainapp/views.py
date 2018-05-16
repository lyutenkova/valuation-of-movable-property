import os
from time import sleep

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from export_excel import export_to_excel
from support import save_file_to_disk
import parse_excel
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            uploaded_path = save_file_to_disk(request)
            message = parse_excel.message_for_user(uploaded_path)

            return render(request, 'index.html', {'response': "Файл успешно загружен!"})

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