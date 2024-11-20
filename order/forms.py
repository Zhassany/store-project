from django import forms
from .models import Order

class OrderRegisterForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address']
        widgets = {
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'})
        }
