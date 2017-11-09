import sys
from itertools import chain, repeat
from dialogsgenerator.agent import Agent
from random import randint

class RandomDialog(object):
    
    def __init__(self, agents, max_len=5):
        # Инициализация
        self.agents = agents
        self.agents_num = len(agents)
        self.max_len = max_len
    
    def generate(self):
        """
        Генерирует случайный диалог состоящий из 1-max_len цепочек.
        При генерации вызывает функцию turn.
        Возвращаемый объект является генератором.
        """
        
        """
        ______________________________________________________________________________________
            Мы хотим вернуть (max_len - 1) цепочек ходов, для этого нам нужно (max_len - 1) раз 
            вызвать turn(), но чтобы каждый раз метод turn() возвращал разные диалоги.

             * self_n_times - пары (i, self), где i = 0..max_len-1
             * invoke_turn - вызывает функцию turn у своего второго аргумента (второй аргумент - self)

            Возьмём map от self_n_times, к котором применён invoke_turn, получим то, что нужно            
        """
        
        # пары - (i, self), где i = 1..max_len-1
        self_n_times = zip(range(self.max_len - 1), repeat(self))
        
        # вызывает turn() у второго аргумента
        invoke_turn = lambda args: list(args[1].turn())
        
        # для каждой пары (i, self) вызываем invoke_turn от self
        yield from map(invoke_turn, self_n_times)

    def turn(self):
        """
        Генерирует одну случайную цепочку следующим образом: выбирается случайный агент.
        Он "говорит" случайное сообщение (msg) из своей Agent.kb (используйте next или send(None)).
        (правила того, как выбирать никак не регулируются, вы можете выбирать случайный твит из Agent.kb никак не учитывая
        переданное msg).
        Это сообщение передается с помощью send (помним, что агент - это объект-генератор).
        Далее получаем ответ от всех агентов и возвращаем (генерируем) их (включая исходное сообщение).
        Возвращаемый объект является генератором.
        """
        
        # получаем сообщение от случайного агента
        rand_agent_ind = randint(0, self.agents_num - 1)
        msg = next(self.agents[rand_agent_ind])
        
        # отправляем сообщение всем агентам
        _ = list(map(lambda x: x.send(msg), self.agents))

        # возвращаем ответы всех агентов вместе с исходным сообщением
        it = iter(self.agents)
        yield from chain([msg], list(map(next, it)))

    def eval(self, dialog=None):
        """
        Превращает генератор случайного далога (который возвращается в self.generate())
        в список списков (пример использования далее).
        Возвращаемый объект является списком.
        """
        if dialog is None:
            dialog = self.generate()
                
        return list(dialog)      

    def write(self, dialog=None, target=sys.stdout):
        """
        Записывает результат self.eval() в соответствующий поток.
        """
        
        if dialog is None:
            dialog = self.eval()
        
        # приписывает к очередному ходу \t
        sep_turns = lambda turn: "\t" + turn
        
        # описание диалога - сначала отдаёт строку с номером диалога, а затем сами сообщения
        turn_desc = lambda turn_obj: list(chain(["turn {}:".format(turn_obj[0])], 
                                           map(sep_turns, turn_obj[1])))
        
        # выводит каждое описание диалога
        print_dialog = lambda turn: list(map(lambda x: print(x, file=target), turn_desc(turn)))
        
        list(map(print_dialog, enumerate(dialog)))
        
    pass