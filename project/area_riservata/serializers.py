import hashlib

from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from models import Seduta, PuntoODG, Allegato


class AllegatoSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(
        max_length=None, use_url=True,
        allow_empty_file=True, read_only=True
    )
    relURI = serializers.CharField(
        max_length=256, write_only=True
    )
    class Meta:
        model = Allegato
        fields = ('id_allegato', 'data', 'nome', 'tipo', 'relURI', 'dimensione', 'file')


class PuntoODGSerializer(serializers.HyperlinkedModelSerializer):
    allegati = AllegatoSerializer(required=False, many=True)

    class Meta:
        model = PuntoODG
        fields = ('id_punto_odg', 'denominazione', 'progressivo', 'ordine', 'allegati')


class SedutaSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        """create the Seduta object, all PuntoODG objects
        specified in the data, and all Allegato objects therein,
        inside an atomic transaction
        
        :param validated_data: JSON serialized, valid data 
        :return: Seduta instance, or None
        """
        seduta = None
        with transaction.atomic():
            punti_odg_data = []
            if 'punti_odg' in validated_data:
                punti_odg_data = validated_data.pop('punti_odg')

            seduta = Seduta.objects.create(**validated_data)

            # generates hash
            seduta.hash = hashlib.sha256(
                settings.HASH_SALT + ":" + seduta.tipo + ":" + str(seduta.id_seduta),
            ).hexdigest()
            seduta.save()

            for punto_odg_data in punti_odg_data:
                # remove OrderDict from punto_odg_data
                allegati_data = []
                if 'allegati' in punto_odg_data:
                    allegati_data = punto_odg_data.pop('allegati')

                punto_odg = PuntoODG.objects.create(
                    seduta=seduta, **punto_odg_data
                )

                for allegato_data in allegati_data:
                    Allegato.objects.create(
                        punto_odg=punto_odg, **allegato_data
                    )

                # for allegato_data in allegati_data:
                #     allegato_id = allegato_data.pop('id_allegato')
                #     allegato, created = Allegato.objects.get_or_create(
                #         id_allegato=allegato_id,
                #         defaults=allegato_data
                #     )
                #     punto_odg.allegati.add(allegato)

            return seduta

    class Meta:
        model = Seduta
        fields = ('id_seduta', 'tipo', 'data', 'ufficiale', )

class SedutaCIPESerializer(SedutaSerializer):
    punti_odg = PuntoODGSerializer(required=False, many=True, write_only=True)
    self_uri = serializers.HyperlinkedIdentityField(view_name = 'cipe-detail')
    class Meta(SedutaSerializer.Meta):
        fields = ('tipo', 'id_seduta', 'self_uri', 'data', 'ufficiale', 'punti_odg')

class SedutaPreCIPESerializer(SedutaSerializer):
    punti_odg = PuntoODGSerializer(required=False, many=True, write_only=True)
    self_uri = serializers.HyperlinkedIdentityField(view_name = 'precipe-detail')
    class Meta(SedutaSerializer.Meta):
        fields = ('tipo', 'id_seduta', 'self_uri', 'data', 'ufficiale', 'punti_odg')


class SedutaDetailSerializer(serializers.HyperlinkedModelSerializer):
    punti_odg = PuntoODGSerializer(required=False, many=True)

    class Meta:
        model = Seduta
        fields = ('tipo', 'id_seduta', 'hash', 'data', 'ufficiale', 'punti_odg')



