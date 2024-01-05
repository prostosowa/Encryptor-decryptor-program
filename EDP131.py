'''Приложение для шифрования и дешифровки текста и текстовых файлов (.txt)
Применяется для защиты личных данных от несанкционированного прочтения'''

import tkinter as tk #Библиотека для создания графического интерфейса
from tkinter import scrolledtext as scrt #Для создания текстовых полей с прокруткой
from tkinter import filedialog as fd #Для создания диалогового окна сохранения и выбора файла
from tkinter import messagebox as msb #Предупреждающие окна
import os #Библиотека для работы с файлами
import random #Библиотека для генерации случайных чисел (основы метода шифрования)
from threading import Thread #Для создания параллельного потока (корректной работы LIVE)

from EDFunc import encryption, decryption



class Button(tk.Button):
    '''Для удобства создания кнопок. Хранит параметры кнопок и метода .grid по умолчанию.'''

    def __init__(self, master=None,
                 text='', font=('Times_new_roman', 12, 'bold'),
                 foreground='black', backgroung='white',
                 activefereground='black', activebackground='green',
                 relief=tk.RAISED, borderwidth=5,
                 width=1, height=1,
                 command=None, **kwargs):
        tk.Button.__init__(self, master=master,
                           text=text, font=font,
                           foreground=foreground, background=backgroung,
                           activeforeground=activefereground, activebackground=activebackground,
                           relief=relief, borderwidth=borderwidth,
                           width=width, height=height,
                           command=command, **kwargs)

    def GRID(self, row=0, column=0, sticky='nsew', columnspan=1, rowspan=1):
        self.grid(row=row, column=column, sticky=sticky, columnspan=columnspan, rowspan=rowspan)

class Label(tk.Label):
    '''Для удобства создания ярлыков. Хранит параметры ярлыков и метода .grid по умолчанию'''

    def __init__(self, master=None,
                 text='', font=('Times_new_roman', 12, 'bold'),
                 foreground='black',
                 width=1, height=1):
        tk.Label.__init__(self, master=master,
                          text=text, font=font,
                          foreground=foreground,
                          width=width, height=height)

    def GRID(self, row=0, column=0, columnspan=1, rowspan=1, sticky='nsew'):
        self.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky)



def root_create():
    '''Создаёт и настраивает главное окно.'''

    global root
    root = tk.Tk()

    root.title('Encryptor-Decryptor') #Заголовок окна
    root.geometry(f'600x450+{root.winfo_screenwidth() // 2 - 300}+{root.winfo_screenheight() // 2 - 225}') #Размеры окна при открытии
    root.minsize(width=600, height=450) #Минимальный размер окна
    root.maxsize(width=root.winfo_screenwidth(), height=root.winfo_screenheight()) #Максимальный размер окна (на весь экран)
    root.resizable(width=True, height=True) #Возможность изменять размер окна


def main_page_create():
    '''Создаёт и настраивает главное меню.'''

    global frm_main_page
    frm_main_page = tk.Frame(master=root)

    frm_main_page.columnconfigure(0, weight=1)
    frm_main_page.columnconfigure(1, weight=1)
    frm_main_page.columnconfigure(2, weight=1)
    frm_main_page.rowconfigure(0, weight=1)
    frm_main_page.rowconfigure(1, weight=1)
    frm_main_page.rowconfigure(2, weight=0)

    #Создаём кнопки главного меню
    btn_enc_text = Button(master=frm_main_page,
                          text='Зашифровать\nтекст',
                          command=enc_text_page_show)
    btn_enc_text.GRID(row=0, column=0)

    btn_enc_files = Button(master=frm_main_page,
                           text='Зашифровать\nфайл(ы)',
                           command=enc_files_page_show)
    btn_enc_files.GRID(row=0, column=1)

    btn_enc_live = Button(master=frm_main_page,
                          text='LIVE\nшифрование',
                          command=enc_live_page_show)
    btn_enc_live.GRID(row=0, column=2)

    btn_dec_text = Button(master=frm_main_page,
                          text='Расшифровать\nтекст',
                          command=dec_text_page_show)
    btn_dec_text.GRID(row=1, column=0, sticky='nsew')

    btn_dec_files = Button(master=frm_main_page,
                           text='Расшифровать\nфайл(ы)',
                           command=dec_files_page_show)
    btn_dec_files.GRID(row=1, column=1)

    btn_dec_live = Button(master=frm_main_page,
                          text='LIVE\nрасшифровка',
                          command=dec_live_page_show)
    btn_dec_live.GRID(row=1, column=2)

    btn_password_generate = Button(master=frm_main_page,
                                   text='Генератор паролей',
                                   command=password_generate_page_show)
    btn_password_generate.GRID(row=2, column=0, columnspan=3)


def passwod_generate_page_create():
    '''Создаёт и настраивает страницу генератора паролей'''

    global frm_password_generate_page
    frm_password_generate_page = tk.Frame(master=root, borderwidth=5)

    frm_password_generate_page.rowconfigure(0, weight=1)
    frm_password_generate_page.rowconfigure(1, weight=1)
    frm_password_generate_page.rowconfigure(2, weight=1)
    frm_password_generate_page.rowconfigure(3, weight=1)
    frm_password_generate_page.rowconfigure(4, weight=1)
    frm_password_generate_page.rowconfigure(5, weight=0)
    frm_password_generate_page.rowconfigure(6, weight=1)
    frm_password_generate_page.columnconfigure(0, weight=1)
    frm_password_generate_page.columnconfigure(1, weight=1)
    frm_password_generate_page.columnconfigure(2, weight=1)
    frm_password_generate_page.columnconfigure(3, weight=1)

    #"Укажите длину пароля"
    lbl_len_password = Label(master=frm_password_generate_page,
                             text='Укажите длину пароля:')
    lbl_len_password.GRID(row=0, column=0, columnspan=4)

    #Шкала для выбора длины пароля
    val_len_password = tk.IntVar()
    scl_len_password = tk.Scale(master=frm_password_generate_page, orient='horizontal',
                                from_=1, to=1000, resolution=1, tickinterval=999, variable=val_len_password)
    scl_len_password.grid(row=1, column=0, columnspan=4, sticky='nsew')

    def generate_password(len_password: int):
        '''Генерирует пароль заданной длины.

        len_password - длина пароля'''
        entry_password.delete(0, tk.END)
        pswrd = ''
        for i in range(len_password):
            random.seed()
            pswrd += chr(random.randint(0, 55291))
        entry_password.insert(0, pswrd)

    #Кнопка "Сгенерировать пароль"
    btn_generate_password = Button(master=frm_password_generate_page,
                                   text='Сгенерировать пароль',
                                   command=lambda: generate_password(len_password=val_len_password.get()))
    btn_generate_password.GRID(row=2, column=0, columnspan=4)

    #"Ваш пароль:"
    lbl_password = Label(master=frm_password_generate_page,
                         text='Ваш пароль:')
    lbl_password.GRID(row=3, column=0, columnspan=2)

    #Флажок "Показать/скрыть пароль"
    if_show_password = tk.BooleanVar()
    chk_show_password = tk.Checkbutton(master=frm_password_generate_page,
                                       variable=if_show_password, offvalue=False, onvalue=True,
                                       font=('Times_new_roman', 12, 'bold'), borderwidth=5,
                                       command=lambda: show_hide_password(if_show_password=if_show_password.get(), ins=entry_password),
                                       text='Показать')
    chk_show_password.grid(row=3, column=2, columnspan=2, sticky='nsew')


    #Поле для вывода сгенерированного пароля
    entry_password = tk.Entry(master=frm_password_generate_page, borderwidth=5, font=100,
                              show='*')
    entry_password.grid(row=4, column=0, columnspan=4, sticky='nsew')

    #Полоса прокрутки для поля вывода
    scrollbar = tk.Scrollbar(master=frm_password_generate_page, orient='horizontal', command=entry_password.xview)
    scrollbar.grid(row=5, column=0, columnspan=4, sticky='nsew')
    entry_password['xscrollcommand'] = scrollbar.set #Настраиваем поле вывода под полосу прокрутки

    #Кнопка "Сохранить пароль"
    btn_save_password = Button(master=frm_password_generate_page,
                               activebackground='white', text='Сохранить',
                               command=lambda: save_text(text=entry_password.get(), is_password=True))
    btn_save_password.GRID(row=6, column=2, columnspan=2)

    # Кнопка выхода в главное меню
    btn_back = Button(master=frm_password_generate_page,
                      text='Назад',
                      activebackground='white',
                      command=lambda: main_page_show(ins=False))
    btn_back.GRID(row=6, column=0, columnspan=2)


def enc_text_page_create():
    '''Создаёт и настраивает страницу шифрования текста.'''

    global frm_enc_text_page
    frm_enc_text_page = tk.Frame(master=root, borderwidth=5)

    frm_enc_text_page.columnconfigure(0, weight=1)
    frm_enc_text_page.columnconfigure(1, weight=2)
    frm_enc_text_page.columnconfigure(2, weight=2)
    frm_enc_text_page.columnconfigure(3, weight=1)
    frm_enc_text_page.rowconfigure(0, weight=0)
    frm_enc_text_page.rowconfigure(1, weight=2)
    frm_enc_text_page.rowconfigure(2, weight=0)
    frm_enc_text_page.rowconfigure(3, weight=0)
    frm_enc_text_page.rowconfigure(4, weight=0)
    frm_enc_text_page.rowconfigure(5, weight=0)
    frm_enc_text_page.rowconfigure(6, weight=0)
    frm_enc_text_page.rowconfigure(7, weight=0)
    frm_enc_text_page.rowconfigure(8, weight=2)
    frm_enc_text_page.rowconfigure(9, weight=0)

    #"Введите текст"
    lbl_enc_text = Label(master=frm_enc_text_page, text='Введите шифруемый текст:')
    lbl_enc_text.GRID(row=0, column=0, columnspan=4)

    #Поле ввода текста
    txt_entr_text = scrt.ScrolledText(master=frm_enc_text_page, borderwidth=5)
    txt_entr_text.grid(column=0, row=1, columnspan=4, sticky='nsew')

    #Кнопка отчистки поля ввода текста
    btn_clear_entry = Button(master=frm_enc_text_page,
                             text='Очистить',
                             foreground='red', activebackground='white',
                             command=lambda: txt_entr_text.delete(0.0, tk.END))
    btn_clear_entry.GRID(column=0, row=2)

    # Флажок "Показать/скрыть пароль"
    if_show_password = tk.BooleanVar()
    chk_show_password = tk.Checkbutton(master=frm_enc_text_page,
                                       variable=if_show_password, offvalue=False, onvalue=True,
                                       font=('Times_new_roman', 12, 'bold'), borderwidth=5,
                                       command=lambda: show_hide_password(if_show_password=if_show_password.get(),
                                                                     ins=entry_password),
                                       text='Показать пароль')
    chk_show_password.grid(row=2, column=2, columnspan=2, sticky='nsew')

    #"Введите пароль"
    lbl_entry_password = Label(master=frm_enc_text_page,
                               text='Пароль:')
    lbl_entry_password.GRID(column=0, row=3)

    #Поле ввода пароля
    entry_password = tk.Entry(master=frm_enc_text_page, borderwidth=5, show='*')
    entry_password.grid(column=1, row=3, columnspan=2, sticky='nsew')

    #Кнопка выбора файла с паролем
    btn_choose_password = Button(master=frm_enc_text_page,
                                 text='Выбрать', activebackground='white',
                                 command=lambda: choose_password(ins=entry_password))
    btn_choose_password.GRID(column=3, row=3)

    # Полоса прокрутки для поля вывода
    scrollbar = tk.Scrollbar(master=frm_enc_text_page, orient='horizontal', command=entry_password.xview)
    scrollbar.grid(row=4, column=1, columnspan=2, sticky='nsew')
    entry_password['xscrollcommand'] = scrollbar.set  # Настраиваем поле вывода под полосу прокрутки

    # Флажок "Добавить символы в шифротекст"
    add_symbols = tk.BooleanVar()
    chk_add_symbols = tk.Checkbutton(master=frm_enc_text_page,
                                     text='Добавить символы', font=('Times_new_roman', 12, 'bold'),
                                     borderwidth=5,
                                     variable=add_symbols, offvalue=False, onvalue=True)
    chk_add_symbols.grid(row=5, column=0, columnspan=2, sticky='nsew')

    # Контрольная сумма
    use_csum = tk.BooleanVar()
    chk_use_csum = tk.Checkbutton(master=frm_enc_text_page,
                                     text='Контрольная сумма', font=('Times_new_roman', 12, 'bold'),
                                     borderwidth=5,
                                     variable=use_csum, offvalue=False, onvalue=True)
    chk_use_csum.grid(row=5, column=2, columnspan=2, sticky='nsew')

    #Кнопка шифровки
    btn_enc = Button(master=frm_enc_text_page,
                     text='Зашифровать',
                     command=lambda: enc_text(
                         text=txt_entr_text.get(0.0, tk.END)[:len(txt_entr_text.get(0.0, tk.END)) - 1],
                         password=entry_password.get(), ins=txt_enced_text, add_symbols=add_symbols.get(), use_csum=use_csum.get()))
    btn_enc.GRID(column=0, row=6, columnspan=4)

    #"Здесь будет выведен зашифрованный текст"
    lbl_enced_text = Label(master=frm_enc_text_page, text='Зашифрованный текст:')
    lbl_enced_text.GRID(row=7, column=0, columnspan=4)

    #Поле вывода зашифрованного текста
    txt_enced_text = scrt.ScrolledText(master=frm_enc_text_page, state='disabled', borderwidth=5)
    txt_enced_text.grid(column=0, row=8, columnspan=4, sticky='nsew')

    def clear_enced():
        '''Функция очищает поле вывода шифротекста'''
        txt_enced_text['state'] = 'normal'
        txt_enced_text.delete(0.0, tk.END)
        txt_enced_text['state'] = 'disabled'

    # Кнопка отчистки поля вывода
    btn_clear_enced = Button(master=frm_enc_text_page,
                             text='Очистить',
                             foreground='red', activebackground='white',
                             command=clear_enced)
    btn_clear_enced.GRID(column=0, row=9)

    #Кнопка "Сохранить шифротекст в виде текстового файла"
    btn_save_enced_text = Button(master=frm_enc_text_page,
                                 text='Сохранить', foreground='green',
                                 activebackground='white',
                                 command=lambda: save_text(
                                     text=txt_enced_text.get(0.0, tk.END)[:len(txt_enced_text.get(0.0, tk.END)) - 1]))
    btn_save_enced_text.GRID(row=9, column=3)

    #Кнопка выхода в главное меню
    btn_back = Button(master=frm_enc_text_page,
                      text='Назад',
                      activebackground='white',
                      command=lambda: main_page_show(ins=False))
    btn_back.GRID(row=9, column=1, columnspan=2)

def enc_files_page_create():
    '''Создаёт и настраивает страницу шифрования файлов.'''

    global frm_enc_files_page
    frm_enc_files_page = tk.Frame(master=root)

    frm_enc_files_page.rowconfigure(0, weight=0)
    frm_enc_files_page.rowconfigure(1, weight=1)
    frm_enc_files_page.rowconfigure(2, weight=0)
    frm_enc_files_page.rowconfigure(3, weight=0)
    frm_enc_files_page.rowconfigure(4, weight=1)
    frm_enc_files_page.rowconfigure(5, weight=0)
    frm_enc_files_page.rowconfigure(6, weight=0)
    frm_enc_files_page.rowconfigure(7, weight=0)
    frm_enc_files_page.rowconfigure(8, weight=0)
    frm_enc_files_page.columnconfigure(0, weight=1)
    frm_enc_files_page.columnconfigure(1, weight=1)
    frm_enc_files_page.columnconfigure(2, weight=1)
    frm_enc_files_page.columnconfigure(3, weight=1)

    # "Введите пути к файлам"
    lbl_entry_path = Label(master=frm_enc_files_page,
                           text='Введите пути к файлам:')
    lbl_entry_path.GRID(row=0, column=0, columnspan=4)

    # Поле ввода пути
    entry_path_e = tk.Entry(master=frm_enc_files_page, borderwidth=5, font=100)
    entry_path_e.grid(row=1, column=0, columnspan=3, sticky='nsew')

    # Кнопка "Выбрать файлы"
    btn_choose_files = Button(master=frm_enc_files_page, activebackground='white',
                              text='Выбрать', command=lambda: choose_files(ins=entry_path_e))
    btn_choose_files.GRID(row=1, column=3)

    # Полоса прокрутки для поля ввода пути
    scrollbar_path = tk.Scrollbar(master=frm_enc_files_page, orient='horizontal', command=entry_path_e.xview)
    scrollbar_path.grid(row=2, column=0, columnspan=3, sticky='nsew')
    entry_path_e['xscrollcommand'] = scrollbar_path.set  # Настраиваем поле ввода под полосу прокрутки

    # "Введите пароль"
    lbl_entry_password = Label(master=frm_enc_files_page,
                               text='Введите пароль:')
    lbl_entry_password.GRID(row=3, column=0, columnspan=2)

    # Флажок "Показать/скрыть пароль"
    if_show_password = tk.BooleanVar()
    chk_if_show_password = tk.Checkbutton(master=frm_enc_files_page,
                                          variable=if_show_password, offvalue=False, onvalue=True,
                                          font=('Times_new_roman', 12, 'bold'), borderwidth=5,
                                          command=lambda: show_hide_password(if_show_password=if_show_password.get(),
                                                                             ins=entry_password),
                                          text='Показать')
    chk_if_show_password.grid(row=3, column=2, columnspan=2, sticky='nsew')

    # Поле ввода пароля
    entry_password = tk.Entry(master=frm_enc_files_page, borderwidth=5, font=100, show='*')
    entry_password.grid(row=4, column=0, columnspan=3, sticky='nsew')

    # Кнопка выбора файла с паролем
    btn_choose_password = Button(master=frm_enc_files_page,
                                 text='Выбрать', activebackground='white',
                                 command=lambda: choose_password(ins=entry_password))
    btn_choose_password.GRID(column=3, row=4)

    # Полоса прокрутки для поля ввода пароля
    scrollbar_password = tk.Scrollbar(master=frm_enc_files_page, orient='horizontal', command=entry_password.xview)
    scrollbar_password.grid(row=5, column=0, columnspan=3, sticky='nsew')
    entry_password['xscrollcommand'] = scrollbar_password.set  # Настраиваем поле ввода под полосу прокрутки

    # Флажок "Добавить в шифротекст символы"
    add_symbols = tk.BooleanVar()
    chk_add_symbols = tk.Checkbutton(master=frm_enc_files_page,
                                        text='Добавить символы', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=add_symbols, offvalue=False, onvalue=True)
    chk_add_symbols.grid(row=6, column=0, columnspan=2, sticky='nsew')

    # Контрольная сумма
    use_csum = tk.BooleanVar()
    chk_use_csum = tk.Checkbutton(master=frm_enc_files_page,
                                        text='Контрольная сумма', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=use_csum, offvalue=False, onvalue=True)
    chk_use_csum.grid(row=6, column=2, columnspan=2, sticky='nsew')

    # Кнопка "Зашифровать"
    btn_start_enc = Button(master=frm_enc_files_page,
                           text='Зашифровать',
                           command=lambda: enc_files(
                               pathes=[path for path in entry_path_e.get().split('; ')], password=entry_password.get(),
                               ins=entry_path_e, add_symbols=add_symbols.get(), use_csum=use_csum.get()))
    btn_start_enc.GRID(row=7, column=0, columnspan=4)

    # Кнопка выхода в главное меню
    btn_back = Button(master=frm_enc_files_page,
                      text='Назад',
                      activebackground='white',
                      command=lambda: main_page_show(ins=entry_path_e))
    btn_back.GRID(row=8, column=0, columnspan=4)

def enc_live_page_create():
    '''Создаёт и настраивает страницу live-шифрования.'''

    global frm_enc_live_page
    frm_enc_live_page = tk.Frame(master=root)

    frm_enc_live_page.rowconfigure(0, weight=0)
    frm_enc_live_page.rowconfigure(1, weight=1)
    frm_enc_live_page.rowconfigure(2, weight=0)
    frm_enc_live_page.rowconfigure(3, weight=0)
    frm_enc_live_page.rowconfigure(4, weight=1)
    frm_enc_live_page.rowconfigure(5, weight=0)
    frm_enc_live_page.rowconfigure(6, weight=0)
    frm_enc_live_page.rowconfigure(7, weight=0)
    frm_enc_live_page.rowconfigure(8, weight=0)
    frm_enc_live_page.columnconfigure(0, weight=1)
    frm_enc_live_page.columnconfigure(1, weight=1)
    frm_enc_live_page.columnconfigure(2, weight=1)
    frm_enc_live_page.columnconfigure(3, weight=1)

    # "Введите путь к директории"
    lbl_entry_path = Label(master=frm_enc_live_page,
                           text='Введите путь к директории:')
    lbl_entry_path.GRID(row=0, column=0, columnspan=4)

    # Поле ввода пути
    entry_path_e_l = tk.Entry(master=frm_enc_live_page, borderwidth=5, font=100)
    entry_path_e_l.grid(row=1, column=0, columnspan=3, sticky='nsew')

    # Кнопка "Выбрать директорию"
    btn_choose_dir = Button(master=frm_enc_live_page, activebackground='white',
                            text='Выбрать', command=lambda: choose_dir(ins=entry_path_e_l))
    btn_choose_dir.GRID(row=1, column=3)

    # Полоса прокрутки для поля ввода пути
    scrollbar_path = tk.Scrollbar(master=frm_enc_live_page, orient='horizontal', command=entry_path_e_l.xview)
    scrollbar_path.grid(row=2, column=0, columnspan=3, sticky='nsew')
    entry_path_e_l['xscrollcommand'] = scrollbar_path.set  # Настраиваем поле ввода под полосу прокрутки

    # "Введите пароль"
    lbl_entry_password = Label(master=frm_enc_live_page,
                               text='Введите пароль:')
    lbl_entry_password.GRID(row=3, column=0, columnspan=2)

    # Флажок "Показать/скрыть пароль"
    show_password = tk.BooleanVar()
    chk_show_password = tk.Checkbutton(master=frm_enc_live_page,
                                       variable=show_password, offvalue=False, onvalue=True,
                                       font=('Times_new_roman', 12, 'bold'), borderwidth=5,
                                       command=lambda: show_hide_password(if_show_password=show_password.get(),
                                                                     ins=entry_password),
                                       text='Показать')
    chk_show_password.grid(row=3, column=2, columnspan=2, sticky='nsew')

    # Поле ввода пароля
    entry_password = tk.Entry(master=frm_enc_live_page, borderwidth=5, font=100, show='*')
    entry_password.grid(row=4, column=0, columnspan=3, sticky='nsew')

    # Кнопка выбора файла с паролем
    btn_choose_password = Button(master=frm_enc_live_page,
                                 text='Выбрать', activebackground='white',
                                 command=lambda: choose_password(ins=entry_password))
    btn_choose_password.GRID(column=3, row=4)

    # Полоса прокрутки для поля ввода пароля
    scrollbar_password = tk.Scrollbar(master=frm_enc_live_page, orient='horizontal', command=entry_password.xview)
    scrollbar_password.grid(row=5, column=0, columnspan=3, sticky='nsew')
    entry_password['xscrollcommand'] = scrollbar_password.set  # Настраиваем поле ввода под полосу прокрутки

    # Флажок "Добавить символы в шифротекст"
    add_symbols = tk.BooleanVar()
    chk_add_symbols = tk.Checkbutton(master=frm_enc_live_page,
                                        text='Добавить символы', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=add_symbols, offvalue=False, onvalue=True)
    chk_add_symbols.grid(row=6, column=0, columnspan=2, sticky='nsew')

    # Контрольная сумма
    use_csum = tk.BooleanVar()
    chk_use_csum = tk.Checkbutton(master=frm_enc_live_page,
                                     text='Контрольная сумма', font=('Times_new_roman', 12, 'bold'),
                                     borderwidth=5,
                                     variable=use_csum, offvalue=False, onvalue=True)
    chk_use_csum.grid(row=6, column=2, columnspan=2, sticky='nsew')

    # Кнопка "Начать LIVE-шифрование"
    btn_start_enc = Button(master=frm_enc_live_page,
                           text='Начать шифрование',
                           command=lambda: enc_live(
                               path=entry_path_e_l.get(), password=entry_password.get(),
                               add_symbols=add_symbols.get(),
                               STOP=False, use_csum=use_csum.get(),
                               ins1=entry_path_e_l, ins2=entry_password, ins3=chk_add_symbols, ins4=btn_start_enc,
                               ins5=btn_back, ins6=btn_stop_enc, ins7=btn_choose_dir, ins8=btn_choose_password))
    btn_start_enc.GRID(row=7, column=0, columnspan=2)

    # Кнопка "Остановить LIVE-шифрование"
    btn_stop_enc = Button(master=frm_enc_live_page,
                          text='Стоп', foreground='Red', activebackground='Red', state='disabled',
                          command=lambda: enc_live(
                              path='', password='', add_symbols=False,
                              STOP=True, use_csum=False,
                              ins1=entry_path_e_l, ins2=entry_password, ins3=chk_add_symbols, ins4=btn_start_enc,
                              ins5=btn_back, ins6=btn_stop_enc, ins7=btn_choose_dir, ins8=btn_choose_password))
    btn_stop_enc.GRID(row=7, column=2, columnspan=2)

    # Кнопка выхода в главное меню
    btn_back = Button(master=frm_enc_live_page,
                      text='Назад',
                      activebackground='white',
                      command=lambda: main_page_show(ins=entry_path_e_l))
    btn_back.GRID(row=8, column=0, columnspan=4)


def dec_text_page_create():
    '''Создаёт и настраивает страницу дешифровки текста.'''

    global frm_dec_text_page
    frm_dec_text_page = tk.Frame(master=root, borderwidth=5)

    frm_dec_text_page.columnconfigure(0, weight=1)
    frm_dec_text_page.columnconfigure(1, weight=2)
    frm_dec_text_page.columnconfigure(2, weight=2)
    frm_dec_text_page.columnconfigure(3, weight=1)
    frm_dec_text_page.rowconfigure(0, weight=0)
    frm_dec_text_page.rowconfigure(1, weight=2)
    frm_dec_text_page.rowconfigure(2, weight=0)
    frm_dec_text_page.rowconfigure(3, weight=0)
    frm_dec_text_page.rowconfigure(4, weight=0)
    frm_dec_text_page.rowconfigure(5, weight=0)
    frm_dec_text_page.rowconfigure(6, weight=0)
    frm_dec_text_page.rowconfigure(7, weight=0)
    frm_dec_text_page.rowconfigure(8, weight=2)
    frm_dec_text_page.rowconfigure(9, weight=0)

    # "Введите текст"
    lbl_dec_text = Label(master=frm_dec_text_page, text='Введите текст для расшифровки:')
    lbl_dec_text.GRID(row=0, column=0, columnspan=4)

    # Поле ввода текста
    txt_entr_text = scrt.ScrolledText(master=frm_dec_text_page, borderwidth=5)
    txt_entr_text.grid(column=0, row=1, columnspan=4, sticky='nsew')

    # Кнопка отчистки поля ввода текста
    btn_clear_entry = Button(master=frm_dec_text_page,
                             text='Очистить',
                             foreground='red', activebackground='white',
                             command=lambda: txt_entr_text.delete(0.0, tk.END))
    btn_clear_entry.GRID(column=0, row=2)

    # Флажок "Показать/скрыть пароль"
    if_show_password = tk.BooleanVar()
    chk_if_show_password = tk.Checkbutton(master=frm_dec_text_page,
                                       variable=if_show_password, offvalue=False, onvalue=True,
                                       font=('Times_new_roman', 12, 'bold'), borderwidth=5,
                                       command=lambda: show_hide_password(if_show_password=if_show_password.get(),
                                                                     ins=entry_password),
                                       text='Показать пароль')
    chk_if_show_password.grid(row=2, column=2, columnspan=2, sticky='nsew')

    # "Введите пароль"
    lbl_entry_password = Label(master=frm_dec_text_page,
                               text='Пароль:')
    lbl_entry_password.GRID(column=0, row=3)

    # Поле ввода пароля
    entry_password = tk.Entry(master=frm_dec_text_page, borderwidth=5, show='*')
    entry_password.grid(column=1, row=3, columnspan=2, sticky='nsew')

    # Кнопка выбора файла с паролем
    btn_choose_password = Button(master=frm_dec_text_page,
                                 text='Выбрать', activebackground='white',
                                 command=lambda: choose_password(ins=entry_password))
    btn_choose_password.GRID(column=3, row=3)

    # Полоса прокрутки для поля вывода
    scrollbar = tk.Scrollbar(master=frm_dec_text_page, orient='horizontal', command=entry_password.xview)
    scrollbar.grid(row=4, column=1, columnspan=2, sticky='nsew')
    entry_password['xscrollcommand'] = scrollbar.set  # Настраиваем поле вывода под полосу прокрутки

    # Флажок "В шифротекст были добавлены символы"
    is_add_symbols = tk.BooleanVar()
    chk_if_add_symbols = tk.Checkbutton(master=frm_dec_text_page,
                                     text='Добавлены символы', font=('Times_new_roman', 12, 'bold'),
                                     borderwidth=5,
                                     variable=is_add_symbols, offvalue=False, onvalue=True)
    chk_if_add_symbols.grid(row=5, column=0, columnspan=2, sticky='nsew')

    is_use_csum = tk.BooleanVar()
    chk_if_use_csum = tk.Checkbutton(master=frm_dec_text_page,
                                        text='Контрольная сумма', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=is_use_csum, offvalue=False, onvalue=True)
    chk_if_use_csum.grid(row=5, column=2, columnspan=2, sticky='nsew')

    # Кнопка дешифровки
    btn_dec = Button(master=frm_dec_text_page,
                     text='Расшифровать',
                     command=lambda: dec_text(
                         text=txt_entr_text.get(0.0, tk.END)[:len(txt_entr_text.get(0.0, tk.END)) - 1],
                         password=entry_password.get(), ins=txt_deced_text, is_add_symbols=is_add_symbols.get(), is_use_csum=is_use_csum.get()))
    btn_dec.GRID(column=0, row=6, columnspan=4)

    # "Здесь будет выведен расшифрованный текст"
    lbl_deced_text = Label(master=frm_dec_text_page, text='Расшифрованный текст:')
    lbl_deced_text.GRID(row=7, column=0, columnspan=4)

    # Поле вывода расшифрованного текста
    txt_deced_text = scrt.ScrolledText(master=frm_dec_text_page, state='disabled', borderwidth=5)
    txt_deced_text.grid(column=0, row=8, columnspan=4, sticky='nsew')

    def clear_deced():
        '''Функция очищает поле вывода расшифрованного текста'''
        txt_deced_text['state'] = 'normal'
        txt_deced_text.delete(0.0, tk.END)
        txt_deced_text['state'] = 'disabled'

    # Кнопка отчистки поля вывода
    btn_clear_deced = Button(master=frm_dec_text_page,
                             text='Очистить',
                             foreground='red', activebackground='white',
                             command=clear_deced)
    btn_clear_deced.GRID(column=0, row=9)

    # Кнопка "Сохранить расшифрованный текст в виде текстового файла"
    btn_save_deced_text = Button(master=frm_dec_text_page,
                                 text='Сохранить', foreground='green',
                                 activebackground='white',
                                 command=lambda: save_text(
                                     text=txt_deced_text.get(0.0, tk.END)[:len(txt_deced_text.get(0.0, tk.END)) - 1]))
    btn_save_deced_text.GRID(row=9, column=3)

    # Кнопка выхода в главное меню
    btn_back = Button(master=frm_dec_text_page,
                      text='Назад',
                      activebackground='white',
                      command=lambda: main_page_show(ins=False))
    btn_back.GRID(row=9, column=1, columnspan=2)

def dec_files_page_create():
    '''Создаёт и настраивает страницу дешифровки файлов.'''

    global frm_dec_files_page
    frm_dec_files_page = tk.Frame(master=root)

    frm_dec_files_page.rowconfigure(0, weight=0)
    frm_dec_files_page.rowconfigure(1, weight=1)
    frm_dec_files_page.rowconfigure(2, weight=0)
    frm_dec_files_page.rowconfigure(3, weight=0)
    frm_dec_files_page.rowconfigure(4, weight=1)
    frm_dec_files_page.rowconfigure(5, weight=0)
    frm_dec_files_page.rowconfigure(6, weight=0)
    frm_dec_files_page.rowconfigure(7, weight=0)
    frm_dec_files_page.rowconfigure(8, weight=0)
    frm_dec_files_page.columnconfigure(0, weight=1)
    frm_dec_files_page.columnconfigure(1, weight=1)
    frm_dec_files_page.columnconfigure(2, weight=1)
    frm_dec_files_page.columnconfigure(3, weight=1)

    # "Введите пути к файлам"
    lbl_entry_path = Label(master=frm_dec_files_page,
                           text='Введите пути к файлам:')
    lbl_entry_path.GRID(row=0, column=0, columnspan=4)

    # Поле ввода пути
    entry_path_d = tk.Entry(master=frm_dec_files_page, borderwidth=5, font=100)
    entry_path_d.grid(row=1, column=0, columnspan=3, sticky='nsew')

    # Кнопка "Выбрать файлы"
    btn_choose_files = Button(master=frm_dec_files_page, activebackground='white',
                            text='Выбрать', command=lambda: choose_files(ins=entry_path_d))
    btn_choose_files.GRID(row=1, column=3)

    # Полоса прокрутки для поля ввода пути
    scrollbar_path = tk.Scrollbar(master=frm_dec_files_page, orient='horizontal', command=entry_path_d.xview)
    scrollbar_path.grid(row=2, column=0, columnspan=3, sticky='nsew')
    entry_path_d['xscrollcommand'] = scrollbar_path.set  # Настраиваем поле ввода под полосу прокрутки

    # "Введите пароль"
    lbl_entry_password = Label(master=frm_dec_files_page,
                               text='Введите пароль:')
    lbl_entry_password.GRID(row=3, column=0, columnspan=2)

    # Флажок "Показать/скрыть пароль"
    if_show_password = tk.BooleanVar()
    chk_if_show_password = tk.Checkbutton(master=frm_dec_files_page,
                                          variable=if_show_password, offvalue=False, onvalue=True,
                                          font=('Times_new_roman', 12, 'bold'), borderwidth=5,
                                          command=lambda: show_hide_password(if_show_password=if_show_password.get(),
                                                                             ins=entry_password),
                                          text='Показать')
    chk_if_show_password.grid(row=3, column=2, columnspan=2, sticky='nsew')

    # Поле ввода пароля
    entry_password = tk.Entry(master=frm_dec_files_page, borderwidth=5, font=100, show='*')
    entry_password.grid(row=4, column=0, columnspan=3, sticky='nsew')

    # Кнопка выбора файла с паролем
    btn_choose_password = Button(master=frm_dec_files_page,
                                 text='Выбрать', activebackground='white',
                                 command=lambda: choose_password(ins=entry_password))
    btn_choose_password.GRID(column=3, row=4)

    # Полоса прокрутки для поля ввода пароля
    scrollbar_password = tk.Scrollbar(master=frm_dec_files_page, orient='horizontal', command=entry_password.xview)
    scrollbar_password.grid(row=5, column=0, columnspan=3, sticky='nsew')
    entry_password['xscrollcommand'] = scrollbar_password.set  # Настраиваем поле ввода под полосу прокрутки

    # Флажок "В шифротекст были добавлены символы"
    is_add_symbols = tk.BooleanVar()
    chk_is_add_symbols = tk.Checkbutton(master=frm_dec_files_page,
                                        text='Добавлены символы', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=is_add_symbols, offvalue=False, onvalue=True)
    chk_is_add_symbols.grid(row=6, column=0, columnspan=2, sticky='nsew')

    # Контрольная сумма
    is_use_csum = tk.BooleanVar()
    chk_is_use_csum = tk.Checkbutton(master=frm_dec_files_page,
                                        text='Контрольная сумма', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=is_use_csum, offvalue=False, onvalue=True)
    chk_is_use_csum.grid(row=6, column=2, columnspan=2, sticky='nsew')

    # Кнопка "Расшифровать"
    btn_start_dec = Button(master=frm_dec_files_page,
                           text='Расшифровать',
                           command=lambda: dec_files(
                               pathes=[path for path in entry_path_d.get().split('; ')], password=entry_password.get(),
                           ins=entry_path_d, is_add_symbols=is_add_symbols.get(), is_use_csum=is_use_csum.get()))
    btn_start_dec.GRID(row=7, column=0, columnspan=4)

    # Кнопка выхода в главное меню
    btn_back = Button(master=frm_dec_files_page,
                      text='Назад',
                      activebackground='white',
                      command=lambda: main_page_show(ins=entry_path_d))
    btn_back.GRID(row=8, column=0, columnspan=4)

def dec_live_page_create():
    '''Создаёт и настраивает страницу live-дешифровки.'''

    global frm_dec_live_page
    frm_dec_live_page = tk.Frame(master=root)

    frm_dec_live_page.rowconfigure(0, weight=0)
    frm_dec_live_page.rowconfigure(1, weight=1)
    frm_dec_live_page.rowconfigure(2, weight=0)
    frm_dec_live_page.rowconfigure(3, weight=0)
    frm_dec_live_page.rowconfigure(4, weight=1)
    frm_dec_live_page.rowconfigure(5, weight=0)
    frm_dec_live_page.rowconfigure(6, weight=0)
    frm_dec_live_page.rowconfigure(7, weight=0)
    frm_dec_live_page.rowconfigure(8, weight=0)
    frm_dec_live_page.columnconfigure(0, weight=1)
    frm_dec_live_page.columnconfigure(1, weight=1)
    frm_dec_live_page.columnconfigure(2, weight=1)
    frm_dec_live_page.columnconfigure(3, weight=1)

    #"Введите путь к директории"
    lbl_entry_path = Label(master=frm_dec_live_page,
                           text='Введите путь к директории:')
    lbl_entry_path.GRID(row=0, column=0, columnspan=4)

    #Поле ввода пути
    entry_path_d_l = tk.Entry(master=frm_dec_live_page, borderwidth=5, font=100)
    entry_path_d_l.grid(row=1, column=0, columnspan=3, sticky='nsew')

    #Кнопка "Выбрать директорию"
    btn_choose_dir = Button(master=frm_dec_live_page, activebackground='white',
                            text='Выбрать', command=lambda: choose_dir(ins=entry_path_d_l))
    btn_choose_dir.GRID(row=1, column=3)

    # Полоса прокрутки для поля ввода пути
    scrollbar_path = tk.Scrollbar(master=frm_dec_live_page, orient='horizontal', command=entry_path_d_l.xview)
    scrollbar_path.grid(row=2, column=0, columnspan=3, sticky='nsew')
    entry_path_d_l['xscrollcommand'] = scrollbar_path.set  # Настраиваем поле ввода под полосу прокрутки

    #"Введите пароль"
    lbl_entry_password = Label(master=frm_dec_live_page,
                               text='Введите пароль:')
    lbl_entry_password.GRID(row=3, column=0, columnspan=2)

    # Флажок "Показать/скрыть пароль"
    if_show_password = tk.BooleanVar()
    chk_if_show_password = tk.Checkbutton(master=frm_dec_live_page,
                                       variable=if_show_password, offvalue=False, onvalue=True,
                                       font=('Times_new_roman', 12, 'bold'), borderwidth=5,
                                       command=lambda: show_hide_password(if_show_password=if_show_password.get(),
                                                                     ins=entry_password),
                                       text='Показать')
    chk_if_show_password.grid(row=3, column=2, columnspan=2, sticky='nsew')

    # Поле ввода пароля
    entry_password = tk.Entry(master=frm_dec_live_page, borderwidth=5, font=100, show='*')
    entry_password.grid(row=4, column=0, columnspan=3, sticky='nsew')

    # Кнопка выбора файла с паролем
    btn_choose_password = Button(master=frm_dec_live_page,
                                 text='Выбрать', activebackground='white',
                                 command=lambda: choose_password(ins=entry_password))
    btn_choose_password.GRID(column=3, row=4)

    # Полоса прокрутки для поля ввода пароля
    scrollbar_password = tk.Scrollbar(master=frm_dec_live_page, orient='horizontal', command=entry_password.xview)
    scrollbar_password.grid(row=5, column=0, columnspan=3, sticky='nsew')
    entry_password['xscrollcommand'] = scrollbar_password.set  # Настраиваем поле ввода под полосу прокрутки

    #Флажок "В шифротекст были добавлены символы"
    is_add_symbols = tk.BooleanVar()
    chk_is_add_symbols = tk.Checkbutton(master=frm_dec_live_page,
                                        text='Добавлены символы', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=is_add_symbols, offvalue=False, onvalue=True)
    chk_is_add_symbols.grid(row=6, column=0, columnspan=2, sticky='nsew')

    # Контрольная сумма
    is_use_csum = tk.BooleanVar()
    chk_if_use_csum = tk.Checkbutton(master=frm_dec_live_page,
                                        text='Контрольная сумма', font=('Times_new_roman', 12, 'bold'),
                                        borderwidth=5,
                                        variable=is_use_csum, offvalue=False, onvalue=True)
    chk_if_use_csum.grid(row=6, column=2, columnspan=2, sticky='nsew')

    #Кнопка "Начать LIVE-расшифровку"
    btn_start_dec = Button(master=frm_dec_live_page,
                           text='Начать дешифрование',
                           command=lambda: dec_live(
                               path=entry_path_d_l.get(), password=entry_password.get(),
                               is_add_symbols=is_add_symbols.get(), is_use_csum=is_use_csum.get(),
                               STOP=False,
                               ins1=entry_path_d_l, ins2=entry_password, ins3=chk_is_add_symbols, ins4=btn_start_dec,
                               ins5=btn_back, ins6=btn_stop_dec, ins7=btn_choose_dir, ins8=btn_choose_password, ins9=chk_if_use_csum))
    btn_start_dec.GRID(row=7, column=0, columnspan=2)

    #Кнопка "Остановить LIVE-расшифровку"
    btn_stop_dec = Button(master=frm_dec_live_page,
                          text='Стоп', foreground='Red', activebackground='Red', state='disabled',
                          command=lambda: dec_live(
                              path='', password='', is_add_symbols=False, is_use_csum=False,
                              STOP=True,
                              ins1=entry_path_d_l, ins2=entry_password, ins3=chk_is_add_symbols, ins4=btn_start_dec,
                              ins5=btn_back, ins6=btn_stop_dec, ins7=btn_choose_dir, ins8=btn_choose_password, ins9=chk_if_use_csum))
    btn_stop_dec.GRID(row=7, column=2, columnspan=2)

    #Кнопка выхода в главное меню
    btn_back = Button(master=frm_dec_live_page,
                      text='Назад',
                      activebackground='white',
                      command=lambda: main_page_show(ins=entry_path_d_l))
    btn_back.GRID(row=8, column=0, columnspan=4)



def main_page_show(ins):
    '''Выводит на экран главное меню'''

    if ins != False:
        ins['background'] = 'white'

    frm_enc_text_page.pack_forget()
    frm_enc_files_page.pack_forget()
    frm_enc_live_page.pack_forget()
    frm_dec_text_page.pack_forget()
    frm_dec_files_page.pack_forget()
    frm_dec_live_page.pack_forget()
    frm_password_generate_page.forget()

    frm_main_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)


def password_generate_page_show():
    '''Выводит на экран страницу генератора паролей'''

    frm_main_page.pack_forget()
    frm_password_generate_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)


def enc_text_page_show():
    '''Выводит на экран страницу шифрования текста.'''

    frm_main_page.pack_forget()
    frm_enc_text_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)

def enc_files_page_show():
    '''Выводит на экран страницу шифрования файлов.'''

    frm_main_page.pack_forget()
    frm_enc_files_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)

def enc_live_page_show():
    '''Выводит на экран страницу live-шифрования текста.'''

    frm_main_page.pack_forget()
    frm_enc_live_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)


def dec_text_page_show():
    '''Выводит на экран страницу расшифровки текста.'''

    frm_main_page.pack_forget()
    frm_dec_text_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)

def dec_files_page_show():
    '''Выводит на экран страницу расшифровки файлов.'''

    frm_main_page.pack_forget()
    frm_dec_files_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)

def dec_live_page_show():
    '''Выводит на экран страницу live-расшифровки.'''

    frm_main_page.pack_forget()
    frm_dec_live_page.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)



def enc_text(text: str, password: str, add_symbols: bool, use_csum: bool, ins):
    '''Получает текст для шифрования, отправляет его шифроваться и выводит результат в поле вывода.

    text - текст для шифрования
    password - пароль шифрования
    add_symbols - добавить ли символы в шифротекст
    ins - поле для вывода шифротекста'''

    txt_enced_text = ins
    txt_enced_text['state'] = 'normal'
    txt_enced_text.insert(0.0, chars=encryption(text=text, password=password, add_symbols=add_symbols, use_csum=use_csum))
    txt_enced_text['state'] = 'disabled'

def enc_files(pathes: list, password: str, add_symbols: bool, use_csum: bool, ins):
    '''Получает список из путей к файлам.
    Вызывает функции получения текста, шифрования и сохранения для файлов. В конце подсвечивает поле ввода пути зелёным.
    Если путь некорректен, подсвечивает окно ввода пути красным.
    Если корректна часть путей, подсвечивает окно ввода пути оранжевым.

    path - путь
    password - пароль
    add_symbols - добавить ли символы в шифротекст
    ins - поле ввода пути'''

    entry_path_e = ins

    if '' in pathes:
        pathes.remove('')

    invalid_path_count = 0
    for path in pathes:
        if os.path.isfile(path):
            if get_text(path) != False:
                save_encrypted_text(
                    encrypted_text=encryption(text=get_text(path), password=password, add_symbols=add_symbols, use_csum=use_csum),
                    path=path)
        else:
            invalid_path_count += 1

    if (invalid_path_count == 0) and (len(pathes) > 0):
        entry_path_e['background'] = 'green'
    elif (invalid_path_count < len(pathes)) and (invalid_path_count > 0):
        print(invalid_path_count, len(pathes))
        entry_path_e['background'] = 'orange'
    elif (invalid_path_count == len(pathes)) or (len(pathes) == 0):
        entry_path_e['background'] = 'red'

def enc_l(path: str, password: str, add_symbols: bool, use_csum: bool):
    '''Вызывается как параллельный поток при нажатии на кнопку "Начать LIVE-шифрование".
    Бесконечно перебирает файлы в директории.
    Если файл не был зашифрован, вызывает для него функции получения текста, шифрования, сохранения.
    Останавливается при нажатии на кнопку "Остановить LIVE-шифрование".

    path - путь к директории
    password - пароль
    add_symbols - добавить ли символы в шифротекст'''

    while True:
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)) and not ' _E_.' in file_name and get_text(
                    os.path.join(path, file_name)) != False:
                save_encrypted_text(
                    encrypted_text=encryption(text=get_text(os.path.join(path, file_name)), password=password,
                                              add_symbols=add_symbols, use_csum=use_csum),
                    path=os.path.join(path, file_name))

            global STOP_ENC_L
            if STOP_ENC_L:
                del STOP_ENC_L
                return

def enc_live(path: str, password: str, add_symbols: bool, use_csum: bool, STOP: bool, ins1, ins2, ins3, ins4, ins5, ins6, ins7, ins8):
    '''Вызывается при нажатии на кнопку "Начать LIVE-шифрование" или "Остановить LIVE-шифрование".
    Если "старт", то проверяет, введён ли корректный путь к директории.
    Если путь корректен, то запускает параллельный поток LIVE-шифрования и блокирует все элементы, кроме кнопки "Стоп".
    Если путь некорректен, подсвечивает поле ввода пути красным.
    Если "стоп", то останавливает параллельный поток и разблокирует элементы управления.

    path - путь
    password - пароль
    add_symbols - добавить ли символы в шифротекст
    STOP - остановить ли LIVE-шифрование
    ins1, ins2 - поля ввода пути и пароля
    ins3 - флажок
    ins4-ins6 - кнопки "старт", "назад", "стоп"
    ins7, ins8 - кнопки выбора директории и пароля'''

    entry_path_e_l = ins1
    entry_password = ins2
    chk_add_symbols = ins3
    btn_start_enc = ins4
    btn_back = ins5
    btn_stop_enc = ins6
    btn_choose_dir = ins7
    btn_choose_password = ins8

    global STOP_ENC_L
    STOP_ENC_L = STOP

    if not STOP:
        if os.path.isdir(path):
            entry_path_e_l['background'] = 'White'
            entry_path_e_l['state'] = 'disabled'
            entry_password['state'] = 'disabled'
            chk_add_symbols['state'] = 'disabled'
            btn_start_enc['state'] = 'disabled'
            btn_back['state'] = 'disabled'
            btn_stop_enc['state'] = 'normal'
            btn_choose_dir['state'] = 'disabled'
            btn_choose_password['state'] = 'disabled'

            enc_thread = Thread(target=enc_l, args=(path, password, add_symbols, use_csum,), daemon=True)
            enc_thread.start()

        else:
            entry_path_e_l['background'] = 'Red'
    else:
        entry_path_e_l['background'] = 'White'
        entry_path_e_l['state'] = 'normal'
        entry_password['state'] = 'normal'
        chk_add_symbols['state'] = 'normal'
        btn_start_enc['state'] = 'normal'
        btn_back['state'] = 'normal'
        btn_back['state'] = 'normal'
        btn_stop_enc['state'] = 'disabled'
        btn_choose_dir['state'] = 'normal'
        btn_choose_password['state'] = 'normal'


def dec_text(text: str, password: str, ins, is_add_symbols: bool, is_use_csum: bool):
    '''Получает текст для расшифровки, отправляет его расшифровываться и выводит результат в поле вывода.

        text - текст для расшифровки
        password - пароль
        is_add_symbols - были ли добавлены символы в шифротекст
        ins - поле для вывода расшифрованного текста'''

    txt_deced_text = ins
    txt_deced_text['state'] = 'normal'
    deced_text = decryption(text=text, password=password, is_add_symbols=is_add_symbols, is_use_csum=is_use_csum)
    if deced_text != False:
        txt_deced_text.insert(0.0, chars=deced_text)
    txt_deced_text['state'] = 'disabled'

def dec_files(pathes: list, password: str, is_add_symbols: bool, is_use_csum: bool, ins):
    '''Получает список из путей к файлам.
    Вызывает функции получения текста, шифрования и сохранения для файлов. В конце подсвечивает поле ввода пути зелёным.
    Если путь некорректен, подсвечивает окно ввода пути красным.
    Если корректна часть путей, подсвечивает окно ввода пути оранжевым.

        path - путь
        password - пароль
        is_add_symbols - были ли добавлены символы в шифротекст
        ins - поле ввода пути'''

    entry_path_d =ins

    if '' in pathes:
        pathes.remove('')

    invalid_path_count = 0
    for path in pathes:
        if os.path.isfile(path):
            if get_text(path) != False:
                save_decrypted_text(
                    decrypted_text=decryption(text=get_text(path), password=password, is_add_symbols=is_add_symbols, is_use_csum=is_use_csum),
                    path=path)
        else:
            invalid_path_count += 1

    if (invalid_path_count == 0) and (len(pathes) > 0):
        entry_path_d['background'] = 'green'
    elif (invalid_path_count < len(pathes)) and (invalid_path_count > 0):
        entry_path_d['background'] = 'orange'
    elif (invalid_path_count == len(pathes)) or (len(pathes) == 0):
        entry_path_d['background'] = 'red'

def dec_l(path: str, password: str, is_add_symbols: bool, is_use_csum: bool):
    '''Вызывается как параллельный поток при нажатии на кнопку "Начать LIVE-расшифровку".
        Бесконечно перебирает файлы в директории.
        Если файл не был расшифрован, вызывает для него функции получения текста, дешифрования, сохранения.
        Останавливается при нажатии на кнопку "Остановить LIVE-дешифрование".

        path - путь к директории
        password - пароль
        add_symbols - были ли добавлены символы в шифротекст'''

    while True:
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)) and not ' _D_.' in file_name and get_text(
                    os.path.join(path, file_name)) != False:
                deced_text = decryption(text=get_text(os.path.join(path, file_name)), password=password,
                                              is_add_symbols=is_add_symbols, is_use_csum=is_use_csum)
                if deced_text == False:
                    return
                save_decrypted_text(decrypted_text=deced_text, path=os.path.join(path, file_name))

            global STOP_DEC_L
            if STOP_DEC_L:
                del STOP_DEC_L
                return

def dec_live(path: str, password: str, is_add_symbols: bool, is_use_csum: bool, STOP: bool, ins1, ins2, ins3, ins4, ins5, ins6, ins7, ins8, ins9):
    '''Вызывается при нажатии на кнопку "Начать LIVE-дешифрование" или "Остановить LIVE-дешифрование".
        Если "старт", то проверяет, введён ли корректный путь к директории.
        Если путь корректен, то запускает параллельный поток LIVE-дешифрования и блокирует все элементы, кроме кнопки "Стоп".
        Если путь некорректен, подсвечивает поле ввода пути красным.
        Если "стоп", то останавливает параллельный поток и разблокирует элементы управления.

        path - путь
        password - пароль
        add_symbols - были ли добавлены символы в шифротекст
        STOP - остановить ли LIVE-дешифрование
        ins1, ins2 - поля ввода пути и пароля
        ins3 - флажок
        ins4-ins6 - кнопки "старт", "назад", "стоп"
        ins7, ins8 - кнопки выбора директории и пароля'''

    entry_path_d_l = ins1
    entry_password = ins2
    chk_is_add_symbols = ins3
    btn_start_dec = ins4
    btn_back = ins5
    btn_stop_dec = ins6
    btn_choose_dir = ins7
    btn_choose_password = ins8
    chk_is_use_csum = ins9

    global STOP_DEC_L
    STOP_DEC_L = STOP

    if not STOP:
        if os.path.isdir(path):
            entry_path_d_l['background'] = 'White'
            entry_path_d_l['state'] = 'disabled'
            entry_password['state'] = 'disabled'
            chk_is_add_symbols['state'] = 'disabled'
            btn_start_dec['state'] = 'disabled'
            btn_back['state'] = 'disabled'
            btn_stop_dec['state'] = 'normal'
            btn_choose_dir['state'] = 'disabled'
            btn_choose_password['state'] = 'disabled'
            chk_is_use_csum['state'] = 'disabled'

            dec_thread = Thread(target=dec_l, args=(path, password, is_add_symbols, is_use_csum,), daemon=True)
            dec_thread.start()

        else:
            entry_path_d_l['background'] = 'Red'
    else:
        entry_path_d_l['background'] = 'White'
        entry_path_d_l['state'] = 'normal'
        entry_password['state'] = 'normal'
        chk_is_add_symbols['state'] = 'normal'
        btn_start_dec['state'] = 'normal'
        btn_back['state'] = 'normal'
        btn_stop_dec['state'] = 'disabled'
        btn_choose_dir['state'] = 'normal'
        btn_choose_password['state'] = 'normal'
        chk_is_use_csum['state'] = 'normal'



def save_text(text: str, is_password=False):
    '''Для сохранения текста, в том числе паролей.
    Вызывает диалоговое окно для сохранения текста в виде текстового документа. Сохраняет текст.
    Если передан is_password=True (сохраняется пароль), то показывает окно с предупреждением о хранении пароля.

    text - зашифрованный либо расшифрованный текст
    is_password - является ли текст паролем (по умолчанию - нет)'''

    path = fd.asksaveasfilename(filetypes=[('TXT файлы', '.txt'), ('RTF файлы', '.rtf'), ('HTML файлы', ('.html', '.htm')),
                                           ('CSV файлы', '.csv'), ('XML файлы', '.xml')], defaultextension='.txt')
    if path != '':
        try:
            file = open(path, 'w', encoding='utf-8')
        except Exception:
            pass
        else:
            try:
                file.write(text)
            except Exception:
                pass
            file.close()

            if is_password:
                msb.showwarning('ВНИМАНИЕ', 'Храните пароль в надёжном месте!\n'
                                            'Храните пароль отдельно от файлов!\n'
                                            'Убедитесь, что случайно не зашифруете пароль!\n'
                                            'Утраченный пароль восстановить не получится!')

def save_encrypted_text(encrypted_text: str, path: str):
    '''Для сохранения зашифрованного текста из файла.
    Создаёт файл с именем исходного файла и добавляет к нему маркировку " _E_", сохраняет в него шифротекст.

    encrypted_text - шифротекст
    path - путь к исходному файлу'''

    try:
        new_file = open(os.path.splitext(path)[0] + ' _E_' + os.path.splitext(path)[1], 'w', encoding='utf-8')
    except FileExistsError:
        pass
    else:
        try:
            new_file.write(encrypted_text)
        except Exception:
            pass
        else:
            os.remove(path)
        new_file.close()

def save_decrypted_text(decrypted_text: str, path: str):
    '''Для сохранения расшифрованного текста из файла.
    Создаёт файл с именем исходного файла и добавляет к нему маркировку " _D_", сохраняет в него расшифрованный текст..

    decrypted_text - расшифрованный текст
    path - путь к исходному файлу'''

    if decrypted_text == False:
        return

    try:
        new_file = open(os.path.splitext(path)[0] + ' _D_' + os.path.splitext(path)[1], 'w', encoding='utf-8')
    except FileExistsError:
        pass
    else:
        try:
            new_file.write(decrypted_text)
        except Exception:
            pass
        else:
            os.remove(path)
        new_file.close()


def get_text(path: str):
    '''Получает текст из файла.
    Возвращает этот текст.
    Если текст получить не удаётся, возвращает False

    path - путь к файлу'''

    try:
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception:
        return False
    else:
        return text


"""
def encryption(text: str, password: str, add_symbols: bool, use_csum: bool):
    '''Шифрует полученный текст.
    Возвращает шифротекст.

    text - исходный текст
    password - пароль
    add_symbols - добавить ли символы в шифротекст'''


    #Получает массив кодов (utf-8) символов из исходного текста
    symbol_codes = [ord(symbol) for symbol in text]
    del text

    #Задаёт сид для генератора псевдослучайных чисел
    random.seed(password + str(len(symbol_codes)))

    #Шифрование за счёт изменения кодов исходных символов
    enc_symbol_codes = [] #Массив изменённых кодов
    lsc = len(symbol_codes)
    for i in range(lsc): #Перебирает каждый код из исходного массива

        # Перезадаёт сид и генерирует случайное число
        a = random.randint(0, len(password))
        b = random.randint(0, len(password))
        random.seed( password[min(a,b) : max(a,b)] + str(random.random()))
        del a
        del b
        modification = random.randint(0, 55291)

        if random.choice([True, False]):
            if symbol_codes[0] + modification > 55291: #Если при сложении превысили 55291, прибавляем лишнее к 0
                enc_symbol_codes.append(symbol_codes[0] + modification - 55292)
                symbol_codes.remove(symbol_codes[0])
            else:
                enc_symbol_codes.append(symbol_codes[0] + modification)
                symbol_codes.remove(symbol_codes[0])

        else:
            if symbol_codes[0] - modification < 0: #Если при вычитании опустились ниже 0, отнимаем лишнее от 55291
                enc_symbol_codes.append(symbol_codes[0] - modification + 55292)
                symbol_codes.remove(symbol_codes[0])
            else:
                enc_symbol_codes.append(symbol_codes[0] - modification)
                symbol_codes.remove(symbol_codes[0])

    #Получаем шифротекст из массива изменённых кодов
    enc_text = ''.join([chr(code) for code in enc_symbol_codes])
    del enc_symbol_codes

    #Если нужно добавить символы в шифротекст (повышает стойкость)
    if add_symbols:
        random.seed(password[::-1]) #Задаёт сид для генератора псевдослучайных чисел
        len_enc = len(enc_text) #Получаем длину шифротекста (будут добавлены 10% символов от исходного кол-ва)
        poses = []
        for i in range(len(enc_text) // 10): #Получаем случайные позиции для вставки доп. символов (10% от исходного кол-ва символов)
            poses.append(random.randint(0, len_enc + 1))
            len_enc += 1
        poses.sort() #Сортируем полученные позиции по возрастанию
        for i in poses:
            enc_text = enc_text[:i] + chr(random.randint(0, 55291)) + enc_text[i:] #Вставляем на позиции случайные символы

    # Контрольная сумма
    if use_csum:
        random.seed(enc_text)
        csum = hex(random.randint(0, 4294967296))[2:]
        while len(csum)<8:
            csum = '0' + csum
        enc_text = enc_text + csum

    return enc_text


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

    # Получает массив кодов (utf-8) символов из шифротекста
    symbol_codes = [ord(symbol) for symbol in text]
    del text

    #Задаёт сид для генератора псевдослучайных чисел
    random.seed(password + str(len(symbol_codes)))

    #Дешифровка за счёт изменения кодов символов шифротекста
    dec_symbol_codes = [] #Массив изменённых кодов
    lsc = len(symbol_codes)
    for i in  range(lsc): #Перебирает все коды из исходного массива

        # Перезадаёт сид и генерирует случайное число
        a = random.randint(0, len(password))
        b = random.randint(0, len(password))
        random.seed(password[min(a, b): max(a, b)] + str(random.random()))
        del a
        del b
        modification = random.randint(0, 55291)

        if random.choice([True, False]):
            if symbol_codes[0] - modification < 0: #Если при вычитании опустились ниже 0, отнимаем лишнее от 55291
                dec_symbol_codes.append(symbol_codes[0] - modification + 55292)
                symbol_codes.remove(symbol_codes[0])
            else:
                dec_symbol_codes.append(symbol_codes[0] - modification)
                symbol_codes.remove(symbol_codes[0])

        else:
            if symbol_codes[0] + modification > 55291: #Если при сложении превысили 55291, прибавляем лишнее к 0
                dec_symbol_codes.append(symbol_codes[0] + modification - 55292)
                symbol_codes.remove(symbol_codes[0])
            else:
                dec_symbol_codes.append(symbol_codes[0] + modification)
                symbol_codes.remove(symbol_codes[0])

    #Получает расшифрованный текст из массива изменённых кодов
    dec_text = ''.join([chr(code) for code in dec_symbol_codes])

    return dec_text
"""


def show_hide_password(if_show_password: bool, ins):
    '''Показывает или скрывает пароль в поле ввода.

    if_show_password - нужно ли показывать пароль
    ins - поле ввода пароля'''

    entry_password = ins

    if if_show_password:
        entry_password['show'] = ''
    else:
        entry_password['show'] = '*'


def choose_password(ins):
    '''Вызывает диалоговое окно для выбора файла с паролем. Вводит пароль из выбранного файла.
    Если пароль уже введён, он будет удалён.

    ins - поле для ввода пароля'''

    entry_password = ins

    password_file = fd.askopenfilename(title='Выбрать файл с паролем',
                                       defaultextension='.txt', filetypes=[('TXT файлы', '.txt'), ('RTF файлы', '.rtf'),
                                                                           ('HTML файлы', ('.html', '.htm')), ('CSV файлы', '.csv'), ('XML файлы', '.xml')])

    password = get_text(password_file)

    if password != False:
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)

def choose_dir(ins):
    entry_path = ins

    directory = fd.askdirectory(title='Выбрать директорию')

    if directory != None:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, directory)

def choose_files(ins):
    entry_path = ins

    files = fd.askopenfilenames(title='Выбрать файл(ы)', defaultextension='.txt',
                                filetypes=[('TXT файлы', '.txt'), ('RTF файлы', '.rtf'),
                                           ('HTML файлы', ('.html', '.htm')), ('CSV файлы', '.csv'), ('XML файлы', '.xml')])

    if files != '':
        entry_path.delete(0, tk.END)
        insert_files = ''.join([f'{file}; ' for file in files])
        entry_path.insert(0, insert_files)
        entry_path['background'] = 'white'



def main():
    root_create()
    main_page_create()
    enc_text_page_create()
    enc_files_page_create()
    enc_live_page_create()
    dec_text_page_create()
    dec_files_page_create()
    dec_live_page_create()
    passwod_generate_page_create()

    main_page_show(ins=False)

    root.mainloop()

if __name__ == '__main__':
    main()

