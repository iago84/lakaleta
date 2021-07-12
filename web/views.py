import os
from builtins import super

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, get_object_or_404



from django.core.mail import send_mail
from django.http import HttpResponse, Http404, request, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, DetailView

from mysite import settings
from .models import Artistas, VideoP, Noticia, BlogEntry, AlbumbyArtist, SongsbyAlbum, Product,Category

# Create your views here.
from django.views.generic.base import TemplateView

class Index(TemplateView):
    template_name = "index.html"
    def get_context_data(self,  **kwargs):
        context=super(Index, self).get_context_data(**kwargs)
        context['ultimos_v']= VideoP.objects.all()[:3:-1]
        context['noticias']=Noticia.objects.all()[:5:-1]
        context['ment']=Artistas.objects.all()
        return context

class Escucha(TemplateView):
    template_name = "escucha.html"
    def get_context_data(self,  **kwargs):
        context= super(Escucha, self).get_context_data(**kwargs)
        context['Track10']=SongsbyAlbum.objects.all()[:10]
        context['Track20'] = SongsbyAlbum.objects.all()[10:20]
        context['Track30'] = SongsbyAlbum.objects.all()[20:30]
        return context

class Mixtapes(TemplateView):
    template_name = "mixtapes.html"

    def get_context_data(self, **kwargs):
        context = super(Mixtapes, self).get_context_data(**kwargs)
        context['all_albums'] = AlbumbyArtist.objects.all()

        return context

class Blog(TemplateView):
    template_name = "blog.html"
    def get_context_data(self,  **kwargs):
        context=super(Blog, self).get_context_data(**kwargs)
        context['BlogEnt']= BlogEntry.objects.all()[:5:-1]
        return context
class Videos(TemplateView):
    template_name = "videos.html"
    def get_context_data(self,  **kwargs):
        context=super(Videos, self).get_context_data(**kwargs)
        context['videos']= VideoP.objects.all()
        return context


class Artista(TemplateView):
    template_name = 'artist.html'

    def get_context_data(self, **kwargs):
        context=super(Artista, self).get_context_data(**kwargs)
        context['Albums']= AlbumbyArtist.objects.filter(Artist=kwargs['pk'])
        #context['Songs']=SongsbyAlbum.objects.filter(Artista=kwargs['pk'])
        context['Art']=Artistas.objects.filter(id=kwargs['pk'])
        return context

"""

class Encargo(CreateView):
    model = Encargo
    form_class = EncargoForm
    template_name = 'encargo.html'
    def form_valid(self, form):
        form.save()
        return self.form_valid()
    def save(self):
        if self.form_valid():
            self.send_email()
        return self.save()
    def send_email(self):
        if request.HttpRequest.method=='POST':
            form = Encargo(request.HttpRequest.POST)
            if form.is_valid():
                mensaje = form.namesur + ' ha pedido : ' + form.articulo + '\n' + 'a la dirección:  ' + form.calle + ' ' + form.piso + ' ' + form.puerta + ' ' + form.codp + ' ' + form.pais + '\n' + 'contacto en: ' + form.email
                send_mail('Encargo la kaleta', mensaje, 'lakaletaestudio@gmail.com',['lakeltaestudio@gmail.com', form.email], fail_silently=False, )

        pass



def LOGREG(request):
    formulario = nuevo_usuario(request)
    formulario2 = ingresar(request)
    usuario=request.user
    contexto = {'formulario': formulario, 'formulario2': formulario2, 'usuario':usuario}
    if request.user.is_anonymous():
        return render(request, 'logreg.html', contexto)
    else:
        return HttpResponseRedirect('/shop1')



"""


def product_list(request,category_slug=None ):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'product_list.html', {'category': category,
                  'categories': categories,'products': products})

def product_detail(request,category_slug, id, slug):
    category = None
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        
    
    return render(request, 'product_detail.html', {'category': category,'product': product})



"""
def actualizar_cookie (request, articulo, cantidad):
    actualizado = False
    usuario = request.user
    response = HttpResponseRedirect(request.GET.get('next'))
    print (request.GET.get('next'))
    if request.COOKIES.get('usuario'):
        carrito = request.COOKIES.get('usuario')
        print (carrito)
        if carrito != "" :
            lista = carrito.split(';')
            for element in lista:
                if element != "":
                    element = element.split('=')
                    if element[0] == articulo:
                        element[1] = int(cantidad)
                        actualizado = True
                    if element[1]!= 0:
                        carrito += str(element[0]) + "=" + str(element[1]) + ";"
        if actualizado == False :
            carrito += articulo + '=' + cantidad + ';'
        response.set_cookie(str(usuario), carrito)
    else:
        response.set_cookie(str(usuario), articulo + '=' + cantidad + ';')
    print (request.COOKIES)
    return response
"""
"""
def carrito(request):
    pagina = 'cart.html'
    usuario = request.user
    formulario = nuevo_usuario(request)
    formulario2 = ingresar(request)
    listado = []
    if request.COOKIES.get('usuario'):
        carrito = request.COOKIES[str(usuario)]
        if carrito != "" :
            art= Product.objects.all()
            lista = carrito.split(';')
            for element in lista:
                if element != "":
                    element = element.split('=')
                    for a in art:
                        if (str(element[0]) == str(a.id)):
                            total = int(element[1]) * int(a.price)
                            encontrado = {"Articulo": a.name,"cantidad": element[1], "Precio": a.price, "total": total, "Articulo": element[0]}
                            listado.append(encontrado)
    contexto = {'articulos' : listado, 'usuario':usuario, 'formulario':formulario, 'formulario2':formulario2}
    return render(request, pagina, contexto)

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            post_values = request.POST.copy()
            post_values['password'] = post_values['password1']
            request.POST = post_values
            ingresar(request)
            return HttpResponseRedirect('/shop1')
    else:
        formulario = UserCreationForm()
    return formulario

def ingresar(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    crear_cookie(request)
                    return HttpResponseRedirect('/shop1' )
            else:
                formulario = AuthenticationForm()
                return formulario
    else:
        formulario = AuthenticationForm()
    return formulario

def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


# views.py

class carrito(DetailView):
    model = Cart
    template_name = 'cart.html'
    def get_context_data(self, **kwargs):
        context=super(carrito, self).get_context_data(**kwargs)
        context['product']= Product.objects.filter(id=kwargs['pk'])


    def add_to_cart(request):
        self.product_id = Product.objects.get(id=Product.id)
        self.unit_price=Product.objects.get(unit_price=Product.unit_price,id=Product.id)
        cart = Cart(request)
        cart.add(self.product_id,self.unit_price, quantity)

    def remove_from_cart(request, product_id):
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.remove(product)

    def get_cart(request):
        return render_to_response('cart.html', dict(cart=Cart(request)))

"""