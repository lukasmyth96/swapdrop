from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile


class Command(BaseCommand):

    def handle(self, *args, **options):
        # if not User.objects.filter(username="admin").exists():
        #     User.objects.create_superuser("admin", "admin@admin.com", "admin")
        user = User.objects.get(username='admin')
        profile = Profile(user=user)
        profile.save()
