from django.contrib import admin
from . import views
from django.urls import path
from altandexp.views import  MasterViewsetView, CodeWiseViewSetView, SupplierViewSetView, ErrorViewsetView
from rest_framework import routers, viewsets

app_name = 'budget'

router = routers.DefaultRouter()
router.register(r'exp', MasterViewsetView, basename='expense')
router.register(r'codes', CodeWiseViewSetView, basename='codes')
router.register(r'category', CodeWiseViewSetView, basename='cat')
router.register(r'supplier', SupplierViewSetView, basename='supplier')
router.register(r'error', ErrorViewsetView, basename='error_message')


# urlpatterns = router.urls



urlpatterns = [
    path('index', views.get_expense, name='index'),
   ] + router.urls

