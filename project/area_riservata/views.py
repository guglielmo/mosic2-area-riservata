# ViewSets define the view behavior.
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from models import Seduta

from serializers import SedutaSerializer, SedutaDetailSerializer


class SedutaViewSet(viewsets.ModelViewSet):
    queryset = Seduta.objects.all()
    serializer_class = SedutaSerializer

    def retrieve(self, request, pk=None):
        queryset = Seduta.objects.all()
        seduta = get_object_or_404(queryset, pk=pk)
        serializer = SedutaDetailSerializer(seduta)
        return Response(serializer.data)
