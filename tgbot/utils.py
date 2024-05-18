import types

import requests
import re
import config
import codecs

num_trofies = 0


def PrinterTroph() -> int:
    html = open("output.txt", "r", encoding='utf-8').read()
    match = re.search(r'Трофеи', html)
    start_index = match.start()
    end_index = match.end()
    substring = (html[start_index:end_index + 200])
    cut = re.search(r'text-warning">', substring)
    end = cut.end()
    symb = substring[end]
    num_trophies = 0
    decimal = 0
    while substring[end] != '<':
        if substring[end] == ',':
            end += 1
            continue
        number = int(substring[end])
        mnozh = 10 ** decimal
        second = number * mnozh
        num_trophies += second
        end += 1
        decimal = decimal + 1
    digit = num_trophies % 10
    n2 = digit

    # Избавляемся от последней цифры первого числа
    n1 = num_trophies // 10

    while n1 > 0:
        # находим остаток - последнюю цифру
        digit = n1 % 10
        # делим нацело - удаляем последнюю цифру
        n1 = n1 // 10
        # увеличиваем разрядность второго числа
        n2 = n2 * 10
        # добавляем очередную цифру
        n2 = n2 + digit
    return n2


def PrinterTrophOfBrawler(Brawler) -> list:
    with codecs.open('output.txt', 'r', encoding='utf-8') as f:
        needed_line = f.readlines()[259]
    match = re.search(Brawler, needed_line)
    cut = needed_line[match.start():len(needed_line)]
    end_index = re.search(",&quot;gears&quot;:", cut)
    full_cut = cut[:end_index.start()]
    INFO_ABOUT_BRAWLER = []
    for number in full_cut.split(","):
        try:
            if ":" in number:
                number = int(number.split(":")[1])
            INFO_ABOUT_BRAWLER.append(number)
        except ValueError:
            continue
    return INFO_ABOUT_BRAWLER
def PrinterBoosts() -> list:
    with codecs.open('output.txt', 'r', encoding='utf-8') as f:
        needed_line = f.readlines()[290]
    match_start = re.search('text-success">+', needed_line)
    match_end = re.search('</span> этой нед', needed_line)
    ANS1 = needed_line[match_start.end(): match_end.start()]
    with codecs.open('output.txt', 'r', encoding='utf-8') as f:
        needed_line = f.readlines()[291]
    match_start = re.search('text-success">+', needed_line)
    match_end = re.search('</span> этой', needed_line)
    ANS2 = needed_line[match_start.end(): match_end.start()]
    return [ANS1, ANS2]
def InfoPlayer() -> list:
    with codecs.open('output.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        needed_line1 = lines[548]
        needed_line2 = lines[552]
        needed_line3 = lines[556]
        # needed_line4 = lines[560]

    match_start = re.search('shadow-normal">', needed_line1)
    match_end = re.search('</td>', needed_line1)
    ANS1 = needed_line1[match_start.end() + 1: match_end.start()]
    match_start = re.search('shadow-normal">', needed_line2)
    match_end = re.search('</td>', needed_line2)
    ANS2 = needed_line2[match_start.end(): match_end.start()]
    match_start = re.search('shadow-normal">', needed_line3)
    match_end = re.search('</td>', needed_line3)
    ANS3 = needed_line3[match_start.end(): match_end.start()]
    return [ANS1, ANS2, ANS3]
def Brawlers() -> list:
    with codecs.open('output.txt', 'r', encoding='utf-8') as f:
        needed_line = f.readlines()[543]
    match_start1 = re.search('shadow-normal">', needed_line)
    match_end1 = re.search('<span class="text-muted"> / ', needed_line)
    match_start2 = re.search('<span class="text-muted"> / ', needed_line)
    match_end2 = re.search("</span></td>", needed_line)
    ANS1 = needed_line[match_start1.end(): match_end1.start()]
    ANS2 = needed_line[match_start2.end(): match_end2.start()]
    number_my = int(ANS1)
    number_max = int(ANS2)
    ANS3 = (round(number_my/number_max, 4)) * 100

    return [ANS1, ANS2, ANS3]
def CheckerOfUser(username: str) -> str:
    with codecs.open('database.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Объединяем все строки в одну строку
    text = ''.join(lines)

    # Ищем имя пользователя в тексте
    match = re.search(username, text)

    # Если найдено, возвращаем тег
    if match:
        start_index = match.start()
        tag = text[start_index - 10:start_index]
        return tag
    # Иначе, возвращаем 0
    else:
        return " "
def RewriteTag(tag: str, username: str):
    username = username
    tag = tag
    with codecs.open('database.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if username in line:
            # Заменяем строку с именем пользователя и тегом на новую строку с новым тегом
            updated_lines.append(tag + " " + username + "\n")
        else:
            updated_lines.append(line)

    # Перезаписываем файл с обновленными строками
    with codecs.open('database.txt', 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
