from django.db import migrations, models

def set_default_quantity(apps, schema_editor):
    ClassTicket = apps.get_model('fiton', 'ClassTicket')
    for ticket in ClassTicket.objects.all():
        ticket.ticket_quantity = 1  # 기본값 설정
        ticket.save()

class Migration(migrations.Migration):
    dependencies = [
        ('fiton', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classticket',
            name='ticket_quantity',
            field=models.PositiveIntegerField(default=1, verbose_name="수업권 횟수"),
        ),
        migrations.RunPython(set_default_quantity),
    ]