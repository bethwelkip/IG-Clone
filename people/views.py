from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image,Profile, Comment
from .forms import LoginForm
from django_registration.forms import RegistrationForm
# from .forms import 
# Create your views here.
def register(request):
    form =  RegistrationForm(request.POST or None)
    context = {}
    if form.is_valid():
        user = request.GET.get('username')
        email = request.GET.get('email')
        password = request.GET.get('password')
        form.save()
        print("Here")
        return redirect('login')
    else: 
        messages.info(request, "Username or Password is incorrect")
        print("Herr")
        return render(request, 'auth/registration.html', {"form":form})
    return render(request, 'auth/registration.html', {"form":form})

def login(request):
    form = LoginForm()
    context = {"form":form}
    if request.method == "POST":
        user = request.GET.get('username')
        password = request.GET.get('password')
        # print("Here")
        user = authenticate(request, username=user, password = password)
        # print("Here")
        if user is not None:
            print("Here")
            login(request, user)
            return redirect('profile', context)
        else: 
            messages.info(request, "Username or Password is incorrect")
            context.update({"messages": messages})
            return redirect('login')
    
    return render(request, 'auth/login.html', context)
@login_required(login_url = '/auth/login')
def allprofiles(request):
    posts = Image.objects.all()
    print(posts)
    return render(request, 'allprofiles.html', {"posts": posts})


@login_required(login_url = '/auth/login')
def profile(request):
    pass
@login_required(login_url = '/auth/login')
def search_results(request):
    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_users = Profile.search_users(search_term)
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"images": searched_images})

    else:
        message = "You haven't searched for any term \n"
        return render(request, 'search.html',{"message":message})
@login_required(login_url = '/auth/login')
def photo(request,  photo_id):
    try:
        photo = Image.objects.get(id = photo_id)
        coms = photo.comments.all()
        comments = [comment.comment for comment in coms]
    except:
        raise Http404()
    return render(request, 'photo.html', {"photo": photo, "comments": comments})
@login_required(login_url = '/auth/login')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.save()
        return redirect('NewsToday')

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})