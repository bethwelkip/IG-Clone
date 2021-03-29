from django.shortcuts import render, redirect, Http404
from django.contrib.auth import authenticate, login as log, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Image,Profile, Comment, Following,InstaPhotos
from .forms import LoginForm, UploadForm, UpdateForm
from .fillnav import initialize
from .emails import send_welcome_email
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
import cloudinary, cloudinary.api,cloudinary.uploader
import os
from io import BytesIO
from PIL import Image as pillow_image

# Create your views here.
def addPhoto(): #irrelevant function
    cwd = os.getcwd()
    photo = InstaPhotos(name = "profile")
    photo.save()
    photo.image = cloudinary.uploader.upload_resource(f'{cwd}/media/profile.png')
    photo.save()
def register(request):
    form =  RegistrationForm(request.POST or None)
    context = {}

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
            print(user.password)
            profile = Profile(user = user)
            profile.save()
            print(user.id)
            send_welcome_email(user,email)
            return redirect('login')
        else: 
            messages.info(request, "Username or Password is incorrect")
            print(form.errors)
            return render(request, 'auth/registration.html', {"form":form})
    return render(request, 'auth/registration.html', {"form":form})

def login(request):
    form = AuthenticationForm()# LoginForm()
    context = {"form":form}
    if request.method == "POST":
        user = request.POST.get('username')
        password = request.POST.get('password')
        print(user, password, "\n\n")
        user = authenticate(request, username=user, password = password)
        if user is not None:
            print("Here")
            log(request, user)
            print("Here2")
            return redirect('allprofiles')
        else: 
            messages.info(request, "Username or Password is incorrect")
            context.update({"messages": messages})
            return redirect('login')
    
    return render(request, 'auth/login.html', context)
@login_required(login_url = '/auth/login')
def allprofiles(request):
    imgs = Image.objects.all()
     # initialize database
    if not imgs:
        initialize()
    # addPhoto()
    # find people the current user doesn't follow
    current_user = request.user
    profile = Profile.objects.get(user__id = current_user.id)
    follow = profile.following.all()
    followed = [user.user for user in follow if user.user.id != current_user.id]
    not_followed = [user for user in User.objects.all() if user not in followed and user.id != current_user.id]
    followed_profiles = list()
    post = list()
    for fol in followed:
        followed_profiles.append(Profile.objects.get(user__id = fol.id))
    print(followed_profiles)
    for profile in followed_profiles:
        post.append(Image.objects.filter(profile__id = profile.id).all())
    filed = Profile.objects.get(user__id = current_user.id)
    post.append(Image.objects.filter(profile__id = filed.id).all())
    # print(type(post))
    posts = list()
    for pos in post:
        for image in pos:
            if image not in posts:
                posts.append(image)
    # print(len(posts))

    # initialize database
    # posts = [post for post in Image.objects.all()]
    if 'comment' in request.GET and request.GET["comment"]:
        com = request.GET.get('comment')
    return render(request, 'allprofiles.html', {"posts": posts, "follow":not_followed})

def new_comment(request, post_id):
    if 'comment' in request.GET and request.GET["comment"]:
        com = request.GET.get('comment')
        new_com = Comment(comment = com)
        new_com.save()
        post = Image.objects.get(id = post_id)
        post.comments.add(new_com)
        post.save()
        print("justice                  \n\n", com) #working
        return redirect('allprofiles')
    return redirect('allprofiles')
def new_like(request, post_id):
    post = Image.objects.get(id = post_id)
    print(post.likes)
    post.likes += 1
    post.save()
    print(post.likes)
    return redirect('allprofiles')

@login_required(login_url = '/auth/login')
def follow(request, user_id):
    current_user = request.user
    print("\n", current_user.id, "\n\n")
    user_to_follow = User.objects.get(id= user_id)
    print("\n", user_to_follow.id, "\n\n")
    follow = Following(user = user_to_follow)
    follow.save()
    follower = Profile.objects.get(user__id =  current_user.id)
    follower.following.add(follow)
    follower.save()
    print(follower.user.username, "\nabove\n\n")
    return redirect('allprofiles')

@login_required(login_url = '/auth/login')
def profile(request):
    current_user = request.user
    profile = Profile.objects.get(user__id = current_user.id)
    print(profile.id)
    posts = Image.objects.filter(profile__user__id = current_user.id).all()
    follow = profile.following.all()
    following = len(follow)
    return render(request, 'profile.html',{"posts": posts, "user": profile})
@login_required(login_url = '/auth/login')
def search_results(request):
    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_users = Profile.search_users(search_term)
        profiles = list()
        for user in searched_users:
            profiles.append(Profile.objects.filter(user__id = user.id).first())
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"users": profiles})

    else:
        message = "You haven't searched for any term \n"
        return render(request, 'search.html',{"message":message})
@login_required(login_url = '/auth/login')
def photo(request, photo_id):
    try:
        photo = Image.objects.get(id = photo_id)
        print(photo.image.url)
        comments = photo.comments
        # comments = [comment.comment for comment in coms]
    except:
        raise Http404()
    return render(request, 'image.html', {"photo": photo, "comments": comments})
@login_required(login_url = '/auth/login')
def upload(request):
    current_user = request.user
    form = UploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        print(form.is_valid())
        if form.is_valid():
            imag = request.FILES.get('image')
            im = pillow_image.open(imag)
            bytes_io = BytesIO()
            im =im.resize((600, 600))
            im.save(bytes_io, 'png')
            im = bytes_io.getvalue()
            img = cloudinary.uploader.upload_resource(im)
            caption = request.POST.get('caption')
            name = request.POST.get('name')
            prof = Profile.objects.get(user__id = current_user.id)
            image = Image(name = name, caption = caption, likes = 0, profile = prof, image = img)
            image.save()
            return redirect('profile')
    return render(request, 'upload.html', {"form": form})

@login_required(login_url = '/auth/login')
def update(request):
    current_user = request.user
    form = UpdateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            img = request.FILES.get('dp')
            bio = request.POST.get('bio')
            prof = Profile.objects.get(user__id = current_user.id)
            prof.dp = cloudinary.uploader.upload_resource(img)
            prof.bio = bio
            prof.save()
            return redirect('profile')
    return render(request, 'updateprofile.html', {"form": form})
def logout_me(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")