# coding=UTF-8
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from gallery.models import Folder, Album

def index(request, album_id=None):
    folder_list = Folder.objects.all()
    album_list = Album.objects.all()
    if album_id is not None:
        context = {'folder_list': folder_list,
                   'album_list': album_list}
    else:
        context = {'folder_list': folder_list,
                   'album_list': album_list}
    return render(request, 'gallery/index.html', context)
