from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search.urls')),  # 包含 search 应用的 URL
]

