from django.urls import path, include
from rest_framework.routers import DefaultRouter
from components.views import ComponentListViewset

router = DefaultRouter()
router.register(r'', ComponentListViewset)

urlpatterns = [
    path('', include(router.urls)),
]
