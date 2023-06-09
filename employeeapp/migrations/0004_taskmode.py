# Generated by Django 4.1.5 on 2023-05-14 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeapp', '0003_delete_taskmodel2'),
    ]

    operations = [
        migrations.CreateModel(
            name='taskmode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empid', models.CharField(max_length=10)),
                ('task', models.CharField(max_length=250)),
                ('assigndate', models.CharField(max_length=50)),
                ('submitdate', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Submitted', 'Submitted')], default='Pending', max_length=50)),
                ('employeeid', models.IntegerField()),
            ],
        ),
    ]
