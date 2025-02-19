from django.core.management.base import BaseCommand
from mailings.models import Mailing


class Command(BaseCommand):
    help = "Отправить рассылку вручную"

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            if mailing.status == 'created':
                mailing.send()
                self.stdout.write(self.style.SUCCESS(f'✅ Рассылка "{mailing.subject}" отправлена!'))
            else:
                self.stdout.write(self.style.WARNING(f'Рассылка "{mailing.subject}" уже отправлена или в процессе!'))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR('Рассылка с таким ID не найдена.'))
