
from django.contrib import admin
from django.urls import path,include
import attendance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.url'))
]
