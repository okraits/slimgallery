from django.db import models

class Folder(models.Model):
    caption = models.CharField(max_length=40)
    parentfolder = models.ForeignKey("self", blank=True, null=True)
    folderpath = models.CharField(max_length=255)
    isAlbum = models.BooleanField(default=False)
    resolutionX = models.IntegerField(max_length=4, default=1024)
    resolutionY = models.IntegerField(max_length=4, default=768)
    quality = models.IntegerField(max_length=3, default=80)
    
    def __unicode__(self):
        return self.caption
