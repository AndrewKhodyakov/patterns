#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
"""
    Объект_комманда_для_выполнения_дейсвий
    и рагирования на случай ексепшонов
"""
#===============================================================================
def fake():
    """
    Фейовая функция для выполенения валицаии входных данных
    """
    pass

class Command:
    """
    Реализация паттерна проектирвоания команда
    """
    def __init__(self, exceptions_actions):
        """
        При создании связывает список эксепшенов со списком действий на них
        exceptions_action - словарь ексепшин - действие - условия выполения команды
        """
        self.__validation(exceptions_actions)

        if 'default' in exceptions_actions.keys():
            self.__default_action = exceptions_actions['default']
            del exceptions_actions['default']
        else:
            self.__default_action = fake


        if exceptions_actions:
            self.__except_action = exceptions_actions
        else:
            self.__except_action = None 

    def __validation(self, exceptions_actions):
        """
        Проверка данных на валидацию
        """
        if ('all_special' in exceptions_actions.keys()) &\
            (len(exceptions_actions) > 2):
            raise TypeError('all_special используется только с default')

        for excpt in exceptions_actions:
            if not (
                (type(exceptions_actions[excpt]) == type(self.__validation)) |\
                (type(exceptions_actions[excpt]) == type(fake))
            ):
                raise TypeError(
                'Дествие {0} должно быть либо методом либо функцией'.format(excpt)
                )

    def execute(self, command, command_param=None, result=False):
        """
        Выполнение комманды и отправка сообщения в логгер
        command : объект-метод, для выполнения
        command_param :параметры команнды
        result : признак того что выполняемаый метод что то должен вернуть
        Выполняет комманду и удаляет сам себя 
        """
        if not (
            (type(command) == type(self.__validation)) |\
            (type(command) == type(fake))
        ):
            raise TypeError('command должнa быть либо методом либо функцией')       

        self.__command = command
        self.__command_param = command_param
        self.__result = result

        return self.__select_except_actions()

        #TODO здесь придлеть метод проверки что command - это метод 


    def __select_except_actions(self):
        """
        Выбор наличия действий в случае возникновения ексепшенов
        """
        if self.__except_action:
            try:
                return self.__select_param()
            except tuple(self.__except_action.keys()) as excpt:
#                self.__except_action[excpt.__class__](excpt)
#TODO проверь как будет работать без передачи экземпляра класса эксепшена
                self.__select_action(excpt)
        else:
            return self.__select_param()
            

    def __select_param(self):
        """
        Выбор наличия параметров
        """
        if self.__command_param:
            return self.__command(**self.__command_param)
        else:
            return self.__command()
        

    def __select_action(self, excpt):
        """
        Выбор действия в зависимости от типа ексепшена
        excpt: экземпляр исключения
        """
        excpt_mro = excpt.__class__.__mro__
        excpt_class = excpt.__class__
        if 'all_special' in self.__except_action.keys():
            action = self.__except_action.get(
                'all_special',
                self.__default_action
            )
            action()
        else:
            action = self.__except_action.get(
                excpt.__class__,
                self.__default_action
            )
            action()
            
#===============================================================================
if __name__=="__main__":
    class My_exception(Exception):pass

    def test_comm(**kwargs):
        """
        Тестовая комманда
        """
        if 'raise' in kwargs.keys():
            raise My_exception('Ошибка') 
        elif 'param' in kwargs.keys():
            print('Do command with param...')
        else:
            print('Do command with out param...')
            return 1234

    def excpt_action():
        """
        Действие при ошибке
        """
        print('Do emergancy action...')

    def default_action():
        print('Default action....')

    context = {My_exception:excpt_action, 'default':default_action}
    Com = Command(context)    
    Com.execute(test_comm)
    res = Com.execute(
        test_comm,
        {'param':12344},
        result=True                
    )
    Com.execute(test_comm, {'raise':None})


    context = {My_exception:excpt_action}
    Com = Command(context)    
    Com.execute(test_comm)
    res = Com.execute(
        test_comm,
        {'param':12344},
        result=True                
    )
    Com.execute(test_comm, {'raise':None})

