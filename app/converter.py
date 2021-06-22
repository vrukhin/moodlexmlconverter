import os
from glob import glob
import xml.etree.ElementTree as ET
from handlers import multichoice_handler, truefalse_handler, matching_handler, shortanswer_handler, numerical_handler, essay_handler


def read_quiz(data):
    """Считывает вопросы из текстового файла.
    Args:
        data (string): путь к файлу с вопросами
    Returns:
        questions (list): список с вопросами и ответами
        Структура списка questions:
            [
                'Название теста',
                ['тип вопроса 1', 'Вопрос 1', 'Ответ 1', 'Ответ 2', 'Ответ 3'],
                ['тип вопроса 2', 'Вопрос 2', 'Ответ 1', 'Ответ 2', 'Ответ 3'],
                ['тип вопроса n', 'Вопрос n', 'Ответ 1', 'Ответ 2', 'Ответ 3']
            ]
    """
    lines = open(data, 'r').read().splitlines() # получаем список строк из файла
    questions = list()
    questions.append(lines.pop(0)) # берем первый элемент

    # превращаем список со строками в двухмерный список вопросов
    for line in lines:
        if line == '':
            questions.append([])
        else:
            questions[-1].append(line)
    return questions # //TODO: Сделать проверку на наличие "пустых" вопросов


def search_files():
    """Ищет файлы формата .md в папке data
    Returns:
        files (list): список найденных файлов
    """
    files = [y for x in os.walk('./data/') for y in glob(os.path.join(x[0], '*.md'))]
    return files


def convert_to_xml(data):
    tree = ET.ElementTree(ET.Element("quiz")) # создаем дерево с корневым элементом "quiz"
    questions = read_quiz(data) # считываем вопросы из текстового файла

    title = questions.pop(0) # убираем название теста из перечня вопросов
    
    question_number = 0 # счетчик вопросов (является частью названия вопроса)
    for question in questions:
        question_number += 1
        tree = handlers[question.pop(0)](tree, question, question_number)

    return tree


def main(files):
    for f in files:
        convert_to_xml(f).write(f[:-2]+'xml', encoding='utf-8')


handlers = dict()
handlers["multichoiсe"] = multichoice_handler
handlers["truefalse"] = truefalse_handler
handlers["matching"] = matching_handler
handlers["shortanswer"] = shortanswer_handler
handlers["numerical"] = numerical_handler
handlers["essay"] = essay_handler

files = search_files()

main(files)
