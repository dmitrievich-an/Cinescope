import pytest


# Исключаем весь модуль из тестов
pytestmark = pytest.mark.skip(reason="Тесты отключены за ненадобностью")

class TestMark:
    """Создайте тесты с метками: +skip, +skipif, +xfail, +usefixtures."""

    @pytest.mark.skip()
    def test_skip(self):
        assert 2 == 3

    statement = 5 > 3

    @pytest.mark.skipif(statement, reason="Тест отключен")
    def test_skipif(self):
        assert True

    @pytest.mark.xfail(reason="Функция не готова")
    def test_xfail(self):
        assert 3 == 4

    @pytest.fixture
    def fixture(self):
        return print("Hi, man")

    @pytest.mark.usefixtures("fixture")
    def test_usefixture(self):
        assert 2 == 2


class TestCustomMark:
    @pytest.mark.smoke
    def test_addition(self):
        assert 1 + 1 == 2

    @pytest.mark.regression
    def test_subtraction(self):
        assert 5 - 3 == 2

    @pytest.mark.api
    def test_multiplication(self):
        assert 2 * 3 == 6

    @pytest.mark.slow
    def test_division(self):
        assert 10 / 2 == 5

    @pytest.mark.flaky(reruns=10, reruns_delay=1)
    def test_maybe_fails(self):
        import random
        assert random.choice([False, False, False, True])
