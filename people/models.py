from django.db import models
from cloudinary.models import  CloudinaryField
import cloudinary, cloudinary.api,cloudinary.uploader
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# Create your models here.
class Comment(models.Model):
    comment = models.CharField(max_length = 300)
class Profile(models.Model):
    bio = models.TextField(blank = True, null = True)
    dp = CloudinaryField('image', null = True, blank = True)
class Image(models.Model):
    image = CloudinaryField('image', null = True, blank = True)
    name = models.CharField(max_length = 30)
    caption = models.TextField(blank = True, null = True) #HTMLField()
    likes = models.IntegerField()
    comments = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    pub_date = models.DateTimeField(null = True, blank = True, auto_now_add=True)

    def save_image(self):
        self.save()
    def delete_image(cls, self):
        cls.objects.filter(id = self.id).delete()
    def update_image(self, image):
        Image.objects.filter(id = self.id).update(image = cloudinary.uploader.upload_resource(image))




