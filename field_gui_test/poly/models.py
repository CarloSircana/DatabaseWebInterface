# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ClassGroup(models.Model):
    class_group_id = models.AutoField(primary_key=True)
    group_order = models.DecimalField(max_digits=65535, decimal_places=65535)
    structure = models.TextField()  # This field type is a guess.
    prime_divisors = models.TextField()  # This field type is a guess.
    ranks = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'class_group'


class Completeness(models.Model):
    grh = models.BooleanField(primary_key=True)
    group = models.ForeignKey('GaloisGroup', models.DO_NOTHING)
    real_embeddings = models.SmallIntegerField()
    discriminant_bound = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'completeness'
        unique_together = (('grh', 'group', 'real_embeddings'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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


class Field(models.Model):
    field_id = models.BigAutoField(primary_key=True)
    polynomial = ArrayField(base_field = models.IntegerField(), unique=True)  # This field type is a guess.
    degree = models.SmallIntegerField()
    real_embeddings = models.SmallIntegerField()
    class_group = models.ForeignKey(ClassGroup, models.DO_NOTHING, blank=True, null=True)
    ramified_primes = models.TextField(blank=True, null=True)  # This field type is a guess.
    regulator = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    discriminant = models.DecimalField(max_digits=65535, decimal_places=65535)
    grh = models.BooleanField(blank=True, null=True)
    group = models.ForeignKey('GaloisGroup', models.DO_NOTHING, blank=True, null=True)
    cm = models.BooleanField(blank=True, null=True)
    torsion_size = models.IntegerField(blank=True, null=True)
    automorphisms_order = models.SmallIntegerField(blank=True, null=True)
    is_canonical_poly = models.BooleanField(blank=True, null=True)
    subfields = models.TextField(blank=True, null=True)  # This field type is a guess.

    def get_degree(self):
        return self.degree

    # def get_discriminant(self):
    #     return self.discriminant

    def __str__(self):
        return str(self.polynomial)

    class Meta:
        managed = False
        db_table = 'field'


class GaloisGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_order = models.DecimalField(max_digits=65535, decimal_places=65535)
    degree = models.IntegerField()
    transitive_group_id = models.IntegerField(blank=True, null=True)
    small_group_id = models.IntegerField(blank=True, null=True)
    generators = models.CharField(unique=True, max_length=1, blank=True, null=True)
    abelian = models.BooleanField()
    nilpotent = models.BooleanField()
    solvable = models.BooleanField()
    primitive = models.BooleanField()
    perfect = models.BooleanField()
    issimple = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'galois_group'
