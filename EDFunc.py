'''Функции шифрования и дешифрования'''

from tkinter import messagebox as msb #Предупреждающие окна
import random #Библиотека для генерации случайных чисел (основы метода шифрования)


def encryption(text: str, password: str, add_symbols: bool, use_csum: bool):
    '''Шифрует полученный текст.
    Возвращает шифротекст.

    text - исходный текст
    password - пароль
    add_symbols - добавить ли символы в шифротекст'''

    #Задаёт сид для генератора псевдослучайных чисел
    random.seed(password + str(len(text)))

    # Перебирает каждый символ исходного текста
    for i in range(len(text)):
        s = text[i]
        sc = ord(s)

        # Перезадаёт сид и генерирует случайное число
        random.seed( ''.join(random.sample(password, len(password)))+str(random.random()) )
        modification = random.randint(0, 55291)

        if random.choice([True, False]):
            if sc + modification > 55291: #Если при сложении превысили 55291, прибавляем лишнее к 0
                text = text[:i] + chr(sc + modification - 55292) + text[i+1:] #Меняет символ на новый
            else:
                text = text[:i] + chr(sc + modification) + text[i+1:]

        else:
            if sc - modification < 0: #Если при вычитании опустились ниже 0, отнимаем лишнее от 55291
                text = text[:i] + chr(sc - modification + 55292) + text[i+1:]
            else:
                text = text[:i] + chr(sc - modification)+ text[i+1:]

    #Если нужно добавить символы в шифротекст (повышает стойкость)
    if add_symbols:
        random.seed(password[::-1]) #Задаёт сид для генератора псевдослучайных чисел
        len_enc = len(text) #Получаем длину шифротекста (будут добавлены 10% символов от исходного кол-ва)
        poses = []
        for i in range(len(text) // 10): #Получаем случайные позиции для вставки доп. символов (10% от исходного кол-ва символов)
            poses.append(random.randint(0, len_enc + 1))
            len_enc += 1
        poses.sort() #Сортируем полученные позиции по возрастанию
        for i in poses:
            text = text[:i] + chr(random.randint(0, 55291)) + text[i:] #Вставляем на позиции случайные символы

    # Контрольная сумма
    if use_csum:
        random.seed(text)
        csum = hex(random.randint(0, 4294967296))[2:]
        while len(csum)<8:
            csum = '0' + csum
        text += csum

    return text


def decryption(text: str, password: str, is_add_symbols: bool, is_use_csum: bool):
    '''Расшифровывает полученный текст.
    Возвращает расшифрованный текст.
    Выполняет алгоритм шифрования в зеркальном виде.

    text - исходный текст
    password - пароль
    is_add_symbols - были ли добавлены символы в шифротекст'''

    # Проверка контрольной суммы
    if is_use_csum:
        if len(text)<8:
            return False
        ref_csum = text[-8:]
        text = text[:-8]
        random.seed(text)
        csum = hex(random.randint(0, 4294967296))[2:]
        while len(csum)<8:
            csum = '0' + csum
        if ref_csum != csum:
            msb.showwarning('ОШИБКА!', 'Данные повреждены!')
            return False

    #Если в шифротекст были добавлены символы
    if is_add_symbols:
        random.seed(password[::-1]) #Задаёт сид для генератора псевдослучайных
        len_on_enc = len(text) - len(text) // 11 #Получает длину шифротекста без доп. символов
        poses = []
        for i in range(len(text) // 11): #Получает позиции доп. символов (10% от кол-ва символов в исходном шифротексте)
            poses.append(random.randint(0, len_on_enc + 1))
            len_on_enc += 1
        poses.sort(reverse=True) #Сортирует позиции по убыванию
        for i in poses:
            text = text[:i] + text[i+1:] #Вырезает символы на позициях (добавленные)

    #Задаёт сид для генератора псевдослучайных чисел
    random.seed(password + str(len(text)))

    # Перебирает все коды из исходного массива
    for i in range(len(text)):
        s = text[i]
        sc = ord(s)

        # Перезадаёт сид и генерирует случайное число
        random.seed( ''.join(random.sample(password, len(password)))+str(random.random()) )
        modification = random.randint(0, 55291)

        if random.choice([True, False]):
            if sc - modification < 0: #Если при вычитании опустились ниже 0, отнимаем лишнее от 55291
                text = text[:i] + chr(sc - modification + 55292) + text[i+1:] #Меняет символ на новый
            else:
                text = text[:i] + chr(sc - modification) + text[i+1:]

        else:
            if sc + modification > 55291: #Если при сложении превысили 55291, прибавляем лишнее к 0
                text = text[:i] + chr(sc + modification - 55292) + text[i+1:]
            else:
                text = text[:i] + chr(sc + modification) + text[i+1:]

    return text
