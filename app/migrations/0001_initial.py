# Generated by Django 5.0.3 on 2024-03-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParsedChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('subscribers', models.IntegerField()),
                ('increment', models.IntegerField()),
                ('post_views', models.IntegerField()),
                ('er', models.FloatField()),
                ('references', models.IntegerField()),
                ('geo', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
            ],
        ),
    ]
