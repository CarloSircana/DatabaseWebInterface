from django.urls import path

from . import views

app_name = 'poly'
urlpatterns = [
    path('', views.index, name='index'),
    path('output', views.output, name='output'),
    #path('<int:degree>/', views.polynomials, name='polynomials'),
]