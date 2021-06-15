import unittest


class Calculator:
    def summ(self, *args):
        """Возвращает сумму принятых аргументов."""
        if len(args) < 2:
            return None
        else:
            sum = 0
            for i in args:
                sum += i
            return sum


class TestCalc(unittest.TestCase):
    """Тестируем Calculator."""
    @classmethod
    def setUpClass(cls):
        """Вызывается однажды перед запуском всех тестов класса."""
        cls.calc = Calculator()

    def test_summ(self):
        act = TestCalc.calc.summ(3, -3, 5)
        self.assertEqual(act, 5, 'summ работает неправильно')

    def test_summ_no_argument(self):
        act = TestCalc.calc.summ()
        self.assertIsNone(act, None, 'что то не то')

    def test_summ_one_argument(self):
        act = TestCalc.calc.summ(1)
        self.assertIsNone(act, None, 'что то не то2')