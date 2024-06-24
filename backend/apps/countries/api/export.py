import datetime
import re

import matplotlib
from apps.users.models import Users
from openpyxl.styles import Side
from openpyxl_style_writer import CustomStyle, RowWriter

from django.http import HttpResponse

from .upload import TravelExpenseUpload

thin_border = {
    'left': Side(style='thin', color='cccccc'),
    'right': Side(style='thin', color='cccccc'),
    'top': Side(style='thin', color='cccccc'),
    'bottom': Side(style='thin', color='cccccc'),
}


class StyleCollections:
    normal_center = CustomStyle(
        font_size='11', font_bold=False, border_params=thin_border, fill_color='ffffff', ali_horizontal='center'
    )
    red_fill = CustomStyle(
        font_size='11', font_bold=False, font_color='ffffff',
        fill_color='ffb3b3'
    )


class ExcelBase(RowWriter, StyleCollections):

    def __init__(self, user):
        super().__init__()
        self.user = user

    def _create_excel_response(self, title: str) -> HttpResponse:
        response = HttpResponse()

        filename = datetime.datetime.now().strftime('%Y%m%d') + '_' + title + '.xlsx'
        self.wb.save(response)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def download_template(self) -> HttpResponse:
        self._create_single_sheet()
        self._create_single_header()
        sheet_name = re.sub(r'\s+', '_', self.sheet_name.lower())
        sheet_name += '_template'
        return self._create_excel_response(sheet_name)

    def _create_single_sheet(self) -> None:
        self.create_sheet(self.sheet_name)

    def _get_user_color(self) -> object:
        user_color = Users.objects.get(name=self.user).color
        hex_color_transform = matplotlib.colors.cnames[user_color].replace('#', '')
        user_color_fill = CustomStyle(
            font_size='11', font_bold=False, font_color='ffffff',
            fill_color=hex_color_transform
        )
        return user_color_fill

    def _create_single_header(self) -> None:
        self.switch_current_sheet(self.sheet_name)
        for i, h in enumerate(self.header):
            header_len = len(h) * 2.5
            self.set_cell_width(col=i + 1, width=header_len)
            self.row_append(h, style=self._get_user_color())
        self.create_row()


class UserDownloaderTemplateExport(ExcelBase):
    sheet_name = "Travel_Expense"
    header = ['Date', 'Cost', 'Sightseeing', 'Country', 'Description']


class UserExpenseExport(UserDownloaderTemplateExport):
    rename_cols = TravelExpenseUpload.rename_cols

    def __init__(self, user: str, data: list[dict[str, str]]):
        super().__init__(user)
        self.data = data

    def download(self) -> HttpResponse:
        """
        Generates and downloads the Excel file.

        Returns:
        An HttpResponse object representing the Excel file.
        """
        self._create_single_sheet()
        self._create_single_header()
        self._create_body()
        sheet_name = re.sub(r'\s+', '_', self.sheet_name.lower())
        return self._create_excel_response(sheet_name)

    def _create_body(self) -> None:
        """
        Creates the body of the sheet with the provided data.
        """

        for data in self.data:
            for col in self.header:
                col_name = self.rename_cols.get(col)
                self.row_append(data[col_name], style=self.normal_center)
            self.create_row()
