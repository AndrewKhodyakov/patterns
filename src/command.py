#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
"""
    Переписываю_комманду_на_чисто
        Комманда работает так - получает объект метод_функцию и выполняет ее
    в опредееленном контексте.
    контекст пердсатвляет собой словарь в котором ключ - это класс
    перехавтываемых исключений, а значение это действие которые необходимо
    выполниить при получении такого искоключения.

"""
import types
import contextlib
#===============================================================================
@contextlib.contextmanager
def context_execute(arg):
    """
    Функция реализцющая менеджер котекста
    """
    command = arg
    try:
        yield
    except command.context_keys as excpt:
        print(excpt.__class__)
        command.get_context(excpt.__class__)
    

class Command:
    """
    Паттерн комманда
    """
    def __init__(self, command_context, all_special=False):
        """
        command_context - контекст в котором выполняются действия
        словарь {"":"", ...,"default":} - здесь default - действие по 
        "умолчанию" - если оно не заданно то перехваченное исключение 
        "улетает дальше"

        all_special - признак перехвата всех исклдчений уноследванных от 
            переданного в command_context
        """
        self.__excpetion_mro = Exception().__class__.__mro__
        self.__context_validation(command_context, all_special)

        self.__all_special = all_special
        self.context = command_context

        self.__default_context = context.get('default', self.__not_set_default)
        if 'default' in context.keys():
            del self.context['default']
        self.context_keys = tuple([exc_type for exc_type in self.context.keys()])
        

    def __not_set_default(self, excpt):
        """
        Действие на случай, когда default контекст не задан,
        надо отправить исключние дальше
        """
        raise excpt()

    def __context_validation(self, context, all_special):
        """
        Валидация словаря контекста
        context: словарь контекста
        """
        self.__empty_dict_test(
            context,
            'Контекст command должден быть словарь не нулевой длины'
        )

        #TODO test
        if (all_special is True) & (len(context) > 1):
            raise TypeError(
                'Флаг all_special - можно использовать только с одинм\
исключением, для того что бы перехватить унаследованные от него исключения'
            )


        for inst in context:
            self.__key_validation(inst)
            self.__value_validation(context[inst])


    def __key_validation(self, obj):
        """
        Проверка занчения ключей в словаре контекста выполнения коммнад
        obj: - ключ значения словаря контекста
        """
        #TODO test
        if len(
            [exc_type for exc_type in obj.__class__.__mro__
                if (
                    (exc_type == self.__excpetion_mro[0]) &\
                        (not (exc_type == 'default'))
                )
            ]
        ):
            raise TypeError(
                'Аргумент должен наслдовать главный класс исключений'
            )
        
    
    def __value_validation(self, obj):
        """
        Проветка аргумента, на то что он является фунекцией или методом класса
        """
        #TODO test
        if not (
            isinstance(obj, types.FunctionType) |\
            isinstance(obj, types.MethodType)
        ):
                raise TypeError(
                    'Аргумент должен быть либо фуинкцией,\
 либо методом экземпляра класса'
                )

    def __empty_dict_test(self, obj, msg):
        """
        Проверка объекта на то что он не путстой словарь
        obj: объект для теста
        msg: сообщение
        """
        #TODO test

        if (len(obj) == 0) | (not isinstance(obj, dict)):
            raise TypeError(msg)

    def get_context(self, excpt=None):
        """
        Получение контекста в зависисомсти от того какой ексепшен перехвачен
            -- словарь всех унаследованных типов (all_special=True);
            -- словарь тех которые переданны
        """
        if self.__all_special:
            return self.context.get(
                self.context[self.context_keys[0]],
                self.__default_context
            )
        else:
            return self.context.get(excpt, self.__default_context)


    def execute(self, command, command_args=None):
        """
        Выполнение комманды в контексте набора исключений
        """
        self.__value_validation(command)
        command = command

        if command_args:
            #выполнение комманды с парамтерами
            self.__empty_dict_test(
                command_args,
                'Аргументы комманды - должны быть не пустым словарем'
            )
            #TODO БАГА ТУТ В ВЫЗОВЕ КОНТЕКТСНОГО МЕНЕДЖЕРА!!!!!!!!
            with context_execute(self) as out:
                out = command(**command_args)
        else:
            with context_execute(self) as out:
                out = command()
            #выполнение комманды без парамтеров
        return out

#===============================================================================

if __name__ == "__main__": 
    class My_exception(Exception):pass
    class E1(My_exception):pass
    class E2(My_exception):pass

    def test_comm(**kwargs):
        """
        Тестовая комманда
        """
        if 'raise' in kwargs.keys():
            raise E2('Ошибка') 
        elif 'param' in kwargs.keys():
            print('Do command with param...')
            return 1234
        else:
            print('Do command with out param...')
            return 1234

    def excpt_action():
        """
        Действие при ошибке
        """
        print('Do emergancy action...')


    context = {E2:excpt_action}
    Com = Command(context)    
    Com.execute(test_comm)
    res = Com.execute(
        test_comm,
        {'param':12344},
    )
    Com.execute(test_comm, {'raise':None})

    context = {My_exception:excpt_action}
    Com = Command(context, all_special=True)    
    Com.execute(test_comm, {'raise':None})

