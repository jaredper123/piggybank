from django import forms
from .models import MoneyRequest

class MoneyRequestForm(forms.ModelForm):
    class Meta:
        model = MoneyRequest
        fields = ['amount', 'reason', 'category']
