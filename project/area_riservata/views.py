# ViewSets define the view behavior.
from django.shortcuts import redirect
from django.views.generic import TemplateView
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
        try:
            allegato_obj = Allegato.objects.get(relURI=filename)

            # remove file from storage if existingm to avoid files duplication
            allegato_obj.file.storage.delete(filename)

            # save file to storage
            allegato_obj.file.save(filename, file_ptr)

            return Response(status=204)
        except Allegato.DoesNotExist:
            return Response(status=400)
        except Exception as e:
            return Response(status=500)


class PublicView(TemplateView):
    template_name = 'public.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            hash = kwargs.pop('hash')
            self.seduta = Seduta.objects.get(hash=hash)
            return super(PublicView, self).dispatch(request, *args, **kwargs)
        except Seduta.DoesNotExist:
            return redirect('tampering-403')


    def get_context_data(self, **kwargs):
        # self.seduta is extracted in the dispatch method
        return super(PublicView, self).get_context_data(
            seduta=self.seduta,
            **kwargs
        )



