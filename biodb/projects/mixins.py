import re
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.db.models import CharField
from biodb.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import ForeignKey
from django.db.models import TextField
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View
from openpyxl import Workbook
from projects.models import Project
from robjects.models import Robject
from robjects.models import Tag
from weasyprint import CSS
from weasyprint import HTML
from django.http.response import HttpResponseRedirect


class ExportViewMixin(object):
    # django.db.models.Model
    model = None
    pdf_template_name = None
    pdf_css_name = None
    css_sufix = None

    def get_model_fields(self, is_relation=False, one_to_one=False, many_to_one=False, exclude_fields=None):
        """
        Return list of fields names
        Attrs:
        """
        if not exclude_fields:
            exclude_fields = []
        model_fields = []
        for field in self.model._meta.get_fields():
            if field.name not in exclude_fields:
                if field.one_to_one:
                    if one_to_one:
                        model_fields.append(field.name)
                elif (field.many_to_one and field.related_model):
                    if many_to_one:
                        model_fields.append(field.name)
                elif field.is_relation:
                    if is_relation:
                        model_fields.append(field.name)
                else:
                    model_fields.append(field.name)

        return model_fields

    def strip_field(self, field_value):
        ''' Strip field from HTML'''
        if isinstance(field_value, datetime):
            return field_value.strftime("%Y-%m-%d %H:%M")
        else:
            field = str(field_value)
            if bool(BeautifulSoup(field, "html.parser").find()):
                only_text = BeautifulSoup(
                    str(field_value), 'html.parser').text
                return only_text.strip()
            else:
                return field

    def export_to_excel(self, queryset, is_relation=False, one_to_one=False, many_to_one=False, exclude_fields=None):
        """ Function handle export to excel view"""

        # create workbook
        wb = Workbook()
        # capture active worksheet
        ws = wb.active
        # filling first row by fields names
        fields_names = self.get_model_fields(
            is_relation, one_to_one, many_to_one, exclude_fields)
        ws.append(fields_names)
        for query_object in queryset:
            temp = list()
            for field_name in fields_names:
                # holding field value
                if field_name in ["tags", "names"]:
                    field_string = getattr(
                        query_object, field_name).all().all_as_string()
                else:
                    field_value = getattr(query_object, field_name)
                    field_string = self.strip_field(field_value)

                # append to container
                temp.append(field_string)

                # adding cline row to excel
            ws.append(temp)
        output = HttpResponse()
        # preparing output
        file_name = "report.xlsx"
        # saving workbook to output
        wb.save(output)
        output['Content-Disposition'] = 'attachment; filename=' + file_name
        return output

    def export_to_pdf(self, queryset):
        ''' View generates pdf view based on models template name and
            model fields.
            In model define:
                model, pdf_template_name, pdf_css_name, css_sufix
        '''

        # create template from file
        html_template = get_template(self.pdf_template_name)
        # get single element list robjects

        rendered_html = html_template.render(
            {'robjects': queryset}).encode(encoding="UTF-8")
        # generate pdf from rendered html
        pdf_file = HTML(string=rendered_html).write_pdf(
            stylesheets=[CSS(settings.BASE_DIR + self.css_sufix +
                             settings.STATIC_URL + self.pdf_css_name)],
        )
        # Add file object to response

        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename="raport.pdf"'
        # return response

        return http_response
