#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
"""
    Объект_комманда_для_выполнения_дейсвий
    и рагирования на случай ексепшонов
"""
#===============================================================================
class Command(object):
    """
    Реализация паттерна проектирвоания команда
    """
    def __init__(self, exceptions_actions=None):
        """
        При создании связывает список эксепшенов со списком действий на них
        exceptions_action - словарь ексепшин 
                          - действие - условия выполения команды
        """
        if exceptions_actions:
            self.__except_action = exceptions_actions
        else:
            self.__except_action = None 

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
        if self.__except_action:
            try:
                return self.__select_param()
            except tuple(self.__except_action.keys()) as excpt:
                self.__except_action[excpt.__class__](excpt)

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

#===============================================================================
