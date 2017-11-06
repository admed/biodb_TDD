import django_tables2 as tables
from samples.models import Sample


class SampleTable(tables.Table):
    edit_entries = tables.TemplateColumn(
        '<a href="/projects/{{record.robject.project.name}}/samples/{{record.id}}/update/">Edit</a>')
    robject = tables.TemplateColumn(
        '<a href="/projects/{{record.robject.project.name}}/samples/{{record.id}}/detail/">{{ record.robject }}</a>')

    class Meta:
        model = Sample
        attrs = {"class": "paleblue"}
        default = '-'
        sequence = ('robject', '...')

        row_attrs = {
            'data-id': lambda record: record.pk
        }
        # add class="paleblue" to <table> tag
