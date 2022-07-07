from django.urls import path
from .views import RegisterUserAPIView,UserloginView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('crud',UserloginView , basename= 'user')


urlpatterns = [
    path('register',RegisterUserAPIView.as_view()),
    path('loginapi',UserloginView.as_view(),name="loginapi"),
]
