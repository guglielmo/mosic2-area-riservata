#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ViewSets define the view behavior.
import logging
import os
import stat
import traceback
import tempfile

from collections import OrderedDict

from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import viewsets, views, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from models import Seduta, Allegato
from serializers import SedutaDetailSerializer, \
    SedutaCIPESerializer, SedutaPreCIPESerializer

logger = logging.getLogger('django')

class BaseSedutaViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    The base viewset for the SedutaViewsets, that provides
    `retrieve`, `create`, `list` and `delete` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class SedutaCIPEViewSet(BaseSedutaViewSet):
    """
    create:
    Creates a new seduta of type `cipe`, and all its sub-objects, if they're
    recursively passed in the JSON body

    list:
    Lists all sedute of type `cipe`. Shows link to detailed views.

    retrieve:
    Shows the full details of the seduta of type `cipe` identified by {id},
    along with its children objects.

    delete:
    Deletes the seduta of type `cipe` identified by {id} and, recursively,
    its children objects from the Database  and the attached documents from the
    file system.
    """

    queryset = Seduta.objects.filter(tipo='cipe')
    serializer_class = SedutaCIPESerializer

    def retrieve(self, request, pk=None):
        queryset = Seduta.objects.filter(tipo='cipe')
        seduta = get_object_or_404(queryset, pk=pk)
        serializer = SedutaDetailSerializer(seduta)
        return Response(serializer.data)


class SedutaPreCIPEViewSet(BaseSedutaViewSet):
    """
    create:
    Creates a new seduta of type `precipe`, and all its sub-objects, if they're
    recursively passed in the JSON body

    list:
    Lists all sedute of type `precipe`. Shows link to detailed views.

    retrieve:
    Shows the full details of the seduta of type `precipe` identified by {id},
    along with its children objects.

    delete:
    Deletes the seduta of type `precipe` identified by {id} and, recursively,
    its children objects from the Database  and the attached documents from the
    file system.
    """
    queryset = Seduta.objects.filter(tipo='precipe')
    serializer_class = SedutaPreCIPESerializer
    http_method_names = ['get', 'post', 'head', 'delete']

    def retrieve(self, request, pk=None):
        queryset = Seduta.objects.filter(tipo='precipe')
        seduta = get_object_or_404(queryset, pk=pk)
        serializer = SedutaDetailSerializer(seduta)
        return Response(serializer.data)

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename):
        """
        Uploads a file.

        The file is put into the `media` path, using part of the hash
        and the `filename` parameter.

        The content of the file is specified in the `file` key of the request
        data.
        """

        # file pointer (content)
        with tempfile.SpooledTemporaryFile(max_size=settings.FILE_UPLOAD_MAX_MEMORY_SIZE) as tf:
            tf.write(request.data['file'].read())
            logger.info("File name: {0}".format(filename))

            # retrieve all Allegato objects, corresponding to file
            try:
                allegato_objects = Allegato.objects.filter(relURI=filename)
                for allegato_obj in allegato_objects:
                    seduta_hash = allegato_obj.punto_odg.seduta.hash[:10]
                    complete_filename = "{0}_{1}".format(
                        seduta_hash, filename
                    )
                    logger.info("  complete_name: {0}".format(allegato_obj.file.storage.path(complete_filename)))

                    # remove file from storage if existingm to avoid files duplication
                    allegato_obj.file.storage.delete(complete_filename)
                    logger.info(" allegato_obj deleted")

                    # save file to storage
                    allegato_obj.file.save(complete_filename, tf)
                    logger.info(" allegato_obj saved")

                    # force permissions change to solve big files problem on server
                    uploaded_file_path = allegato_obj.file.storage.path(complete_filename)
                    logger.info(" uploaded file path: {0}".format(uploaded_file_path))
                    os.chmod(uploaded_file_path, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                    logger.info(" allegato_obj permissions modified")

                return Response(
                    status=204,
                    data={
                        'status': 204,
                        'message':
                            u"File {0} caricato correttamente".format(filename)
                    }
                )
            except Exception as e:
                logger.error("Errore durante caricamento di {0}: {1}".format(filename, repr(e)))
                logger.error("Traceback: {0}".format(traceback.format_exc()))
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
        """
        Returns useful data of a seduta of the given type,
        starting from the `id_seduta` and the `tipo` parameters.

        The result is a dict:

            {
              'id':  the internal unique autoincrement id
              'url': the absolute url of the  public page
            }
        """
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
    """
    The public, shared page, accessible through the `hash`
    """
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




