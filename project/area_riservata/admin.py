from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from area_riservata.models import Seduta, PuntoODG, Allegato

class AllegatoInline(admin.TabularInline):
    model = Allegato
    max_num = 0
    can_delete = False
    show_change_link = True
    readonly_fields = fields = ('nome', 'tipo', 'file', 'dimensione')

    # def change_link(self, obj):
    #     return mark_safe('<a href="%s">Full edit</a>' % \
    #                     reverse('admin:area_riservata_puntoodg_change',
    #                     args=(obj.id,)))


class PuntoODGAdmin(admin.ModelAdmin):
    list_display = ('id', 'denominazione', 'progressivo', 'ordine', 'seduta')
    readonly_fields = list_display
    search_fields = ('denominazione',)
    inlines = [AllegatoInline,]


class PuntoODGInline(admin.TabularInline):
    model = PuntoODG
    max_num = 0
    can_delete = False
    show_change_link = True
    readonly_fields = fields = ('denominazione', 'progressivo', 'ordine', )

    def change_link(self, obj):
        return mark_safe('<a href="%s">Full edit</a>' % \
                        reverse('admin:area_riservata_puntoodg_change',
                        args=(obj.id,)))

class SedutaAdmin(admin.ModelAdmin):
    list_display = ('id', 'hash', 'data')
    readonly_fields = list_display + ('tipo', 'ufficiale')
    search_fields = ('data',)
    inlines = [PuntoODGInline,]


admin.site.register(Seduta, SedutaAdmin)
admin.site.register(PuntoODG, PuntoODGAdmin)
