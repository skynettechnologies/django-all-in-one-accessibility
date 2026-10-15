from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessibility', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AioaDomainRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255, unique=True)),
                ('registered', models.BooleanField(default=False)),
                ('attempts', models.PositiveSmallIntegerField(default=0)),
                ('no_required_eu', models.PositiveSmallIntegerField(default=1)),
                ('last_status_code', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('last_attempt_at', models.DateTimeField(blank=True, null=True)),
                ('registered_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'AIOA domain registration',
                'verbose_name_plural': 'AIOA domain registrations',
            },
        ),
    ]
