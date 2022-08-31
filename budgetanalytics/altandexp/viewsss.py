from .models import Category, Expenditure, Transaction
from rest_framework.permissions import IsAuthenticated
from. serializers import ExpenditureSerializer, CodeWiseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum


from rest_framework import (
    viewsets,
    filters,
    parsers,
    generics,
)
from django_filters.rest_framework import DjangoFilterBackend
from url_filter.integrations.drf import DjangoFilterBackend


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['username', 'email']


class ExpenseViewsetView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    serializer_class = ExpenditureSerializer
    pagination_classes = [parsers.FormParser, parsers.MultiPartParser]
    filterset_fields = ['updated_at']

class CodeWiseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CodeWiseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','seven_digit_code']

 

# class SupplierWiseViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Expenditure.objects.values('item_supplier__name',).annotate(
#             ttl=Sum('total_exp'),
#             tds=Sum('total_tds'),
#             vds=Sum('total_vds'),
#             payable=Sum('total_paid'),
           
#         )
#     serializer_class = SupplierWiseSerializer
#     filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter,)
#     ordering_fields = ['total_exp', 'total_tds']
#     search_fields = ['updated_at', 'total_tds']

# class ErrorViewsetView(viewsets.ModelViewSet):
#     queryset = Expenditure.objects.all()
#     serializer_class = ErrorSerializer

   
    #   filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    # filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter,)
    # ordering_fields = ['start_date','start_date']
    # search_fields = ['start_date', 'end_date']
    # filterset_fields = {
        # annotate(
        #     ttl=Sum('total_exp'),
        #     tds=Sum('total_tds'),
        #     vds=Sum('total_vds'),
        #     payable=Sum('total_paid'), 
        # )
    #   'start_date':['gte', 'lte', 'exact', 'gt', 'lt'],
    #   'end_date':['exact'],
    #     }