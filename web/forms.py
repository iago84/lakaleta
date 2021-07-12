from django import forms
from django.core.mail import send_mail
from django.http import request

from web.models import Product, Encargo


class EncargoForm(forms.ModelForm):
    articulo=forms.Select(Product.objects.select_related().all())
    class meta():
        fields = ['articulo', 'nombre', 'calle', 'piso', 'puerta', 'CP', 'pais', 'email', 'precio']
        model=Encargo
