from django.contrib import admin
from django.urls import path
from solver import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.bisection_method, name='bisection'),
]