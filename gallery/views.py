# coding=UTF-8
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from gallery.models import Folder
from django.conf import settings
from os import listdir, mkdir, system

# this should be replaced by a media path
UPLOAD_PATH = "user/"
THUMBS_PATH = "thumbs/"

def index(request, folder_id=None):
    folder_list = Folder.objects.filter(parentfolder=folder_id)
    
    if folder_id is not None:
        # check only folders which have this folder as parentfolder
        pass
    else:
        # check only folders which have no parentfolder
        for folder in folder_list:
            if folder.isAlbum:
                picfolder_path = settings.STATICFILES_DIRS[0] + UPLOAD_PATH + folder.folderpath + "/"
                thumbfolder_path = settings.STATICFILES_DIRS[0] + THUMBS_PATH + folder.folderpath + "/"
                try:
                    piclist = listdir(picfolder_path)
                except (IOError, OSError):
                    return HttpResponseNotFound("Path %s not found." % (picfolder_path))
                try:
                    thumblist = listdir(thumbfolder_path)
                except (IOError, OSError):
                    try:
                        mkdir(thumbfolder_path)
                    except (IOError, OSError):
                        return HttpResponseNotFound("Error while creating thumbnail folder.")
                    for pic in piclist:
                        picpath = picfolder_path + pic
                        thumbpath = thumbfolder_path + "thumb_" + pic
                        retval = system("convert \"%s\" -resize %sx%s -quality %s \"%s\"" % (picpath, folder.resolutionX,
                                                                           folder.resolutionY,
                                                                           folder.quality, thumbpath))
                        if retval != 0:
                            return HttpResponseNotFound("Error while generating thumbnails.")
    
    
    if folder_id is not None:
        context = {'folder_list': folder_list,
                   'folder_id': folder_id}
    else:
        context = {'folder_list': folder_list}
    return render(request, 'gallery/index.html', context)
