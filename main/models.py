from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
import re
# Create your models here.

class Articulo(models.Model):
    def mes_proceso_default():
        return datetime.now().date()

    codigo = models.CharField(_("código"), primary_key=True, max_length=10, validators= [MaxLengthValidator(limit_value=10, 
                                                                                                           message='La cantidad de caracteres no puede ser mayor que 10'), 
                                                                                        MinLengthValidator(limit_value=10, 
                                                                                                            message='La cantidad de caracteres no puede ser menor que 10'),
                                                                                        RegexValidator(regex=r'^[0-9]*$', message='Solo puede contener números')
                                                                                        ])
    nombre = models.CharField(_("nombre"), max_length=50)
    costo = models.DecimalField(_("costo"), max_digits=8, decimal_places=3)
    cantidad_producida_en_el_mes = models.PositiveIntegerField(_("cantidad producida en el mes"))
    taller = models.ForeignKey("main.Taller", on_delete=models.CASCADE)
    mes_proceso = models.DateField(_("mes de proceso"), auto_now=False, auto_now_add=False, default=mes_proceso_default)
    cantidad_rechazada = models.PositiveIntegerField(_("cantidad rechazada"))

    class Meta:
        verbose_name = _("Articulo")
        verbose_name_plural = _("Articulos")
        constraints = [models.CheckConstraint(
                                    name='check_cpm__gt__cr', 
                                    check=models.Q(
                                    cantidad_producida_en_el_mes__gt=models.F('cantidad_rechazada'),
                                    ),
                                    violation_error_message='La cantidad producida en el mes no puede ser menor que cantidad rechazada'
                                  ),

        ]

    def __str__(self):
        return self.nombre

    # def get_absolute_url(self):
    #     return reverse("Articulo_detail", kwargs={"pk": self.pk})

class Taller(models.Model):

    class TallerCodigo(models.TextChoices):
        VAJILLAS   = '01', _('Taller de vajillas')
        ACCESORIOS = '02', _('Taller de accesorios para el baño')
        MISCELANEAS= '03', _('Taller de misceláneas')

    codigo = models.CharField(_("código"), primary_key=True, max_length=2, choices=TallerCodigo.choices, default=TallerCodigo.VAJILLAS)
    # nombre = models.CharField("nombre", max_length=50)
    

    class Meta:
        verbose_name = _("Taller")
        verbose_name_plural = _("Talleres")

    def __str__(self):
        return self.TallerCodigo(self.codigo).label.title()

    # def get_absolute_url(self):
    #     return reverse("Taller_detail", kwargs={"pk": self.pk})

