from django.forms import ModelForm, BaseModelFormSet
from main_crm.models import Company, Phone, Email
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('slug',)
        widgets = {
            'description': CKEditorUploadingWidget(),
        }


class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        exclude = ('user',)


class EmailForm(ModelForm):
    class Meta:
        model = Email
        exclude = ('user',)
