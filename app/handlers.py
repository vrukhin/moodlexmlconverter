import xml.etree.ElementTree as ET


def multichoice_handler(tree, query, question_number):
    """обработчик вопросов типа multichoice.
    Args:
        tree: xml-дерево с вопросами
        query (string): вопрос в формате списка
        question_number (int): порядковый номер вопроса
    Returns:
        tree: xml-дерево с новым вопросом
    """
    # словарь с баллами moodle
    grades = {
        -5:'-5', -10:'-10', -11:'-11.11111', -12:'-12.5', -14:'-14.285711', -16:'-16.66667', -20:'-20', -25:'-25',
        -30:'-30', -33:'-33.33333', -40:'-40', -50:'-50', -60:'-60', -66:'-66.66667', -70:'70', -75:'-75', -80:'-80',
        -83:'-83.3333', -90:'-90', -100:'0',
        5:'5', 10:'10', 11:'11.11111', 12:'12.5', 14:'14.285711', 16:'16.66667', 20:'20', 25:'25',
        30:'30', 33:'33.33333', 40:'40', 50:'50', 60:'60', 66:'66.66667', 70:'70', 75:'75', 80:'80',
        83:'83.3333', 90:'90', 100:'100',
    }

    query_text = query.pop(0) # извлекаем текст вопроса
    answers = list()
    scores = {'+':0, '-':0}
    for q in query:
        answer = dict()
        answer["text"] = q[:-2]
        answer["grade"] = q[-1]
        scores[q[-1]] += 1
        answers.append(answer)

    scores['+'] = grades[int(100/scores['+'])] # пересчитываем баллы в шкалу %
    scores['-'] = grades[-int(100/scores['-'])] if scores['+'] != "100" else "0"

    # получаем корень дерева
    root = tree.getroot() 
    # добавляем дочерний элемент "question"
    question = ET.SubElement(root, "question", {"type":"multichoice"})
    # название и текст вопроса
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = "q{}".format(question_number)
    questiontext = ET.SubElement(question, "questiontext", {"format":"markdown"})
    questiontext_text = ET.SubElement(questiontext, "text")
    questiontext_text.text = query_text

    # стоимость вопроса
    defaultgrade = ET.SubElement(question, 'defaultgrade')
    defaultgrade.text = '1.0000000'

    # штраф
    penalty = ET.SubElement(question, 'penalty')
    penalty.text = '0.0000000'

    # хз что это О_о
    hidden = ET.SubElement(question, 'hidden')
    hidden.text = '0'

    # id - вопроса
    idnumber = ET.SubElement(question, 'idnumber')
    idnumber.text = "q{}".format(question_number)

    # количество правильных ответов (если true, будут радиобатоны, иначе -- чекбоксы)
    single = ET.SubElement(question, 'single')
    single.text = 'true' if scores['+'] == '100' else 'false'

    # случайный порядок ответов
    shuffleanswers = ET.SubElement(question, 'shuffleanswers')
    shuffleanswers.text = 'true'

    # нумерация ответов
    answernumbering = ET.SubElement(question, 'answernumbering')
    answernumbering.text = 'none' # allowed values: 'none', 'abc', 'ABCD' or '123'

    # показать стандартные инструкции 
    showstandardinstruction = ET.SubElement(question, 'showstandardinstruction')
    showstandardinstruction.text = '0'

    # отзывы на ответы
    correctfeedback = ET.SubElement(question, 'correctfeedback', {'format':'html'})
    text = ET.SubElement(correctfeedback, 'text')
    text.text = 'Ваш ответ верный.'

    partiallycorrectfeedback = ET.SubElement(question, 'partiallycorrectfeedback', {'format':'html'})
    text = ET.SubElement(partiallycorrectfeedback, 'text')
    text.text = 'Ваш ответ частично правильный.'

    incorrectfeedback = ET.SubElement(question, 'incorrectfeedback', {'format':'html'})
    text = ET.SubElement(incorrectfeedback, 'text')
    text.text = 'Ваш ответ неправильный.'

    for ans in answers:
        answer = ET.SubElement(question, "answer", {"fraction":scores[ans["grade"]]})
        answer_text = ET.SubElement(answer, "text")
        answer_text.text = ans["text"]
        
    tree = ET.ElementTree(root)
    return tree


def truefalse_handler(tree, query, question_number):
    root = tree.getroot()
    tree = ET.ElementTree(root)
    return tree


def matching_handler(tree, query, question_number):
    root = tree.getroot()
    tree = ET.ElementTree(root)
    return tree


def shortanswer_handler(tree, query, question_number):
    root = tree.getroot()
    tree = ET.ElementTree(root)
    return tree


def numerical_handler(tree, query, question_number):

    query_text = query.pop(0) # извлекаем текст вопроса

    # получаем корень дерева
    root = tree.getroot() 

    # добавляем дочерний элемент "question"
    question = ET.SubElement(root, "question", {"type":"numerical"})

    # название и текст вопроса
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = "q{}".format(question_number)
    questiontext = ET.SubElement(question, "questiontext", {"format":"markdown"})
    questiontext_text = ET.SubElement(questiontext, "text")
    questiontext_text.text = query_text

    # ответ
    answer = ET.SubElement(question, "answer", {"fraction":"100", "format":"moodle_auto_format"})
    answer_text = ET.SubElement(answer, "text")
    answer_text.text = query.pop(0)

    # допустимое отклонение
    tolerance = ET.SubElement(answer, "tolerance")
    tolerance.text = "0"

    tree = ET.ElementTree(root)
    return tree


def essay_handler(tree, query, question_number):
    query_text = query.pop(0) # извлекаем текст вопроса

    # получаем корень дерева
    root = tree.getroot() 

    # добавляем дочерний элемент "question"
    question = ET.SubElement(root, "question", {"type":"essay"})

    # название и текст вопроса
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = "q{}".format(question_number)
    questiontext = ET.SubElement(question, "questiontext", {"format":"markdown"})
    questiontext_text = ET.SubElement(questiontext, "text")
    questiontext_text.text = query_text

    # формат ответа
    responseformat = ET.SubElement(question, "responseformat")
    responseformat.text = "monospaced"

    # заполнение поля ответа обязательно
    responserequired = ET.SubElement(question, "responserequired")
    responserequired.text = "1"

    # размер поля ответа
    responsefieldlines = ET.SubElement(question, "responsefieldlines")
    responsefieldlines.text = "15"

    # разрешить/запретить вложения
    attachments = ET.SubElement(question, "attachments")
    attachments.text = "0"

    # (не)требовать вложения
    attachmentsrequired = ET.SubElement(question, "attachmentsrequired")
    attachmentsrequired.text = "0"

    root = tree.getroot()
    tree = ET.ElementTree(root)
    return tree



