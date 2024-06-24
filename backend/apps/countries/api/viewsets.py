from core.settings import ALLOWED_CONTENT_TYPE

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from ..models import Countries, TravelExpense, VisitedCountries
from .export import UserDownloaderTemplateExport, UserExpenseExport
from .filters import TravelExpenseFilter
from .pagination import DataPagination
from .reshaping import UserTravelTrackReshaping
from .serializer import CountrySerializer, SingleUploadSerializer, TravelExpenseSerializer, VisitedCountriesSerializer
from .upload import CountryUpload, TravelExpenseUpload


class CountryViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Countries.objects.all().order_by('id')
    serializer_class = CountrySerializer
    allowed_content_type = ALLOWED_CONTENT_TYPE
    pagination_class = DataPagination

    def get_serializer_class(self):
        if self.action == 'upload':
            return SingleUploadSerializer
        else:
            return self.serializer_class

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['file'].content_type not in self.allowed_content_type:
            resp = {'title': 'File type error', 'detail': 'Wrong file type. It should be .xlsb or .xlsx'}
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        CountryUpload(serializer.validated_data).upload()
        resp = {'title': 'Success', 'detail': 'Upload succeeded !'}
        return Response(resp, status=status.HTTP_201_CREATED)


class VisitedCountriesViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = VisitedCountries.objects.all().order_by('id')
    serializer_class = VisitedCountriesSerializer


class TravelExpenseViewSet(viewsets.ModelViewSet):
    queryset = TravelExpense.objects.all().order_by('visited_date')
    serializer_class = TravelExpenseSerializer
    allowed_content_type = ALLOWED_CONTENT_TYPE
    pagination_class = DataPagination
    filterset_class = TravelExpenseFilter

    def get_serializer_class(self):
        if self.action == 'upload':
            return SingleUploadSerializer
        else:
            return self.serializer_class

    @action(detail=False, methods=['GET'])
    def summary(self, request, *args, **kwargs):
        data = UserTravelTrackReshaping(request.query_params['user']).reshaping()
        return Response(data)

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if request.data['file'].content_type not in self.allowed_content_type:
            resp = {'title': 'File type error', 'detail': 'Wrong file type. It should be .xlsb or .xlsx'}
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
        sheet_name = 'Travel_Expense'
        TravelExpenseUpload(serializer.validated_data, sheet_name).upload(user)
        resp = {'title': 'Success', 'detail': 'Upload succeeded !'}
        return Response(resp, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['PATCH'])
    def multi_update(self, request):
        queryset = self.get_queryset()
        instance = []
        for data in request.data.get('data'):
            obj = queryset.get(id=data['id'])
            obj.description = data['description']
            obj.cost = data['cost']
            obj.sightseeing = data['sightseeing']
            instance.append(obj)
        queryset.bulk_update(instance, ['description', 'cost', 'sightseeing'])
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def template(self, request):
        template = UserDownloaderTemplateExport(request.query_params['user'])
        return template.download_template()

    @action(detail=False, methods=['GET'])
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return UserExpenseExport(request.query_params['user'], serializer.data).download()
