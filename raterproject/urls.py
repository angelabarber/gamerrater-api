from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

# from rest_framework.authtoken.views import obtain_auth_token
from raterapi.views import (
    login_user,
    register_user,
    GameView,
    CategoryView,
    get_current_user,
    ReviewView,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"games", GameView, "game")
router.register(r"categories", CategoryView, "category")
router.register(r"reviews", ReviewView, "review")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
    path("current_user", get_current_user),
    # path("api-token-auth", obtain_auth_token),
    # path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
]
