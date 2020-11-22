from django.conf.urls import url
from . import views
from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
url('^$', views.allprofiles, name = 'allprofiles'),
url('^profile', views.profile, name = 'location'),
url(r'^search/', views.search_results, name='search_results'),
url(r'^photo/(\d+)',views.photo,name ='photo'), 
url(r'^auth/login',views.login,name ='login'),
url(r'^auth/register',views.register,name ='register'),

]
