from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'app_geografia'

urlpatterns = [
    path('api/regiones/', views.RegionListCreateAPIView.as_view(), name='region-list'),
    path('api/regiones/create/', views.RegionCreateAPIView.as_view(), name='region-create'),
    path('api/regiones/<int:pk>/', views.RegionRetrieveAPIView.as_view(), name='region-detail'),
    path('api/regiones/<int:pk>/update/', views.RegionUpdateAPIView.as_view(), name='region-update'),
    path('api/regiones/<int:pk>/delete/', views.RegionDestroyAPIView.as_view(), name='region-delete'),






    path('api/comunas/', views.ComunaListAPIView.as_view(), name='comuna-list'),
    path('api/comunas/<int:id>/', views.ComunaDetailAPIView.as_view(), name='comuna-detail'),
    path('api/comunas/create/', views.ComunaCreateAPIView.as_view(), name='comuna-create'),
]