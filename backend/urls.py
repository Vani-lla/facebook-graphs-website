from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', loginView),
    path('logout', logoutView),
    path('register', registerView),
    path('who', whoView),
    path('json/upload', jsonUploadView),
    path('json/view', allJsonView),
    path('<id>', jsonDataView),
]
