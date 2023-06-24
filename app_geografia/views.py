from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Region, Comuna
from .serializers import RegionSerializer, ComunaSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.shortcuts import get_object_or_404



class RegionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def perform_create(self, serializer):
        serializer.save()

        # Reiniciar los IDs de las regiones
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE app_geografia_region_id_seq RESTART WITH 1;")


from rest_framework.generics import CreateAPIView
class RegionCreateAPIView(generics.CreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework.generics import UpdateAPIView
class RegionUpdateAPIView(UpdateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

from rest_framework.generics import DestroyAPIView
class RegionDestroyAPIView(DestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

from rest_framework.generics import RetrieveAPIView
class RegionRetrieveAPIView(RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer



class ComunaListAPIView(generics.ListAPIView):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer

class ComunaDetailAPIView(generics.RetrieveAPIView):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer
    lookup_field = 'id'


class ComunaCreateAPIView(generics.CreateAPIView):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer

    def create(self, request, *args, **kwargs):
        region_id = request.data.get('region_id')
        region = get_object_or_404(Region, id=region_id)
        comunas_data = request.data.get('comunas', [])

        for comuna_data in comunas_data:
            comuna_data['region'] = region.id

        serializer = self.get_serializer(data=comunas_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

