

# Create your models here.

from django import forms
from django.db import models
from django.db.models import CASCADE
from django.urls import reverse
from embed_video.fields import EmbedVideoField


class Artistas(models.Model):
    name=models.CharField('Mención',max_length=100)
    descrip=models.TextField('Descripción')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('ArtistaDetail',args=[self.id])

class AlbumbyArtist(models.Model):
    Album_title=models.CharField('Título del álbum',max_length=500)
    Artist=models.ForeignKey(Artistas,on_delete=models.CASCADE)
    zipfile = models.FileField(upload_to='media/')
    precio = models.IntegerField(default=10)
    sell = models.BooleanField(default=True)
    def __str__(self):
        return self.Album_title


class SongsbyAlbum(models.Model):
    Song_title=models.CharField('Título de la canción',max_length=500)
    Album=models.ForeignKey(AlbumbyArtist,on_delete=models.CASCADE,blank=True,null=True)
    Artista=models.ForeignKey(Artistas, on_delete=models.CASCADE,blank=True,null=True)
    file = models.FileField(upload_to='media/')

    def __str__(self):
        return self.Song_title

class Noticia(models.Model):
    titular =models.CharField('Titular',max_length=200)
    cuerpo =models.TextField('Cuerpo')
    date= models.DateField('Fecha',auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.titular

class VideoP(models.Model):
    link = EmbedVideoField()
    titulo=models.CharField('Titulo',max_length=80)

    def __str__(self):
        return self.titulo


class BlogEntry(models.Model):
    titulo=models.CharField('Titulo',max_length=200)
    imagen= models.ImageField('Imagen',upload_to='media/',blank=True,null=True)
    linkV=EmbedVideoField(blank=True, null=True)
    date = models.DateField('Fecha', auto_now_add=True, blank=True, null=True)
    cuerpo_noticia=models.TextField('Cuerpo',blank=True,null=True)

    def __str__(self):
        return self.titulo


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products',null=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=False,null=False)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField('Precio', decimal_places=2, max_digits=4, null=False)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.category.slug,self.id, self.slug])





"""
class Cart(models.Model):
    product = models.CharField('Producto',max_length=200)
    unit_price=models.DecimalField
    quantity =models.IntegerField
    total=models.DecimalField



    def remove(self, product):
        pass


class Encargo(models.Model):
    articulo=models.ManyToOneRel(Product, on_delete=False,to=Cart,field_name=Product.name)
    nombre=models.CharField('Nombre',max_length=90)
    calle=models.TextField('Calle')
    piso=models.IntegerField('Piso')
    puerta=models.CharField('Puerta', max_length=2)
    CP=models.CharField('CP',max_length=10)
    pais=models.CharField('Pais' ,max_length=30)
    email=models.EmailField('Email')
    precio=models.FloatField('Precio')

"""






