# ViewSets define the view behavior.
from rest_framework import viewsets, views
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from models import Seduta, Allegato
from serializers import SedutaSerializer, SedutaDetailSerializer


class SedutaViewSet(viewsets.ModelViewSet):
    queryset = Seduta.objects.all()
    serializer_class = SedutaSerializer

    def retrieve(self, request, pk=None):
        queryset = Seduta.objects.all()
        seduta = get_object_or_404(queryset, pk=pk)
        serializer = SedutaDetailSerializer(seduta)
        return Response(serializer.data)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename):
        # file pointer (content)
        file_ptr = request.data['file']

        # retrieve Allegato object, corresponding to file
        allegato_obj = Allegato.objects.get(relURI=filename)

        # bind the uploaded content to the file field of the allegato object
        allegato_obj.file.save(filename, file_ptr)
        return Response(status=204)
