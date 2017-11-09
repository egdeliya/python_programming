from itertools import chain, repeat
from dialogsgenerator import Agent, RandomDialog
import io
import sys
import pandas as pd
import codecs

def generate(rd, count_dialogs=5):
    """
    Генерирует count_dialogs диалогов с помощью rd.generate().
    Возвращаемый объект является генератором.
    """
    # пары - (i, rd), где i = 1..count_dialogs
    rd_n_times = zip(range(count_dialogs), repeat(rd))

    # вызывает generate() у второго аргумента
    invoke_generate = lambda args: args[1].generate()

    # у каждой пары (i, rd) вызываем invoke_generate от rd
    yield from map(invoke_generate, rd_n_times)
    

def write(dialogs, target):
    """
    Записывает сгенерированные диалоги dialogs (это объект-генератор) в поток target.
    """

    # выводит сначала номер диалога, а затем вызывает функцию write у самого диалога
    def print_dialog_descr(dialog_obj):
        print("_______________________Dialog {}______________________".format(dialog_obj[0]), file=target)

        rd = RandomDialog([], 0)
        evaluate = rd.eval(dialog_obj[1])
        rd.write(evaluate)
        
    
    print_dialogs = lambda dialog_obj: print_dialog_descr(dialog_obj)
   
    list(map(print_dialogs, enumerate(dialogs)))

import argparse
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # ------------------парсим аргументы------------------------------------
    parser.add_argument("-o", "--output", help=u"Поток, в который будет производиться вывод"),
                        action="store_true")
    parser.add_argument("-t", "--trump_kb", help=u"Файл с репликами для ответов Трампа",
                        action="store_true")
    parser.add_argument("-c", "--clinton_kb", help=u"Файл с репликами для ответов Клинтон",
                        action="store_true")
    parser.add_argument("count_dialog", type=int,
                        help=u"Количество диалогов, которые необходимо сгенерировать")
    parser.add_argument("max_dialog_len", type=int,
                        help=u"Максимальное количество цепочек в одном диалоге")
    args = parser.parse_args()
    
    # ------------------ в зависимости от аргументов делаем различные действия------------------------------------
    clinton = pd.read_csv("clinton.csv", encoding="utf-8")
    trump = pd.read_csv("trump.csv", encoding="utf-8")

    output_stream = sys.stdout
    if (args.output):
        output_stream = args.output
    if (args.trump_kb):
        trump = pd.read_csv(args.trump_kb, encoding="utf-8") 
    if (args.clinton_kb):
        clinton = pd.read_csv(args.clinton_kb, encoding="utf-8") 
    
    # ------------------ создаём генератор и запускаем его ------------------------------------
    rd = RandomDialog([Agent(clinton, "clinton"), Agent(trump, "trump")], max_len=args.max_dialog_len)
    dialogs = generate(rd, args.count_dialog)
    write(dialogs, output_stream)