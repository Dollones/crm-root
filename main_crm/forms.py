from django.forms import ModelForm
from main_crm.models import Company


class CompanyForm(ModelForm):

    class Meta:
        model = Company
        exclude = ('slug',)
