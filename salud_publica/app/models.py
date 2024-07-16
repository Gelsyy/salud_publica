from django.db import models
from django.core.exceptions import ValidationError

class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre_insumo = models.CharField(max_length=255)
    codigo_cup = models.CharField(max_length=14, unique=True)  # Definir como único
    importado = models.IntegerField(blank=True, null=True)
    produccion_nacional = models.IntegerField(blank=True, null=True)
    TC = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre_insumo


class Hospital(models.Model):
    id_hospital = models.AutoField(primary_key=True)
    nombre_hospital = models.CharField(max_length=255)

    def __str__(self):
          return self.nombre_hospital


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    lote = models.CharField(max_length=255)
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    id_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    cantidad_entrada = models.IntegerField(default=0)
    cantidad_salida = models.IntegerField(default=0)
    existencia = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField()
    fecha_entrada = models.DateField()

    def clean(self):
        # Validación para asegurar que cantidad_salida no supere cantidad_entrada
        if self.cantidad_salida > self.cantidad_entrada:
            raise ValidationError("La cantidad de salida no puede ser mayor que la cantidad de entrada.")

   

    def save(self, *args, **kwargs):
        self.existencia = self.cantidad_entrada - self.cantidad_salida
        super().save(*args, **kwargs)

    def __str__(self):
          return self.lote  