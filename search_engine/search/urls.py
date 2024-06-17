from django.urls import path
from search import views

app_name = 'search'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('wenxin_result/', views.wenxin_result, name='wenxin_result'),
]
