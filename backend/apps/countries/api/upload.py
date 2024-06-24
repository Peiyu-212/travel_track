import pandas as pd
from apps.users.models import Users

from ..models import Countries, TravelExpense, VisitedCountries
from .exceptions import CountryNameWrong, ErrorDataType, ErrorHeaders, SheetDoesNotExists


class CountryUpload:
    """
    Upload default world country name and country code
    """

    def __init__(self, data: object) -> None:
        self.read_csv(data)

    def read_csv(self, data):
        try:
            self.csv = pd.read_csv(data['file'])
        except ValueError as e:
            print(e)
            raise e

    def upload(self) -> None:
        obj_list = []
        for i in self.csv.to_dict('records'):
            obj_list.append(
                Countries(
                    id=i['id'],
                    country_code=i['country_code'],
                    country_name=i['country_name']
                )
            )
        Countries.objects.bulk_create(obj_list)


class TravelExpenseUpload:
    """
    Upload database with TravelExpense sheet
    """

    rename_cols = {"Date": 'visited_date', "Cost": "cost", "Sightseeing": "sightseeing",
                   "Country": "country_name", "Description": "description"}
    headers = list(rename_cols.keys())

    def __init__(self, data: object, sheet_name: str, **kwargs):
        self.read_excel(data, sheet_name, **kwargs)

    def read_excel(self, data, sheet_name, **kwargs):
        try:
            self.excel = pd.read_excel(data['file'], sheet_name=sheet_name, dtype=object, **kwargs)
        except ValueError as e:
            print(e)
            raise SheetDoesNotExists(f"Sheet '{sheet_name}' does not exist !")

    def upload(self, user: str) -> None:
        try:
            df = self.excel[self.headers]
        except KeyError:
            diff = set(self.headers) - set(self.excel.columns.to_list())
            raise ErrorHeaders(
                f"Error! the column {diff} does not exist! Please download template first!"
            )

        df = df.rename(columns=self.rename_cols)
        df.drop_duplicates(inplace=True)
        df.dropna(how='all', inplace=True)
        df.fillna(0, inplace=True)

        # check if the cost column is integer
        converted = pd.to_numeric(df['cost'], errors='coerce')
        if pd.isna(converted).any():
            raise ErrorDataType("There are some non-numeric value in Cost column.")

        # transform visited date column to date format
        df['visited_date'] = pd.to_datetime(df['visited_date']).dt.date

        # get user id
        user = Users.objects.get(name=user)

        country_name_wrong_list = []
        row_num = 1
        for i in df.itertuples():
            country_code = Countries.objects.filter(country_name=i.country_name)
            if not country_code.exists():
                country_name_wrong_list.append(f"Row {row_num}: Country Name have wrong spelling!")
            else:
                obj, _ = VisitedCountries.objects.get_or_create(user_id=user.id,
                                                                country_code=country_code[0].country_code)
                TravelExpense.objects.update_or_create(description=i.description,
                                                       cost=i.cost,
                                                       visited_date=i.visited_date,
                                                       defaults={"user_country_id": obj.id,
                                                                 "sightseeing": i.sightseeing})
        if len(country_name_wrong_list) > 0:
            raise CountryNameWrong("\n".join(country_name_wrong_list))
