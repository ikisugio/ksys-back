from django.urls import path, re_path
from .views import CompanyList, CompanyDetail, JigyosyoList, JigyosyoDetail

urlpatterns = [
    path("companies/", CompanyList.as_view(), name="company-list"),
    re_path(
        r"^companies/(?P<pk>[0-9a-f-]+)/$",
        CompanyDetail.as_view(),
        name="company-detail",
    ),
    path("jigyosyos/", JigyosyoList.as_view(), name="jigyosyo-list"),
    re_path(
        r"^jigyosyos/(?P<pk>[0-9a-f-]+)/$",
        JigyosyoDetail.as_view(),
        name="jigyosyo-detail",
    ),
]
