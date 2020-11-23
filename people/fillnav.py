from .models import Image, Profile, Comment, InstaPhotos
import random
from django.contrib.auth.models import User
from random import shuffle
import cloudinary, cloudinary.api,cloudinary.uploader
import os
def initialize():
    cwd = os.getcwd()
    comments = ["soo cute  ","Couldn't be me haha", "wyd lol", "hii", "this cracked me up haha"]
    profiles = [("bethwel", "bethu's clique"),("moha", "moha's antics")]

    for username, profile in profiles:
        prof = Profile(bio = profile, user = User.objects.get(username = username))
        prof.dp = cloudinary.uploader.upload_resource(f'{cwd}/media/memes/{2}.JPG')
        prof.save()

    for comment in comments:
        com = Comment(comment = comment)
        com.save()
    profs = [prof for prof in Profile.objects.all()]
    coms = [com for com in Comment.objects.all()]
    for i in range(7):
        img = Image(name =f'Post number {i}',caption = " just a favourite meme",likes = 0, profile = random.choice(profs))
        img.save()
        img.comments.add(random.choice(coms))
        img.comments.add(random.choice(coms))
        img.image = cloudinary.uploader.upload_resource(f'{cwd}/media/memes/{i}.JPG')
        img.save()
    options = ["home", 'like', 'messages']
    for option in options:
        photo = InstaPhotos(name = option)
        photo.save()
        photo.image = cloudinary.uploader.upload_resource(f'{cwd}/media/{option}.png')
        photo.save()