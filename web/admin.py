from django.contrib import admin
from .models import VideoP,Noticia,BlogEntry,Artistas,AlbumbyArtist,SongsbyAlbum,Category,Product
# Register your models here.runse



admin.site.register(Artistas)
admin.site.register(AlbumbyArtist)
admin.site.register(SongsbyAlbum)
admin.site.register(Product)
admin.site.register(Category)


@admin.register(VideoP)
class VAdmin(admin.ModelAdmin):
    fields = ('titulo','link')
    list_display = ('titulo','link')



@admin.register(BlogEntry)
class VBlog(admin.ModelAdmin):
    fields = ('titulo','cuerpo_noticia','linkV','imagen')
    list_display = ('titulo','linkV','cuerpo_noticia','imagen')


@admin.register(Noticia)
class NotAdmin(admin.ModelAdmin):
    fields = ('titular','cuerpo')
    date_hierarchy = 'date'
    list_display = ('titular','cuerpo')
