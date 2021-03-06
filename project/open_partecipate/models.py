# -*- coding: utf-8 -*-
from django.db import models
from django.utils.functional import cached_property
from model_utils import Choices
from territori.models import Territorio


class BaseCodelist(models.Model):
    codice = models.CharField(max_length=6, primary_key=True)
    descrizione = models.CharField(max_length=150)

    def __unicode__(self):
        return u'{}'.format(self.descrizione)

    class Meta:
        abstract = True
        ordering = ['descrizione']


class EnteCategoria(BaseCodelist):
    TIPO = Choices(
        ('C1', 'categoria', u'Categoria'),
        ('C2', 'sottocategoria', u'Sottocategoria'),
    )

    tipo = models.CharField(max_length=2, choices=TIPO, db_index=True)
    categoria_superiore = models.ForeignKey('self', related_name='categorie_figlie', default=None, null=True, limit_choices_to={'tipo': TIPO.categoria})


class Ente(models.Model):
    TIPOLOGIA = Choices(
        ('AL', 'amministrazionilocali', u'Amministrazioni Locali'),
        ('AR', 'amministrazioniregionali', u'Amministrazioni Regionali'),
        ('IL', 'impresepubblichelocali', u'Imprese pubbliche locali'),
    )

    id = models.IntegerField(primary_key=True)
    codice = models.CharField(max_length=12, unique=True, db_index=True)
    denominazione = models.CharField(max_length=255)
    anno_inizio_attivita = models.CharField(max_length=4, null=True)
    anno_fine_attivita = models.CharField(max_length=4, null=True)
    codice_fiscale = models.CharField(max_length=16, null=True)
    indirizzo = models.CharField(max_length=100, null=True)
    cap = models.CharField(max_length=5, null=True)
    comune = models.ForeignKey(Territorio, related_name='enti', null=True, limit_choices_to={'tipo': Territorio.TIPO.C})
    telefono = models.CharField(max_length=100, null=True)
    fax = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    tipologia = models.CharField(max_length=2, choices=TIPOLOGIA, db_index=True)
    sottocategoria = models.ForeignKey(EnteCategoria, related_name='enti', limit_choices_to={'tipo': EnteCategoria.TIPO.sottocategoria})

    @cached_property
    def categoria(self):
        return self.sottocategoria.categoria_superiore

    def __unicode__(self):
        return u'{}'.format(self.denominazione)
