from django.core.management.base import BaseCommand, CommandError
from ...models import Post


class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all products? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            Post.objects.filter(postCategory__designation = args).delete()
            self.stdout.write(self.style.SUCCESS('Succesfully wiped products!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим, что в доступе отказано