
from mysite import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.contrib import admin

from django.http import request


from web.views import Index, Escucha, Mixtapes, Blog, Videos, Artista, product_detail, product_list


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^$', Index.as_view(), name="Index"),
    url(r'^escucha/', Escucha.as_view(), name="Escucha"),
    url(r'^mixtapes/', Mixtapes.as_view(), name="Mixtapes"),
    url(r'^blog/$', Blog.as_view(), name="Blog"),
    url(r'^videos/$', Videos.as_view(), name='Videos'),
    url(r'^artista/(?P<pk>\d+)', Artista.as_view(), name='ArtistaDetail'),
    url(r'^shop/(?P<category_slug>[-\w]+)/$', product_list, name='product_list_by_category'),
    url(r'^shop/(?P<category_slug>[-\w]+)/(?P<id>\d+)/(?P<slug>[-\w]+)/$', product_detail, name='product_detail'),

    #Root url

    url(r'^shop/', product_list, name='shop'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
