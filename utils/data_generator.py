import random
import string

from faker import Faker

fake = Faker()


class DataGenerator:
    @staticmethod
    def generate_random_email():
        letters = string.ascii_lowercase
        numbers = string.digits
        # складываем все буквы и цифры и из результата берем рандомные 8
        shake_chars = random.choices(letters + numbers, k=8)
        rand_chars = "".join(shake_chars)
        return f"{rand_chars}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{fake.first_name()} {fake.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        - Минимум 1 буква.
        - Минимум 1 заглавная буква.
        - Минимум 1 цифра.
        - Минимум 1 спецсимвол
        - Длина от 8 до 20 символов.
        """
        lower_letter = random.choice(string.ascii_lowercase)
        upper_letter = random.choice(string.ascii_uppercase)
        number = random.choice(string.digits)
        special_chars = "?@#$%^&*|:"
        special_char = random.choice(special_chars)
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(4, 16)

        remaining_chars = "".join(random.choices(all_chars, k=remaining_length))
        required = lower_letter + upper_letter + number + special_char
        password = list(required + remaining_chars)
        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_random_movie_name():
        movie_name = " ".join(fake.words(random.randint(2, 4))).title()
        return movie_name
