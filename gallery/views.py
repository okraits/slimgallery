# coding=UTF-8
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from gallery.models import Folder

def index(request, folder_id=None):
    folder_list = Folder.objects.all()
    if folder_id is not None:
        context = {'folder_list': folder_list,
                   'folder_id': folder_id}
    else:
        context = {'folder_list': folder_list}
    return render(request, 'gallery/index.html', context)
