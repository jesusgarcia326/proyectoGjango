# Generated by Django 5.1.7 on 2025-04-08 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_entrada_alter_usuario_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discoteca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('aforo', models.IntegerField()),
            ],
        ),
    ]
