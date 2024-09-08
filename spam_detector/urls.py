from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, ContactViewSet, SpamReportViewSet, SearchViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'spam-reports', SpamReportViewSet)
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

