#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ViewSets define the view behavior.
from collections import OrderedDict

from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import viewsets, views
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from models import Seduta, Allegato
from serializers import SedutaDetailSerializer, \
    SedutaCIPESerializer, SedutaPreCIPESerializer


class SedutaCIPEViewSet(viewsets.ModelViewSet):
    queryset = Seduta.objects.filter(tipo='cipe')
    serializer_class = SedutaCIPESerializer

    def retrieve(self, request, pk=None):
        queryset = Seduta.objects.filter(tipo='cipe')
        seduta = get_object_or_404(queryset, pk=pk)
        serializer = SedutaDetailSerializer(seduta)
        return Response(serializer.data)


class SedutaPreCIPEViewSet(viewsets.ModelViewSet):
    queryset = Seduta.objects.filter(tipo='precipe')
    serializer_class = SedutaPreCIPESerializer

    def retrieve(self, request, pk=None):
        queryset = Seduta.objects.filter(tipo='precipe')
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

            seduta_hash = allegato_obj.punto_odg.seduta.hash[:10]
            complete_filename = "{0}_{1}".format(
                seduta_hash, filename
            )

            # remove file from storage if existingm to avoid files duplication
            allegato_obj.file.storage.delete(complete_filename)

            # save file to storage
            allegato_obj.file.save(complete_filename, file_ptr)

            return Response(
                status=204,
                data={
                    'status': 204,
                    'message':
                        u"File {0} caricato correttamente".format(filename)
                }
            )
        except Allegato.DoesNotExist:
            return Response(
                status=404,
                data={
                    'status': 404,
                    'message':
                        u"File {0} non trovato".format(filename)
                }
            )
        except Exception as e:
            return Response(
                status=500,
                data={
                    'status': 500,
                    'message':
                        u"Errore durante caricamento di {0}: {1}".format(filename, repr(e))
                }
            )


class SedutaView(views.APIView):
    def get(self, request, tipo, id_seduta):
        try:
            seduta = Seduta.objects.get(id_seduta=id_seduta, tipo=tipo)

            seduta_url = "http://{0}{1}".format(
                Site.objects.get(pk=1),
                reverse('seduta-{0}'.format(tipo),
                    args=(seduta.hash,)
                )
            )
            return Response(
                data=OrderedDict([
                    ('id', seduta.id),
                    ('url', seduta_url)
                ]),
                status=200
            )
        except Seduta.DoesNotExist:
            return Response(
                status=404,
                data={'status': 404, 'message': u"Impossibile trovare seduta"}
            )


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




