from django.core.management.base import BaseCommand
from webapp.models import Client


class Command(BaseCommand):
    help = "delete_client"

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='Идентификатор пользователя')

    def handle(self, *args, **options):
        pk = options.get('pk')

        client = Client.objects.filter(pk=pk).first()
        if client is not None:
            client.delete()

        self.stdout.write(f'f{client}')