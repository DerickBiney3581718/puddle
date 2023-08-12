from django import forms
from .models import Item

class NewItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = [ 'category','name', 'description', 'price',  'image', ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }
        
class EditItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = [ 'name', 'description', 'price',  'image','is_sold' ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }