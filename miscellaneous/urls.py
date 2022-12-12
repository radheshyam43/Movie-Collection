from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.GetMovies.as_view(), name='movies'),
    path('request-count/', views.RequestCount.as_view(), name='request-count'),
    path('request-count/reset/', views.ResetRequestCount.as_view(),
         name='reset-request-count'),
]
