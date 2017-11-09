from random import randint
from collections import Generator

class Agent(Generator):
    
    def __init__(self, kb, name):
        # Инициализация
        self.tweets_pool = kb['text']
        self.num_tweets = len(kb)
        self.name = name

    def send(self, msg):
        # Будем возвращать случайное сообщение из self.tweets_pool
        random_idx = randint(0, self.num_tweets - 1)
        return "{} : {}".format(self.name, self.tweets_pool[random_idx])

    def throw(self, typ=None, val=None, tb=None):
        # Оставляем как есть
        super().throw(typ, val, tb)

    def __str__(self):
        # Опишем строковое представление класса
        return self.name

    def __repr__(self):
        return str(self)