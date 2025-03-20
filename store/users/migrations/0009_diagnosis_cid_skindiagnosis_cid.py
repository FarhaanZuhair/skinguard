from django.db import migrations, models
import uuid

def populate_unique_cid(apps, schema_editor):
    Diagnosis = apps.get_model('users', 'Diagnosis')
    SkinDiagnosis = apps.get_model('users', 'SkinDiagnosis')

    # Populate unique cid for Diagnosis
    for diagnosis in Diagnosis.objects.filter(cid__isnull=True):
        diagnosis.cid = uuid.uuid4()
        diagnosis.save()

    # Populate unique cid for SkinDiagnosis
    for skin_diagnosis in SkinDiagnosis.objects.filter(cid__isnull=True):
        skin_diagnosis.cid = uuid.uuid4()
        skin_diagnosis.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_diagnosis_diagnosis_result_and_more'),  # Replace with the actual previous migration name
    ]

    operations = [
        # Step 1: Add the cid field with null=True temporarily
        migrations.AddField(
            model_name='diagnosis',
            name='cid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='skindiagnosis',
            name='cid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        # Step 2: Populate unique values for existing rows
        migrations.RunPython(populate_unique_cid),
        # Step 3: Enforce unique=True and disallow null values
        migrations.AlterField(
            model_name='diagnosis',
            name='cid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='skindiagnosis',
            name='cid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]