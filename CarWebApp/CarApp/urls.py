from django.conf.urls import include, url
from . import views
urlpatterns =[
    url(r'index/', views.index, name='index'),
    url(r'details/(?P<id>[0-9]+)$', views.details, name='details'),
    url(r'register/', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'bookedbyme/(?P<id>[0-9]+)$',views.bookedbyme, name='bookedbyme'),
    url(r'aboutme/',views.aboutme, name='aboutme')
]
