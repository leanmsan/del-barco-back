# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Coccion(models.Model):
    idcoccion = models.AutoField(db_column='idCoccion', primary_key=True)  # Field name made lowercase.
    fecha_coccion = models.DateField()
    receta = models.ForeignKey('Receta', models.DO_NOTHING, db_column='receta', to_field='nombre_receta')
    volumen_producido = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'coccion'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Entrada(models.Model):
    identrada = models.AutoField(db_column='idEntrada', primary_key=True)  # Field name made lowercase.
    proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor', to_field='nombre_proveedor')
    fecha_entrada = models.DateTimeField(blank=True, null=True)
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
    idinsumo = models.ForeignKey(Insumo, models.DO_NOTHING, db_column='idInsumo')  # Field name made lowercase.
    punto_reposicion = models.IntegerField(blank=True, null=True)
    fecha_ultima_compra = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punto_reposicion'


class Receta(models.Model):
    idreceta = models.IntegerField(db_column='idReceta', primary_key=True)  # Field name made lowercase.
    nombre_receta = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'receta'


class Recetadetalle(models.Model):
    receta = models.OneToOneField(Receta, models.DO_NOTHING, db_column='receta', primary_key=True)  # The composite primary key (receta, insumo) found, that is not supported. The first column is selected.
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
    fecha_salida = models.DateTimeField(blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    
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
