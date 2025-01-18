from django import forms
from .models import Address


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'first_name', 'last_name',
            'province', 'city', 'detailed_address',
            'postal_code', 'plaque', 'recipient_phone',
            'note'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].required = True
        self.fields['city'].required = True
        self.fields['detailed_address'].required = True
        self.fields['postal_code'].required = True
        self.fields['plaque'].required = True
        self.fields['recipient_phone'].required = True
        self.fields['note'].required = False

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

