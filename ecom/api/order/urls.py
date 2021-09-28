from django.urls import path,include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'',views.OrderViewSet )


urlpatterns = [
    path("add/<int:id>/<str:token>/",views.add,name="order.add"),
    path('',include(router.urls)),
]