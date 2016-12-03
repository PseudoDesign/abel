import os
import yaml


class Keys:

    LOCATION = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, key_location=LOCATION):
        file = open(key_location)
        self.keys = yaml.load(file)
        file.close()

    @classmethod
    def generate_random_keys(key_location=LOCATION):
        pass