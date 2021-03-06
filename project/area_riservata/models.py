from __future__ import unicode_literals
from django.db import models


class Seduta(models.Model):
    id_seduta = models.IntegerField()

    TIPO_SEDUTA_CHOICES = (
        ('precipe','Pre CIPE'),
        ('cipe','CIPE'),
    )
    tipo = models.CharField(
        max_length=10,
        default="precipe",
        choices=TIPO_SEDUTA_CHOICES,
        help_text="Tipo di seduta, se CIPE o Pre CIPE",
        verbose_name="Tipo di seduta"
    )

    data = models.DateField(
        max_length=10,
        help_text="Data della seduta",
        verbose_name="Data seduta"
    )
    ufficiale = models.BooleanField(
        default=False,
    )
    hash = models.CharField(
        max_length=64,
        blank=True, null=True,
        unique=True
    )

    def __unicode__(self):
        return self.tipo + " del " + self.data.strftime('%Y-%m-%d')

    class Meta:
        verbose_name_plural = "sedute"
        unique_together = (('tipo', 'id_seduta'),)


class PuntoODG(models.Model):
    id_punto_odg = models.IntegerField()

    denominazione = models.TextField(
        max_length=1024
    )

    progressivo = models.IntegerField(
        default=1,
        help_text="Posizione in sequenza odg"
    )

    ordine = models.CharField(
        max_length=5,
        default="1",
        help_text="Indicazione punto PuntoODG: 1, 1a, 1b, 1b.2..."
    )

    seduta = models.ForeignKey(
        'Seduta',
        related_name='punti_odg',
        blank=True, null=True,
        on_delete=models.deletion.CASCADE
    )

    def __unicode__(self):
        return self.ordine

    class Meta:
        verbose_name_plural = "punti ODG"


def relURI_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<relURI>/<filename>
    return '{0}'.format(filename)

class Allegato(models.Model):
    id_allegato = models.IntegerField()

    data = models.DateField(
        max_length=10,
    )

    nome = models.CharField(
        max_length=512
    )

    tipo = models.CharField(
        max_length=8
    )

    relURI = models.CharField(
        max_length=512
    )

    # file will contain the file,
    # it is null becaus it can be added after the Allegato
    # object has been created
    file = models.FileField(
        max_length=512,
        blank=True, null=True,
        upload_to=relURI_path
    )


    dimensione = models.IntegerField(
        null=True, blank=True
    )

    punto_odg = models.ForeignKey(
        'PuntoODG',
        related_name='allegati',
        blank=True, null=True,
        on_delete=models.deletion.CASCADE
    )

    def __unicode__(self):
        return self.relURI

    class Meta:
        verbose_name_plural = "allegati"



# signals ---------------------------------------------

from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Allegato)
def allegato_post_delete_handler(sender, **kwargs):
    """remove files from storage when the allegato object is removed
    TODO: only if no other allegato objects point to that file
    :param sender:
    :param kwargs:
    :return:
    """
    allegato_obj = kwargs['instance']
    if allegato_obj.file:
        storage, path = allegato_obj.file.storage, allegato_obj.file.path
        storage.delete(path)
