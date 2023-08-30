from django import forms
from .models import Users

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = '__all__'  # You can specify the fields you want to include here if not all.
        # exclude_fields = [field.name for field in Users._meta.fields if field.name.startswith('sd')]
        # fields = [field.name for field in Users._meta.fields if field.name not in exclude_fields]
        fields = list()
        for field in Users._meta.fields:
            if field.name.startswith("sd"):
                continue
            fields.append(field.name)