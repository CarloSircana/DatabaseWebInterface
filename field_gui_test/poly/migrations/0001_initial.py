# Generated by Django 3.1.2 on 2021-08-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClassGroup',
            fields=[
                ('class_group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_order', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('structure', models.TextField()),
                ('prime_divisors', models.TextField()),
                ('ranks', models.TextField()),
            ],
            options={
                'db_table': 'class_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Completeness',
            fields=[
                ('grh', models.BooleanField(primary_key=True, serialize=False)),
                ('real_embeddings', models.SmallIntegerField()),
                ('discriminant_bound', models.DecimalField(decimal_places=65535, max_digits=65535)),
            ],
            options={
                'db_table': 'completeness',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('field_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('polynomial', models.TextField(unique=True)),
                ('degree', models.SmallIntegerField()),
                ('real_embeddings', models.SmallIntegerField()),
                ('ramified_primes', models.TextField(blank=True, null=True)),
                ('regulator', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('discriminant', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('grh', models.BooleanField(blank=True, null=True)),
                ('cm', models.BooleanField(blank=True, null=True)),
                ('torsion_size', models.IntegerField(blank=True, null=True)),
                ('automorphisms_order', models.SmallIntegerField(blank=True, null=True)),
                ('is_canonical_poly', models.BooleanField(blank=True, null=True)),
                ('subfields', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'field',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GaloisGroup',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_order', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('degree', models.IntegerField()),
                ('transitive_group_id', models.IntegerField(blank=True, null=True)),
                ('small_group_id', models.IntegerField(blank=True, null=True)),
                ('generators', models.CharField(blank=True, max_length=1, null=True, unique=True)),
                ('abelian', models.BooleanField()),
                ('nilpotent', models.BooleanField()),
                ('solvable', models.BooleanField()),
                ('primitive', models.BooleanField()),
                ('perfect', models.BooleanField()),
                ('issimple', models.BooleanField()),
            ],
            options={
                'db_table': 'galois_group',
                'managed': False,
            },
        ),
    ]
