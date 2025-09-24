from typing import List, Optional, Union

import pytest

from conftest import fake


def multiply(a: int, b: int) -> int:
    return a * b


print(multiply(5, "7"))


def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)


print(sum_numbers([1, 2, 3, 4, 5]))


def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None


print(find_user(3))


def process_input(value: Union[int, str]):
    return f"Ты передал: {value}"


print(process_input(type([4, 5])))


class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"


user = User(777, 32)
print(user.greet())


def get_even_numbers(numbers: List[int]) -> List[int]:
    return [num for num in numbers if num % 2 == 0]


# print(get_even_numbers(["four", "five"]))
print(get_even_numbers([4, 5]))

@pytest.mark.parametrize("movie_id, expected_status", [
        (99999, 404),
        (f"{fake.word()}%EE{fake.word()}", 400)
    ])
def test_delete_movie_with_parametrize(super_admin, movie_id, expected_status):
    super_admin.api.movie_api.delete_movie(movie_id=movie_id, expected_status=expected_status)