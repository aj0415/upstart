import csv

from django.http import HttpResponse
from django.shortcuts import redirect


class ExportJsonMixin:
    def export_json_as_csv(self, request, queryset):
        """
        Export the JSONField of a model to a CSV file
        """
        meta = self.model._meta
        json_field = None
        for field in meta.fields:
            if field.get_internal_type() == 'JSONField':
                json_field = field
        if not json_field:
            self.message_user(
                request,
                "No JSONField found"
            )
            return redirect("..")

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)

        json_data = queryset.values_list(json_field.name, flat=True)
        fieldnames = list(json_data[0].keys())
        writer = csv.DictWriter(response, fieldnames=fieldnames, delimiter=',', quotechar="'", lineterminator="\n")
        writer.writeheader()
        for row in json_data:
            writer.writerow(row)
        return response

    export_json_as_csv.short_description = 'Export Selected to CSV'
