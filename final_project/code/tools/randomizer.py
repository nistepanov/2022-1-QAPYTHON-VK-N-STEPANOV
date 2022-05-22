import random
import string


class RandomGenerate:

    @staticmethod
    def generate_random_email(left_bound=6, right_bound=16, first_half=0, second_half=0):
        letters_symbols_low = string.ascii_lowercase
        letters_symbols_ap = string.ascii_uppercase
        letters_digits = string.digits
        letters = (letters_symbols_low + letters_symbols_ap + letters_digits) * left_bound
        length = random.randint(left_bound, right_bound)
        if first_half:
            rand_email_first_part = ''.join(random.sample(letters, length))
            return rand_email_first_part
        if second_half:
            rand_email_second_part = random.choice(["@mail.ru", "@bk.ru", "@ya.ru", "@gmail.com", "@vk.com"])
            return rand_email_second_part
        else:
            rand_email_first_part = ''.join(random.sample(letters, length))
            rand_email_second_part = random.choice(["@mail.ru", "@bk.ru", "@ya.ru", "@gmail.com", "@vk.com"])
            return rand_email_first_part + rand_email_second_part

    @staticmethod
    def generate_random_password(left_bound=6, right_bound=16):
        letters_digits = string.digits
        letters_symbols_low = string.ascii_lowercase
        letters_symbols_ap = string.ascii_uppercase
        letters = (letters_digits + letters_symbols_low + letters_symbols_ap) * left_bound
        length = random.randint(left_bound, right_bound)
        rand_password = ''.join(random.sample(letters, length))

        return rand_password

    @staticmethod
    def generate_random_user_name(left_bound=6, right_bound=16):
        letters_digits = string.digits
        letters_symbols_low = string.ascii_lowercase
        letters_symbols_ap = string.ascii_uppercase
        letters = (letters_symbols_ap + letters_symbols_low + letters_digits) * left_bound
        length = random.randint(left_bound, right_bound)
        rand_user_name = ''.join(random.sample(letters, length))

        return rand_user_name
