from django.db import models


class Coccion(models.Model):
    idcoccion = models.AutoField(db_column='idCoccion', primary_key=True)  # Field name made lowercase.
    fecha_coccion = models.CharField(max_length=50, blank=True, null=True)
    receta = models.ForeignKey('Receta', models.DO_NOTHING, db_column='receta', to_field='nombre_receta')

    class Meta:
        managed = False
        db_table = 'coccion'


class Entrada(models.Model):
    identrada = models.AutoField(db_column='idEntrada', primary_key=True)  # Field name made lowercase.
    proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor', to_field='nombre_proveedor')
    fecha_entrada = models.CharField(max_length=50, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrada'


class Entradadetalle(models.Model):
    identrada = models.OneToOneField(Entrada, models.DO_NOTHING, db_column='idEntrada', primary_key=True)  # Field name made lowercase. The composite primary key (idEntrada, insumo) found, that is not supported. The first column is selected.
    insumo = models.ForeignKey('Insumo', models.DO_NOTHING, db_column='insumo', to_field='nombre_insumo')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entradadetalle'
        unique_together = (('identrada', 'insumo'),)


class Insumo(models.Model):
    idinsumo = models.AutoField(db_column='idInsumo', primary_key=True)  # Field name made lowercase.
    nombre_insumo = models.CharField(unique=True, max_length=80)
    cantidad_disponible = models.IntegerField(blank=True, null=True)
    tipo_medida = models.CharField(max_length=10, blank=True, null=True)
    categoria = models.CharField(max_length=20, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor', to_field='nombre_proveedor', blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insumo'


class Proveedor(models.Model):
    idproveedor = models.AutoField(db_column='idProveedor', primary_key=True)  # Field name made lowercase.
    nombre_proveedor = models.CharField(max_length=60, unique=True)
    mail = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'


class PuntoReposicion(models.Model):
    idpuntoreposicion = models.AutoField(db_column='idPuntoReposicion', primary_key=True)  # Field name made lowercase.
    insumo = models.ForeignKey(Insumo, models.DO_NOTHING, db_column='insumo', to_field='nombre_insumo')
    punto_reposicion = models.IntegerField(blank=True, null=True)
    fecha_ultima_compra = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punto_reposicion'


class Receta(models.Model):
    idreceta = models.AutoField(db_column='idReceta', primary_key=True)  # Field name made lowercase.
    nombre_receta = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50)
    litros = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        managed = False
        db_table = 'receta'


class Recetadetalle(models.Model):
    idrecetadetalle = models.AutoField(db_column='idRecetaDetalle', primary_key=True)
    receta = models.ForeignKey(Receta, models.DO_NOTHING, db_column='receta', to_field='nombre_receta')  # The composite primary key (receta, insumo) found, that is not supported. The first column is selected.
    insumo = models.ForeignKey(Insumo, models.DO_NOTHING, db_column='insumo', to_field='nombre_insumo')
    cantidad = models.IntegerField()
    tipo_medida = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'recetadetalle'
        unique_together = (('receta', 'insumo'),)


class RegistroAlertasStock(models.Model):
    idalerta = models.AutoField(db_column='idAlerta', primary_key=True)  # Field name made lowercase.
    descripcion_alerta = models.CharField(max_length=100, blank=True, null=True)
    fecha_alerta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registro_alertas_stock'


class Salida(models.Model):
    idsalida = models.AutoField(db_column='idSalida', primary_key=True)  # Field name made lowercase.
    fecha_salida = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salida'


class Salidadetalle(models.Model):
    idsalida = models.OneToOneField(Salida, models.DO_NOTHING, db_column='idSalida', primary_key=True)  # Field name made lowercase. The composite primary key (idSalida, insumo) found, that is not supported. The first column is selected.
    insumo = models.ForeignKey(Insumo, models.DO_NOTHING, db_column='insumo', to_field='nombre_insumo')
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'salidadetalle'
        unique_together = (('idsalida', 'insumo'),)
