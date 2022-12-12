from django.urls import path

from . import views

urlpatterns = [
    path('', views.CollectionList.as_view(), name='collections'),
    path('<uuid:collection_uuid>/', views.CollectionDetail.as_view(),name='collection-details'),
]
