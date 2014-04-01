# coding=UTF-8
from django.template import loader, Context
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from gallery.models import Folder
from django.conf import settings
from os import listdir, makedirs, system

def getPicturesFromFolder(folder, context):
    # generate path to the top folder
    current = folder
    root_path = ""
    while current.parentfolder is not None:
        root_path = current.parentfolder.folderpath + "/" + root_path
        current = current.parentfolder
    # put paths together
    picfolder_path = settings.SG_UPLOAD_PATH + root_path + folder.folderpath + "/"
    thumbfolder_path = settings.SG_THUMBS_PATH + root_path + folder.folderpath + "/"
    # path strings for templates
    html_picfolder_path = "user/" + root_path + folder.folderpath + "/"
    html_thumbfolder_path = "thumbs/" + root_path + folder.folderpath + "/"
    context['picfolder_path'] = html_picfolder_path
    context['thumbfolder_path'] = html_thumbfolder_path
    # get piclist and thumblist
    try:
        piclist = listdir(picfolder_path)
        piclist.sort()
        context['piclist'] = piclist
    except (IOError, OSError):
        return False, "Path %s not found." % (picfolder_path)
    try:
        thumblist = listdir(thumbfolder_path)
        thumblist.sort()
        # compare pics and thumbs and check if we need to create thumbs
        if len(piclist) != len(thumblist):
            for pic in piclist:
                for thumb in thumblist:
                    if pic in thumb:
                        break
                    else:
                        # no thumb for this pic found in thumblist
                        if thumblist.index(thumb) == (len(thumblist) - 1):
                            # create thumb
                            picpath = picfolder_path + pic
                            thumbpath = thumbfolder_path + "thumb_" + pic
                            retval = system("convert \"%s\" -resize %sx%s -quality %s \"%s\"" % (picpath, folder.thumbSizeX,
                                                                               folder.thumbSizeY,
                                                                               folder.thumbQuality, thumbpath))
                            if retval != 0:
                                return False, "Error while generating thumbnails."
        thumblist = listdir(thumbfolder_path)
        thumblist.sort()
        context['thumblist'] = thumblist
        return True, ""
    except (IOError, OSError):
        # no thumbfolder found for this picfolder => create it
        try:
            makedirs(thumbfolder_path)
        except (IOError, OSError):
            return False, "Error while creating thumbnail folder."
        for pic in piclist:
            # create thumbs for this picfolder
            picpath = picfolder_path + pic
            thumbpath = thumbfolder_path + "thumb_" + pic
            retval = system("convert \"%s\" -resize %sx%s -quality %s \"%s\"" % (picpath, folder.thumbSizeX,
                                                               folder.thumbSizeY,
                                                               folder.thumbQuality, thumbpath))
            if retval != 0:
                return False, "Error while generating thumbnails."
        thumblist = listdir(thumbfolder_path)
        thumblist.sort()
        context['thumblist'] = thumblist
        return True, ""

def index(request, folder_id=None):
    context = {}
    if folder_id is not None:
        folder = Folder.objects.get(id__exact=folder_id)
    if folder_id is not None and folder is not None:
        context['folder'] = folder
    if folder_id is not None and folder is not None and folder.isAlbum:
        # folder is valid and an album => get pic- and thumblist
        retval, errorstring = getPicturesFromFolder(folder, context)
        if not retval:
            return HttpResponseNotFound("%s" % (errorstring))
    else:
        # folder is not an album => get folderlist
        folder_list = Folder.objects.filter(parentfolder=folder_id)
        context['folder_list'] = folder_list
    return render(request, 'gallery/index.html', context)

def browse(request, folder_id=None, image=None):
    context = {}
    if folder_id is not None:
        folder = Folder.objects.get(id__exact=folder_id)
        if folder is not None and folder.isAlbum:
            # render a page with a single image in full size
            context['folder'] = folder
            retval, errorstring = getPicturesFromFolder(folder, context)
            if not retval:
                return HttpResponseNotFound("%s" % (errorstring))
            if not image in context['piclist']:
                return HttpResponseNotFound("Image not found in folder.")
            context['image'] = image
            # store names of the first and last image to jump to the beginning and the end:
            context['first'] = context['piclist'][0]
            context['last'] = context['piclist'][-1]
            # store names of the previous and next image to jump forth and back:
            if context['piclist'].index(image) != 0:
                context['previous'] = context['piclist'][context['piclist'].index(image) - 1]
            else:
                context['previous'] = context['piclist'][0]
            if context['piclist'][-1] != image:
                context['next'] = context['piclist'][context['piclist'].index(image) + 1]
            else:
                context['next'] = context['piclist'][-1]
            return render(request, 'gallery/browse.html', context)
        else:
            return HttpResponseNotFound("Folder does not exist or is not an album.")
    else:
        return HttpResponseNotFound("No folder given.")
