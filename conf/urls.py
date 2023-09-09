from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("manage/", admin.site.urls),
    path("crawl/", include("apps.crawler.urls")),
    path("crm/", include("apps.crm.urls")),
]
