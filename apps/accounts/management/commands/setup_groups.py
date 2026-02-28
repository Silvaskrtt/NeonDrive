# apps/accounts/management/commands/setup_groups.py

from django.core.management.base import BaseCommand
from accounts.permissions import create_groups_and_permissions

class Command(BaseCommand):
    help = 'Configura grupos e permissões do sistema'

    def handle(self, *args, **kwargs):
        create_groups_and_permissions()
        self.stdout.write(
            self.style.SUCCESS('✅ Grupos e permissões configurados!')
        )