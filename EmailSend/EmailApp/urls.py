from django.urls import path
from . import views
urlpatterns=[
    path('',views.Email_Sending,name='Email_Sending')
]