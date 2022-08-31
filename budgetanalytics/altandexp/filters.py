import django_filters
from django_filters import DateFilter, CharFilter
from .models import Allotment, Expenditure, Transaction

    

class ExpFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='updated_at' , lookup_expr='gte')
    end_date = DateFilter(field_name='updated_at' , lookup_expr='lte')
    # title = CharFilter(lookup_expr='iexact', field_name='title')
    
    class Meta:
        model = Expenditure
        fields =['expcode','itemsupplier']
     