import random
import string


class RandomGenerate(object):

    @staticmethod
    def generate_random_name():
        letters_symbols_low = string.ascii_lowercase
        letters_symbols_ap = string.ascii_uppercase
        letters = letters_symbols_ap + letters_symbols_low
        length = random.randint(5, 20)
        rand_name = ''.join(random.sample(letters, length))

        return rand_name
