from django.urls import path

from . import views

app_name = 'poly'
urlpatterns = [
    path('', views.index, name='index'),
    path('output', views.OutputView.as_view(), name='output'),
    #path('<int:degree>/', views.polynomials, name='polynomials'),
    path('download_py', views.DownloadPyView.as_view(), name='download_py'),
    path('download_jl', views.DownloadJlView.as_view(), name='download_jl'),
    path('download_coeff', views.DownloadCoeffView.as_view(), name='download_coeff'),
]