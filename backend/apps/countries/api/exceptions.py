from rest_framework.exceptions import APIException


class ErrorDataType(APIException):
    status_code = 400
    default_detail = 'There must be some invalid data type in the dataframe.'
    default_code = 'Bad Request'

    def __init__(self, message=default_detail):
        self.detail = {'title': 'Error', 'detail': message}


class ErrorHeaders(APIException):
    status_code = 400
    default_detail = 'There are wrong headers in this file.'
    default_code = 'Bad Request'

    def __init__(self, message=default_detail):
        self.detail = {'title': 'Error', 'detail': message}


class SheetDoesNotExists(APIException):
    status_code = 400
    default_detail = 'The Sheet Name Does not exists !'
    default_code = 'Bad Request'

    def __init__(self, message=default_detail):
        self.detail = {'title': 'Error', 'detail': message}


class CountryNameWrong(APIException):
    status_code = 400
    default_detail = 'The Country Names are wrong. Please check again!'
    default_code = 'Bad Request'

    def __init__(self, message=default_detail):
        self.detail = {'title': 'Error', 'detail': message}
