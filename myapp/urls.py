# myapp/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup2/', views.signup2, name='signup2'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    # Add more paths as needed
]
