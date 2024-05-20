import xlwt
from django.http import HttpResponse
from .models import *
from shop.models import *


def get_field_value(obj, field_name):
    """ Retrieve the value of a field or method, handling ForeignKey fields. """
    # Check if the attribute is a method and call it if so
    if hasattr(obj, field_name) and callable(getattr(obj, field_name)):
        return getattr(obj, field_name)()
    
    # Check if the value is a model instance (ForeignKey field)
    value = getattr(obj, field_name)
    if hasattr(value, '_meta'):
        return str(value)  # Use the __str__ method of the model instance

    return value


def download_excel_new(queryset, columns, file_name='Table', excluded_fields=[]):
    # Create an HttpResponse object with the appropriate headers
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.xls"'  #File name

    # Create a workbook and add a worksheet
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(file_name)  # sheet name

    # If the queryset is empty, no need to proceed
    if not queryset:
        return response    

    # Write the headers
    for col_num, column in enumerate(columns):
        ws.write(0, col_num, column)

    # Write data from the queryset
    for row_num, obj in enumerate(queryset, 1):
        for col_num, field in enumerate(columns):
            # Retrieve value from object dynamically using getattr
            val = get_field_value(obj, field)
            ws.write(row_num, col_num, val)

    # Save the workbook in the response
    wb.save(response)


    return response