import pandas as pd
from apps.users.models import Users

from ..models import Countries, TravelExpense


class UserTravelTrackReshaping:
    '''
    to get about user information and country cost total
    '''

    def __init__(self, user: str):
        '''
        Initialize the UserTravelTrackReshaping object
        Args:
        - user (str): The user name
        '''

        self.user = Users.objects.filter(name=user)
        self.travel_expense = TravelExpense.objects.filter(user_country__user__name=user).values(
            'cost', 'user_country__country_code', 'sightseeing', 'description', 'visited_date'
        )
        self.country = dict(Countries.objects.values_list('country_code', 'country_name'))

    def _get_travel_expense_df(self):
        df = pd.DataFrame(self.travel_expense)
        df.rename(columns={"user_country__country_code": "country_code"}, inplace=True)
        grouped_sum = df.groupby('country_code')['cost'].sum()
        grouped_description = df.groupby('country_code').apply(lambda x: x.drop(
            columns='country_code').to_dict(orient='records'))
        merged_df = pd.concat([grouped_description, grouped_sum], axis=1).rename(columns={0: "detail"}).reset_index()
        merged_df['country_name'] = merged_df['country_code'].map(self.country)
        return merged_df

    def reshaping(self):
        user_information = self.user.values()[0]
        df_expense = self._get_travel_expense_df()
        user_information['country'] = df_expense.to_dict('records')
        return user_information
