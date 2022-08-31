from .models import Category, Expenditure, Transaction
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from. serializers import ExpenditureSerializer, CodeWiseSerializer, SupplierWiseSerializer,ErrorSerializer,CategoryWiseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models import F, Q
from datetime import datetime

from rest_framework import (
    viewsets,
    filters,
    parsers,
    generics,
)
from django_filters.rest_framework import DjangoFilterBackend
# from url_filter.integrations.drf import DjangoFilterBackend

def get_expense(request):
    expense_details = Expenditure.objects.all()
    context = {
        'expense_details':expense_details,
    }
    return render(request,'exp/index.html', context)

class MasterViewsetView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,)
    serializer_class = ExpenditureSerializer
    ordering_fields = ['expenditure_code',]
    filterset_fields = {'updated_at': ['gte', 'lte'],}

class CodeWiseViewSetView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Expenditure.objects.all()
    serializer_class = CodeWiseSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    filterset_fields = {'updated_at': ['gte', 'lte'],}

class SupplierViewSetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Expenditure.objects.all()
    serializer_class = SupplierWiseSerializer

class CatgoryViewSetView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryWiseSerializer

class ErrorViewsetView(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    serializer_class = ErrorSerializer
   


   

