# deals/tests/tests_models.py
from django.test import TestCase
from posts.models import Post, Group

class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
                # и сохраняем ее в качестве переменной класса                
        # Не указываем значение slug, ждем, что при создании
        # оно создастся автоматически из title.
        # А title сделаем таким, чтобы после транслитерации он стал более 
        # 100 символов 
        # (буква "ж" транслитерируется в два символа: "zh")
        # Создаём тестовую запись в БД
        # 
        cls.post = Post.objects.create(text='ж'*60)
        cls.group = Group.objects.create(title='hello')

    def test_text_convert_to_slug(self):
        """save преобразует в slug содержимое поля title."""
        groups = GroupModelTest.group
        title = groups.__str__()
        slug = title.slug
        self.assertEqual(slug, 'hello')

