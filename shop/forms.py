from django import forms
from shop.models import File
class FileForm(forms.ModelForm):
    class Meta:
        model = File 
        fields = ('document',)

