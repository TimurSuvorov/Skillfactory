from django.core.management import BaseCommand, CommandError

from news.models import Category, Post


class Command(BaseCommand):
    help = 'Удаление постов по выбранной категории'
    missing_args_message = 'Отсутствуют аргументы команды'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        cats = Category.objects.all().values_list('catname', flat=True)
        parser.add_argument('-c', '--category', nargs='+', choices=cats)

    def handle(self, *args, **options):
        cats_args = options['category']
        print(cats_args)
        cats_args_str = ', '.join(cats_args)
        xposts = Post.objects.filter(category__catname__in=cats_args)
        if xposts:
            self.stdout.write(f'Вы уверены, что хотите удалить все новости из категорий: "%s"  ?' % cats_args_str)
            answer = input("Y/n: ")
        else:
            self.stdout.write(self.style.WARNING(f'Нет постов из категорий: "%s"' % cats_args_str))
            return

        if answer == 'Y':
            xposts.delete()
            self.stdout.write(self.style.SUCCESS('Все посты из категорий: "%s" удалены' % cats_args_str))
            return

        raise CommandError('Удаление отклонено')

