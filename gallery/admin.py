from django.contrib import admin
import gallery.models

class FolderAdmin(admin.ModelAdmin):
    list_display = ['caption', 'parentfolder', 'folderpath', 'isAlbum', 'thumbSizeX', 'thumbSizeY', 'thumbQuality']
    list_filter = ['isAlbum']
    search_fields = ['caption']

admin.site.register(gallery.models.Folder, FolderAdmin)
