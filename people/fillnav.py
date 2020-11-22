from .models import Image, Profile, Comment
import random
from random import shuffle
import cloudinary, cloudinary.api,cloudinary.uploader
import os
def initialize():
    cwd = os.getcwd()
    comments = ["soo cute  ","Couldn't be me haha", "wyd lol", "hii", "this cracked me up haha"]
    profiles = ["bethu's clique","bethwel"]

    for profile in profiles:
        prof = Profile(bio = profile)
        prof.dp = cloudinary.uploader.upload_resource(f'{cwd}/media/memes/{2}.JPG')
        prof.save()

    for comment in comments:
        com = Comment(comment = comment)
        com.save()
    profs = [prof for prof in Profile.objects.all()]
    coms = [com for com in Comment.objects.all()]
    for i in range(7):
        img = Image(name =f'Post number {i}',caption = " just a favourite meme",likes = 0, profile = random.choice(profs), comments = random.choice(coms))
        img.save()
        img.image = cloudinary.uploader.upload_resource(f'{cwd}/media/memes/{i}.JPG')
        img.save()
        