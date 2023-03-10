# Generated by Django 4.0.1 on 2022-12-15 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')),
                ('full_name', models.CharField(max_length=250, verbose_name='Nombre y Apellidos')),
            ],
            options={
                'verbose_name': 'Autor',
                'verbose_name_plural': 'Autores',
                'ordering': ['-created_at'],
                'permissions': (('manage_author', 'Puede Administrar Autores'),),
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')),
                ('title', models.CharField(max_length=150, verbose_name='Título')),
                ('summary', models.CharField(blank=True, max_length=500, null=True, verbose_name='Resumen')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Cantidad de Ejemplares')),
                ('in_stock', models.PositiveIntegerField(default=1, verbose_name='Cantidad Disponible')),
                ('author', models.ManyToManyField(related_name='books', to='core.Author', verbose_name='Autor')),
            ],
            options={
                'verbose_name': 'Libro',
                'verbose_name_plural': 'Libros',
                'ordering': ['-created_at'],
                'permissions': (('manage_book', 'Puede Administrar Libros'),),
            },
        ),
        migrations.CreateModel(
            name='BookLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')),
                ('status', models.CharField(choices=[('in_time', 'En Tiempo'), ('past', 'Fuera de Tiempo'), ('returned', 'Entregado')], default='in_time', max_length=8, verbose_name='Estado')),
                ('end_date', models.DateField(verbose_name='Fecha de Entrega')),
                ('books', models.ManyToManyField(related_name='book_loan', to='core.Book', verbose_name='Libros')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_loan', to='customers.customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Préstamo',
                'verbose_name_plural': 'Préstamos',
                'ordering': ['-created_at'],
                'permissions': (('manage_book_loan', 'Puede Administrar Préstamos'),),
            },
        ),
    ]
