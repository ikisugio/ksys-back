from django.urls import path, re_path
from .views import (CompanyList, CompanyDetail,
                    JigyosyoList, JigyosyoDetail,
                    LogicalJigyosyoList, LogicalJigyosyoDetail,
                    AdminGroupList, AdminGroupDetail,
                    AdminUserList, AdminUserDetail,
                    CustomAuthToken)

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
    path('admin/groups/', AdminGroupList.as_view(), name='admin-group-list'),
    path('admin/groups/<int:pk>/', AdminGroupDetail.as_view(), name='admin-group-detail'),
    path('admin/users/', AdminUserList.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', AdminUserDetail.as_view(), name='admin-user-detail'),
    path('admin/login/', CustomAuthToken.as_view(), name='admin-login'),
    path('logical-jigyosyo/', LogicalJigyosyoList.as_view(), name='logical-jigyosyo-list'),
    path('logical-jigyosyo/<int:pk>/', LogicalJigyosyoDetail.as_view(), name='logical-jigyosyo-detail'),
]
