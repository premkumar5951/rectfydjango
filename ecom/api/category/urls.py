from . import views
from django.urls import path,include


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'',views.CategoryViewSet )


urlpatterns = [

    path('',include(router.urls)),
]