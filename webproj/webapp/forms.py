from django import forms


class ProductForm(forms.Form):
    prod_name = forms.CharField(label='Название', max_length=250)
    description = forms.CharField(label='Описание', widget=forms.Textarea)
    cost = forms.DecimalField(label='Цена', max_digits=8, decimal_places=2)
    prod_count = forms.IntegerField(label='Количество')
    image = forms.ImageField(label='Изображение', required=False)


class ImageForm(forms.Form):
    image=forms.ImageField()