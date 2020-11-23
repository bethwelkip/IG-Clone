from django.db import models
from cloudinary.models import  CloudinaryField
import cloudinary, cloudinary.api,cloudinary.uploader
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# Create your models here.
class Following(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)

class InstaPhotos(models.Model):
    name = models.CharField(max_length = 20)
    image = CloudinaryField('image', null = True, blank = True)
class Comment(models.Model):
    comment = models.CharField(max_length = 300)
class Profile(models.Model):
    bio = models.TextField(blank = True, null = True)
    dp = CloudinaryField('image', null = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    following = models.ManyToManyField(Following)
    def save_profile(self):
        self.save()
    def delete_profile(self):
        Profile.objects.filter(id = self.id).delete()
    def update_profile(self, dp = None, bio = None):
        if dp is not None:
            Profile.objects.filter(id = self.id).update(dp = cloudinary.uploader.upload_resource(dp))
        if bio is not None:
            Profile.objects.filter(id = self.id).update(bio = bio)

    @classmethod
    def search_users(cls, search_term):
        users = [user for user in User.objects.all()]
        user = User.objects.filter(username__icontains = search_term).all()
        print(users)
        return user
class Image(models.Model):
    image = CloudinaryField('image', null = True)
    name = models.CharField(max_length = 30)
    caption = models.TextField() #HTMLField()
    likes = models.IntegerField(blank = True,null = True)
    comments = models.ManyToManyField(Comment)
    profile = models.ForeignKey(Profile, null = True, blank = True, on_delete=models.DO_NOTHING)
    pub_date = models.DateTimeField(null = True, blank = True, auto_now_add=True)
# image, name, caption, likes, profile
    def save_image(self):
        self.save()
    def delete_image(self):
        Image.objects.filter(id = self.id).delete()
    def update_image(self, caption, image):
        if image is not None:
            img = Image.objects.get(id = self.id)
            img.caption = caption
            img.save()
            img.image = cloudinary.uploader.upload_resource(image)
            img.save()
            return img




