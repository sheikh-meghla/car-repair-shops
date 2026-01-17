from django.http import Http404
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    # auth
    SignUpAPIView,
    SignInAPIView,
    SignOutAPIView,


    #profile
    UpdateProfileAPIView,
    MyProfileAPIView,
    CreateVendorProfile,

    # witch role

    SwitchRoleAPIView,

)

urlpatterns = [

    # Authentications

    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("signin/", SignInAPIView.as_view(), name="signin"),
    path("signout/", SignOutAPIView.as_view(), name="signout"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # profile
    path('create-vendor-profile/',CreateVendorProfile.as_view(), name='create-vendor-profile'),
    path('update-profile/', UpdateProfileAPIView.as_view(), name='profile-update'),
    path('my-profile/', MyProfileAPIView.as_view(), name='profile-get'),


    # switch role

    path("switch-role/", SwitchRoleAPIView.as_view(), name="switch-role"),
]
