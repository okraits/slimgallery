# coding=UTF-8
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from gallery.models import Folder
from django.conf import settings
from os import listdir, mkdir, system

def index(request, folder_id=None):
    context = {}
    if folder_id is not None:
        folder = Folder.objects.get(id__exact=folder_id)
    if folder_id is not None and folder is not None and folder.isAlbum:
        context['folder'] = folder
        picfolder_path = settings.SG_UPLOAD_PATH + folder.folderpath + "/"
        thumbfolder_path = settings.SG_THUMBS_PATH + folder.folderpath + "/"
        try:
            piclist = listdir(picfolder_path)
            context['piclist'] = piclist
        except (IOError, OSError):
            return HttpResponseNotFound("Path %s not found." % (picfolder_path))
        try:
            thumblist = listdir(thumbfolder_path)
            context['thumblist'] = thumblist
        except (IOError, OSError):
            # no thumbs found for this folder - we have to generate them
            return HttpResponseNotFound("This error should not happen ;-)")
    else:
        folder_list = Folder.objects.filter(parentfolder=folder_id)
        context['folder_list'] = folder_list
        if folder_id is not None:
            context['folder_id'] = folder_id
        for folder in folder_list:
            if folder.isAlbum:
                picfolder_path = settings.SG_UPLOAD_PATH + folder.folderpath + "/"
                thumbfolder_path = settings.SG_THUMBS_PATH + folder.folderpath + "/"
                try:
                    piclist = listdir(picfolder_path)
                    context['piclist'] = piclist
                except (IOError, OSError):
                    return HttpResponseNotFound("Path %s not found." % (picfolder_path))
                try:
                    thumblist = listdir(thumbfolder_path)
                    context['thumblist'] = thumblist
                except (IOError, OSError):
                    # no thumbs found for this folder - we have to generate them
                    try:
                        mkdir(thumbfolder_path)
                    except (IOError, OSError):
                        return HttpResponseNotFound("Error while creating thumbnail folder.")
                    for pic in piclist:
                        picpath = picfolder_path + pic
                        thumbpath = thumbfolder_path + "thumb_" + pic
                        retval = system("convert \"%s\" -resize %sx%s -quality %s \"%s\"" % (picpath, folder.thumbSizeX,
                                                                           folder.thumbSizeY,
                                                                           folder.thumbQuality, thumbpath))
                        if retval != 0:
                            return HttpResponseNotFound("Error while generating thumbnails.")
                    thumblist = listdir(thumbfolder_path)
                    context['thumblist'] = thumblist
    return render(request, 'gallery/index.html', context)
