from django.db import migrations, models


def migrate_clubmember_roles(apps, schema_editor):

    ClubMember = apps.get_model("events", "ClubMember")

    for member in ClubMember.objects.all():

        if member.role == "PRESIDENT":
            member.membership_type = "CORE"
            member.is_president = True

        elif member.role == "CORE":
            member.membership_type = "CORE"
            member.is_president = False

        else:
            member.membership_type = "MEMBER"
            member.is_president = False

        member.save()


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0010_alter_clubmember_role"),
    ]

    operations = [

        # First add the new fields
        migrations.AddField(
            model_name="clubmember",
            name="is_president",
            field=models.BooleanField(default=False),
        ),

        migrations.AddField(
            model_name="clubmember",
            name="membership_type",
            field=models.CharField(
                choices=[
                    ("CORE", "Core Member"),
                    ("MEMBER", "Member"),
                ],
                default="MEMBER",
                max_length=20,
            ),
        ),

        migrations.AddField(
            model_name="clubmember",
            name="position",
            field=models.CharField(
                blank=True,
                max_length=100,
            ),
        ),

        # Copy old role data into the new fields
        migrations.RunPython(
            migrate_clubmember_roles,
            migrations.RunPython.noop,
        ),

        # Only now remove the old role field
        migrations.RemoveField(
            model_name="clubmember",
            name="role",
        ),
    ]