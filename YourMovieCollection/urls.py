from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls')),
    path('', include('miscellaneous.urls')),
    path('admin/', admin.site.urls),
    path('collection/', include('collection.urls')),
]
