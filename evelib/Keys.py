import os
import yaml
import random
import string

class SqlKey:

    PASSKEY_LEN = 30

    def __init__(self, value=None):
        self.__value = value

    def __str__(self):
        return self.__value

    @classmethod
    def create_random_key(cls):
        allowed_chars = string.ascii_letters + string.digits + "!#$#"
        key = ""
        for _ in range(cls.PASSKEY_LEN):
            key += random.SystemRandom().choice(allowed_chars)
        return cls(key)


class Keys:

    LOCATION = os.path.dirname(os.path.abspath(__file__) + ".keys.yaml")

    KEYS_TRACKED = {
        'sql_user': SqlKey()
    }

    def __getattr__(self, item):
        return self.dict[item]

    def __init__(self, key_location=LOCATION):
        # Set key_location to None for a blank dict
        super().__init__()
        if key_location is None:
            self.dict = self.KEYS_TRACKED
        else:
            file = open(key_location, 'r')
            self.dict = yaml.load(file)
            file.close()

    @classmethod
    def generate_random_keys(cls, key_location=LOCATION):
        if os.path.exists(key_location):
            raise FileExistsError()
        keys = cls(None)
        for key in keys.dict:
            keys.dict[key] = str(keys.dict[key].create_random_key())
        file = open(key_location, 'w')
        yaml.dump(keys.dict, file)
        file.close()
