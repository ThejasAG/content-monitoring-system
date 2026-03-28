from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KeywordViewSet, FlagViewSet, scan_view

router = DefaultRouter()
router.register(r'keywords', KeywordViewSet)
router.register(r'flags', FlagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('scan/', scan_view, name='scan'),
]
