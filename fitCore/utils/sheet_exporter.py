import csv
from io import BytesIO, StringIO
from django.http import HttpResponse
from openpyxl import Workbook


class SheetExporter:
    def generate_csv(self, data):
        out = StringIO()
        writer = csv.writer(out)
        if data:
            headers = list(data[0].keys())
            writer.writerow(headers)
        for row in data:
            writer.writerow([row[header] for header in headers])

        return out.getvalue()

    def generate_csv_response(self, data, name="sheet"):
        csv_file = self.generate_csv(data)
        response = HttpResponse(csv_file, content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{name}.csv"'
        return response

    def generate_xlsx(self, data, sheet_title="sheet"):
        out = BytesIO()
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = sheet_title

        if data:
            headers = list(data[0].keys())
            sheet.append(headers)
        for row in data:
            sheet.append([row[header] for header in headers])

        workbook.save(out)
        out.seek(0)

        return out.getvalue()

    def generate_xlsx_response(self, data, name="sheet", sheet_title="sheet"):
        xlsx_file = self.generate_csv(data)
        response = HttpResponse(
            xlsx_file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{name}.xlsx"'
        return response
