from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ContactViewSet, SpamReportViewSet, SearchViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'spam-reports', SpamReportViewSet)
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]