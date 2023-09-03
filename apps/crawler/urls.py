from django.urls import path
from .views import CrawlListList, CrawlListDetail, CrawlDetailList, CrawlDetailDetail

urlpatterns = [
    path("crawl-lists/", CrawlListList.as_view(), name="crawl-list-list"),
    path("crawl-lists/<int:pk>/", CrawlListDetail.as_view(), name="crawl-list-detail"),
    path("crawl-details/", CrawlDetailList.as_view(), name="crawl-detail-list"),
    path(
        "crawl-details/<int:pk>/",
        CrawlDetailDetail.as_view(),
        name="crawl-detail-detail",
    ),
]
