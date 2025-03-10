from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Загружает группу "Менеджеры" с правами из фикстуры'

    def handle(self, *args, **kwargs):
        try:
            call_command('loaddata', 'managers_group.json', app_label='mailings')
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" успешно загружена!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке группы: {e}'))
