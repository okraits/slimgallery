from django.contrib import admin
import gallery.models

admin.site.register(gallery.models.Folder)

admin.site.register(gallery.models.Album)
