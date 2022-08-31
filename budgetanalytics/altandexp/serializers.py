from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Expenditure, Transaction, Allotment
from django.db.models import Sum

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'invoice_date', 'amount', 'invoice_no','lp_no', 'receivevoucher_no')         
        

class ExpenditureSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)
   
      
    class Meta:
        model = Expenditure
        fields = ('id','updated_at','slug','expenditure_code','consumer_unit', 'item_supplier', 'created_by', 'title', 'transactions','get_prog_alts','get_totals','taxrate','get_income_tax','get_value_added_tax','get_paid_amount', 'get_children_length','is_cheque','vatrate','get_serial_no','get_page_no')  
        depth =  1



class AllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allotment
        fields = ('get_total_allotment')     

class CodeWiseSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Expenditure
        fields = ('__all__')
        depth =  1   

class CategoryWiseSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Category
        fields = ('transactions',)
    
class SupplierWiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenditure
        fields = ('__all__')
        depth =  1

class ErrorSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = Expenditure
        fields = ('title','get_tds_errors','get_vds_errors','get_expense_errors','get_cross_check_errors')  
        
  
     