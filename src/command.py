#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
"""
    Объект комманда для последовательного выполненя действий
    и рагирования на случай ексепшонов:
        - получвет на вход контекст выполнения:
            actions - словарь действий: {'№':вызваемая_функция(метод)}
"""
import heapq
#===============================================================================
class Command(object):
    """
    Одна из реализаций паттерна проектирвоания команда
    """
    def __init__(self):
        """
        При создании связывает список эксепшенов со списком действий на них
        exceptions_action - словарь ексепшин 
                          - действие - условия выполения команды
        """
        self.__actions = None
        self.__actions_quae = None

        self.__params = None
        self.__params_quae = None

        self.__exceptions = None 


    @property
    def set_actions(self, actions):
        """
        Загрузка actions в комманду
        actions: список задач для выполнения
        """
        if isinstance(actions, dict):
            for k in actions:
                if not (isinstance(k, int) & isinstance(action[k], self.execute)):
                    msg = 'Action dict key should be a int, '
                    msg = msg + 'action dict value should be a function!'

            self.__actions = actions
            self.__actions_quae = heapq.heapify([i for i in self.__actions])

        else:
            raise TypeError('Actions is not dict!')


    @property
    def set_exceptions(exception_context):
        """
        Загрузка exception_context в комманду
        exception_context: список задач для выполнения
        """
        if isinstance(exceptions, dict):
            for k in exception_context:
                if not (\
                    isinstance(k, type) & isinstance(exception_context[k],
                        self.execute)\
                ):
                    msg = 'Exception dict key should be a class,'
                    msg = msg + 'exception dict value should be a function!'
                    raise TypeError(msg)

            self.__exceptions = exception_context

        else:
            raise TypeError('Exceptions is not dict!')

    @property
    def set_params(self, params):
        """
        Установка параметров для каждого выполняемого action
        """
        if isinstance(params, dict):
            for k in params:
                if not isinstance(k, int):
                    raise TypeError('Key in params dict should be int!')

            self.__params = params
            self.__params_quae = heapq.heapify([i for i in self.__params])

        else:
            raise TypeError('Params is not dict!')


    def __align_action_and_params(self):
        """
        Выставялем кажому action его параметры выполнения
        """
        pass


    def execute(self):
        """
        Выполнени комманды 
        """
        pass


    def execute(self, command, command_param=None, result=False):
        """
        Выполнение комманды и отправка сообщения в логгер
        command : объект-метод, для выполнения
        command_param :параметры команнды
        result : признак того что выполняемаый метод что то должен вернуть
        Выполняет комманду и удаляет сам себя 
        """
        #TODO здесь придлеть метод проверки что command - это метод 

        self.__command = command
        self.__command_param = command_param
        self.__result = result

        return self.__select_except_actions()


    def __select_except_actions(self):
        """
        Выбор наличия действий в случае возникновения ексепшенов
        """
        if self.__exceptions:
            try:
                return self.__select_param()
            except tuple(self.__exceptions.keys()) as excpt:
                self.__exceptions[excpt.__class__](excpt)

        else:
            return self.__select_param()
            

    def __select_param(self):
        """
        Выбор наличия параметров
        """
        if self.__command_param:

            if isinstance(self.__command_param, dict):
                return self.__command(**self.__command_param)
            else:
                return self.__command(self.__command_param)

        else:
            return self.__command()


    def __repr__(self):
        """
        Вывод комманды в "сыром" виде.
        """
        exceptions = '\t - exceptions: {0}'.format(self.__exceptions)

        actions = '\t - actions: {0}'.format(self.__actions)

        param = '\t - parametrs: {0}'.format(self.__params)

        return 'Command content:\n{0}{1}{2}'.format(exceptions, actions, param)


    def __src__(self):
        """
        Вывод комманды в удобновм виде в печать.
        """
        pass
#===============================================================================
