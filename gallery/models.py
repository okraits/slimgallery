from django.db import models

class Folder(models.Model):
    caption = models.CharField(max_length=40)
    parentfolder = models.ForeignKey("self", blank=True, null=True)
    
    def __unicode__(self):
        return self.caption

class Album(models.Model):
    caption = models.CharField(max_length=40)
    parentfolder = models.ForeignKey(Folder, blank=True, null=True)
    resolutionX = models.IntegerField(max_length=4, default=1024)
    resolutionY = models.IntegerField(max_length=4, default=768)
    path = models.CharField(max_length=120)
    
    def __unicode__(self):
        return self.caption
