import random
import string


class RandomGenerate(object):
    @staticmethod
    def generate_random_email(length=random.randint(5, 10)):
        letters = string.ascii_lowercase
        rand_email_first_part = ''.join(random.sample(letters, length))
        rand_email_second_part = random.choice(["@mail.ru", "@bk.ru", "@ya.ru", "@gmail.com", "@vk.com"])
        return rand_email_first_part + rand_email_second_part

    @staticmethod
    def generate_random_password():
        letters_digits = string.digits
        letters_symbols_low = string.ascii_lowercase
        letters_symbols_ap = string.ascii_uppercase
        letters = letters_digits + letters_symbols_low + letters_symbols_ap
        length = random.randint(5, 20)
        rand_password = ''.join(random.sample(letters, length))

        return rand_password

    @staticmethod
    def generate_random_name():
        letters_symbols_low = string.ascii_lowercase
        letters_symbols_ap = string.ascii_uppercase
        letters = letters_symbols_ap + letters_symbols_low
        length = random.randint(5, 20)
        rand_name = ''.join(random.sample(letters, length))

        return rand_name
