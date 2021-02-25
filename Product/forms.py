from django import forms
from .models import *

class Category_Forms(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class Product_Forms(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name' : 'Product Name'
        }
    
    def __init__(self, *arg, **kwarg):
        super(Product_Forms, self).__init__(*arg, **kwarg)
        self.fields['category'].empty_label = "Select"

