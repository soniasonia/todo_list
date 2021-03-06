# Generated by Django 2.2.4 on 2019-08-16 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('list', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='list_app.List')),
            ],
            options={
                'ordering': ('id',),
                'unique_together': {('list', 'text')},
            },
        ),
    ]
