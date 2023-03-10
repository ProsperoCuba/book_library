# Generated by Django 4.0.1 on 2022-12-15 02:12

import django.core.validators
from django.db import migrations, models
import utils.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')),
                ('document_number', models.CharField(max_length=15, unique=True, verbose_name='DNI/NIE/Pasaporte')),
                ('first_name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=250, verbose_name='Apellidos')),
                ('email', utils.mixins.LowercaseEmailField(blank=True, max_length=128, null=True, verbose_name='Correo')),
                ('phone_number', models.CharField(blank=True, help_text="Teléfono tiene que ser en el formato: '+999999999'. Se permiten hasta 15 dígitos.", max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Teléfono tiene que ser en el formato: '+999999999'. Se permiten hasta 15 dígitos.", regex='\\+(9[976]\\d|8[987530]\\d|6[987]\\d|5[90]\\d|42\\d|3[875]\\d|2[98654321]\\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\\d{1,14}$')], verbose_name='Teléfono')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['-created_at'],
                'permissions': (('manage_customer', 'Puede Administrar Cliente'),),
            },
        ),
    ]
