from asyncio.windows_events import NULL
from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import datetime
from django.conf import settings
import decimal
from decimal import Decimal
from django.db.models import Sum
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text= _("Required and Unique"),
        max_length=255,
        unique=True,
    )  
    slug = models.SlugField(
        verbose_name=_("Budget Code Slug"),
        max_length=255,
        unique=True,
    )
    seven_digit_code = models.IntegerField(blank=False)
    is_general_or_spl= models.BooleanField(default=True)
    heading = models.CharField(max_length=255, blank= False)
    voucher_head = models.CharField(max_length=3, blank=False)
    total_alloted_amounts = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00,)
    total_refund_amounts = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00,)
    progress_of_allotments = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00, verbose_name=_("Progressive Allotment"))
    progress_of_expenses = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00, verbose_name=_("Progressive Expense"))
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00, verbose_name=_("Unspent Balance"))


    def get_allotment_totals(self):
        sub_total = 0
        sub_total = Allotment.objects.filter(allotment_code=self).aggregate(total=Sum('alloted_amount'))['total'] or 0.00
        return Decimal(sub_total)

    def get_refunds_totals(self):
        refunds_total = 0
        refunds_total = Refund.objects.filter(refund_code=self).aggregate(total=Sum('refund_amount'))['total'] or 0.00
        return Decimal(refunds_total)
     

    def get_current_prog_of_allotment(self):
        current_allotment__prg = 0
        current_allotment__prg = self.get_allotment_totals() - self.get_refunds_totals()
        return Decimal(current_allotment__prg)

    def get_current_prog_of_expense(self):
        sub_expenses = 0
        sub_expenses = Expenditure.objects.filter(expenditure_code=self).aggregate(total=Sum('total_exp'))['total'] or 0.00
        return Decimal(sub_expenses)

    def your_current_balance(self):
        c_balance= 0
        c_balance = self.get_current_prog_of_allotment()- self.get_current_prog_of_expense()
        return Decimal(c_balance)

  

    def save(self, *args,**kwargs):
        
        self.total_alloted_amounts = self.get_allotment_totals()
        self.total_refund_amounts = self.get_refunds_totals()
        self.progress_of_allotments = self.get_current_prog_of_allotment()
        self.progress_of_expenses = self.get_current_prog_of_expense()
        self.current_balance = self.your_current_balance()
        ttl_allotted_prog = self.get_current_prog_of_allotment()
        ttl_refunded_amount  = self.get_refunds_totals()
        refunds_err_msg = f"Total Refund amount must be less than tatal Proggress of Allotments for respective Budget Code.Check."
        refunds_err_msg = f"Your Expense must be less than allotment."
        the_current_balance = self.your_current_balance()
            
        if ttl_refunded_amount> ttl_allotted_prog:
            raise ValidationError(f" {refunds_err_msg}  || Check  {self.name}  ")
        elif the_current_balance <0 :
            raise ValidationError(f" {refunds_err_msg}  || Check  {self.name}  ")
        # self.current_balance.save()
        return super(Category,self).save(*args,**kwargs)


    class Meta:
        verbose_name = _('Budget Code')
        verbose_name_plural = _('Budget Codes')

    def __str__(self):
        return self.name

  
class Consumerunit(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=25, unique =True)
    parent_office = models.CharField(max_length=50, db_index=True)

    class Meta:
        verbose_name = _("Consumer Unit Name")
        verbose_name_plural = _("Consumer Unit Names")

    def __str__(self):
       return self.name

class Procurementprovider(models.Model):
    name = models.CharField(
    verbose_name=_("Name"),
    help_text= _("Required"),
    max_length=255,
    blank=False,
    ) 
    slug = models.SlugField(max_length=255, unique =True)
    address = models.CharField(max_length=255,)
    tin_no = models.CharField(max_length=13, blank=False,)
    vat_no = models.CharField(max_length=13, blank=False,)
    regpage_no = models.CharField(max_length=13, blank=False,)
    is_registered = models.BooleanField(default=True)
    reg_date = models.DateField()
    

    class Meta:
        verbose_name = _("Procurement Provider Name")
        verbose_name_plural = _("Procurement Provider Names")

    def __str__(self):
       return self.name


    def get_ser_no(self):
        len_of_sup = 0
        len_of_sup = len(Expenditure.objects.filter(item_supplier=self))
        return Decimal(len_of_sup)

class Allotment(models.Model):
    allotment_code = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="allotments", verbose_name=_("Budget Codes"))
    alloted_unit = models.ForeignKey(Consumerunit, on_delete=models.CASCADE, verbose_name=_("For Which Office"))
    title = models.CharField(
        verbose_name=_("title"),
        help_text="Required",
        max_length=255)

    slug = models.SlugField(max_length=255, unique=True)
    alloted_on = models.DateField(verbose_name=_("Allotment Date"))
    alloted_auth = models.CharField(max_length=70, default="23.03.2600.039.51.001.21.000/ A", verbose_name=_("Vide Ltr Reference"))
    alloted_amount = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00,)
   
    class Meta:
        verbose_name = 'Allotment'
        verbose_name_plural = 'Allotment'
        ordering = ('allotment_code',)
          
    def __str__(self):
        return self.title

class Refund(models.Model):
    refund_code = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="refund_allotments", verbose_name=_("Budget Codes"))
    refund_unit = models.ForeignKey(Consumerunit, on_delete=models.CASCADE, verbose_name=_("For Which Office"))
    title = models.CharField(
        verbose_name=_("title"),
        help_text="Required",
        max_length=255)

    slug = models.SlugField(max_length=255, unique=True)
    refund_on = models.DateField(verbose_name=_("Trdunded Date"))
    refund_auth = models.CharField(max_length=70, default="23.03.2600.039.51.001.21.000/ A", verbose_name=_("Vide Ltr Reference"))
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00,)
    approved = models.BooleanField("Approved", default=False,)
   
    class Meta:
        verbose_name = 'Refund Allotment'
        verbose_name_plural = 'Refund Allotments'
        ordering = ('refund_code',)
          
    def __str__(self):
        return self.title

class Expenditure(models.Model):
    title = models.CharField(
    verbose_name=_("title"),
    help_text="Required",
    max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    expenditure_code = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="alt_exp", verbose_name=_("Budget Codes"))
    consumer_unit = models.ForeignKey(Consumerunit, on_delete=models.RESTRICT, verbose_name=_("Consumer Office Name"))
    item_supplier = models.ForeignKey(Procurementprovider, on_delete=models.RESTRICT, verbose_name=_("Select Your Supplier"))
    is_cheque = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    taxrate = models.DecimalField(blank=False, max_digits=4, decimal_places=2,verbose_name=_("Income TAX Rate"), default=0)
    complex_tax = models.DecimalField(blank=False, max_digits=8, decimal_places=2,verbose_name=_("Complex TAX Amount"), default=0)
    vatrate = models.DecimalField(blank=False, max_digits=4, decimal_places=2,verbose_name=_("VAT Rate"), default=0)
    complex_vat = models.DecimalField(blank=False, max_digits=8, decimal_places=2,verbose_name=_(" Complex VAT Amount"), default=0)
    created_at = models.DateField(_("Created Date"), default=datetime.date.today)
    updated_at = models.DateField(_("Update Date"), default=datetime.date.today)
    total_allotments_codewise = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00 ,verbose_name=_("Progress of Allotments"),  help_text="Automated. Do not insert any value here",)
    total_expense_codewise = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00 ,verbose_name=_("Progress of Expense"),  help_text="Automated. Do not insert any value here",)
    total_exp = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00 ,verbose_name=_("Total of Single Bills"),  help_text="Automated. Do not insert any value here",)
    total_tds = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00 ,verbose_name=_("Tax deducted at Source"),  help_text="Automated. Do not insert any value here",)
    total_vds = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00 ,verbose_name=_("VAT deducted at Source"),  help_text="Automated. Do not insert any value here",)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00 ,verbose_name=_("Payable Amount of the Bill"),  help_text="Automated. Do not insert any value here",)
    

    class Meta:
        verbose_name = 'Expenditure'
        verbose_name_plural = 'Expenditures'
    
   
    def __str__(self):
        return (f"{self.title} & tk {self.total_exp}" )  
  
    def get_prog_alts(self):
        net_total = self.expenditure_code.get_current_prog_of_allotment()
        return net_total

    def get_totals(self):
        totals = 0
        net_total = 0
        for x in Transaction.objects.filter(invoices=self):
            totals += x.amount
            net_total = Decimal(totals)
        return net_total

    def get_income_tax(self):
        tax = 0
        tax_rate = self.taxrate
        tax_amount = self.complex_tax
        if tax_rate==0 and tax_amount==0:
           return Decimal(tax)
        elif tax_rate<0 or tax_amount<0:
            return Decimal(tax)
        elif tax_rate>0 and tax_amount>0:
            return Decimal(tax)
        elif tax_rate >0 and tax_amount==0:
            income_tax = self.get_totals()*tax_rate/100
            return Decimal(income_tax)
        elif tax_rate ==0 and tax_amount>0:
            return Decimal(tax_amount)
        else:
            return Decimal(tax)

    def get_value_added_tax(self):
        vat = 0
        vat_rate = self.vatrate
        vat_amount = self.complex_vat
        if vat_rate==0 and vat_amount==0:
           return Decimal(vat)
        elif vat_rate<0 or vat_amount<0:
            return Decimal(vat)
        elif vat_rate>0 and vat_amount>0:
            return Decimal(vat)
        elif vat_rate >0 and vat_amount==0:
            vat_is = self.get_totals()*vat_rate/100
            return Decimal(vat_is)
        elif vat_rate ==0 and vat_amount>0:
            return Decimal(vat_amount)
        else:
            return Decimal(vat)

    def get_tds_errors(self):
        get_errors_msg = 'No error in TAX'
        negative_tds_msg = f" Negative Value as TAX is not accepted. Correction is required for {self.taxrate} or  {self.complex_tax}"
        tds_conflict_msg = f"Insert tolat TAX amount or tax rate. Do not insert both. Insert {self.taxrate} or  {self.complex_tax}"

        tax_rate = self.taxrate
        tax_amount = self.complex_tax
        
        if tax_rate<0 or tax_amount<0:
            raise ValidationError(negative_tds_msg)
        elif tax_rate>0 and tax_amount>0:
            raise ValidationError(tds_conflict_msg)
        else:
            return get_errors_msg

    def get_vds_errors(self):
        get_succress_msg = 'No error in VAT'
        negative_msg = f" Negative Value as VAT is not accepted. Insert positive value of {self.vatrate} or  {self.complex_vat}"
        tds_conflict_msg = f"Insert tolat VAT amount or vat rate. Do not insert both. Insert {self.vatrate} or  {self.complex_vat}"
        vat_rate = self.vatrate
        vat_amount = self.complex_vat

        if vat_rate<0 or vat_amount<0:
            raise ValidationError(negative_msg)
        elif vat_rate>0 and vat_amount>0:
            raise ValidationError(tds_conflict_msg)
        else:
            return get_succress_msg


    def get_expense_errors(self):
        expense_err_msg = "Total Expense amount must be less than tatal Allotments for each Budget Code. Please add Allotment or expense it after getting allotment"
        get_valid_exp_msg = 'Expense Successful'
        a = self.expenditure_code.get_current_prog_of_expense()
        b = self.expenditure_code.get_current_prog_of_allotment()
        if a > b:
            raise ValidationError(f"{expense_err_msg} .You are trying to expense {a} from {b}. Please check {self.expenditure_code}")
        return get_valid_exp_msg

    def get_paid_amount(self):
        net_payable = 0
        ttl_amount = self.get_totals()
        sum_of_it_vat = self.get_income_tax() + self.get_value_added_tax()
        net_payable = ttl_amount - sum_of_it_vat
        return Decimal(net_payable)

    def get_cross_check_errors(self):
       
        recheck_msg = f" The sum of IT, VAT and paid amount is greater than gross subtotal of bills.  IT {self.get_income_tax()} + VAT  {self.get_value_added_tax()} +  Paid {self.get_paid_amount()}  =  Gross {self.get_totals()} ??? Please check {self.expenditure_code}"

        it_vat_paid_amount = self.get_income_tax() + self.get_value_added_tax() + self.get_paid_amount()

        if  it_vat_paid_amount == self.get_totals():
            return (f" Success ")
        else:
            raise ValidationError(f" Sorry !  ||  Please Check your Expense  ||  {self.title}  ||   {recheck_msg}")


    def get_children(self):
        return Transaction.objects.filter(invoices=self)

    def get_children_length(self):
        get_len = len(Transaction.objects.filter(invoices=self))
        return Decimal(get_len)

    def get_serial_no(self):
        purchase_times = 0
        purchase_times = self.item_supplier.get_ser_no()
        return Decimal(purchase_times)

    def get_page_no(self):
        get_page_no = 0
        get_page_no = Decimal(self.item_supplier.regpage_no)
        get_length= Decimal(self.get_serial_no())
        if  get_length > 1:
            return get_page_no +1
        elif  get_length > 2:
            return get_page_no +2
        elif get_length > 3:
            return get_page_no +3
        return Decimal(get_page_no)


    def save(self, *args, **kwargs):
        self.total_allotments_codewise = self.expenditure_code.get_current_prog_of_allotment()
        self.total_expense_codewise = self.expenditure_code.get_current_prog_of_expense()
        self.total_exp = self.get_totals()
        self.total_tds = self.get_income_tax()
        self.total_vds = self.get_value_added_tax()
        self.total_paid = self.get_paid_amount()
        total_current_balance = self.expenditure_code.your_current_balance()
        exp_of_this_bill = self.get_totals()

        if self.get_paid_amount()<0:
            raise ValidationError(f"Please Check your Expense.(IT) {self.get_income_tax()} + (VAT) {self.get_value_added_tax()} + (Paid) {self.get_paid_amount()} is not eqaul to  gross amount {self.get_totals()}")
        
        elif exp_of_this_bill > total_current_balance:
            raise ValidationError(f"Insufficient Balance. Balance is balane is {total_current_balance} and you are trying to expense {exp_of_this_bill} ")
        return super().save(*args, **kwargs)

class Transaction(models.Model):
    invoices= models.ForeignKey(Expenditure, on_delete=models.CASCADE, related_name="transactions")
    invoice_no = models.CharField(max_length=30)
    invoice_date = models.DateField()
    lp_no = models.CharField(max_length=6)
    receivevoucher_no = models.CharField(max_length=8)
    amount = models.DecimalField(max_digits=12, decimal_places=2) 

    class Meta:
        verbose_name = _("Invoice Detail")
        verbose_name_plural = _("Invoice Details")
        unique_together = ('invoices', 'invoice_no')
