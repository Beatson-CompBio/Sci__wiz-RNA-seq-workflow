#!/usr/bin/env python
"""
Created on 2024-01-24 15:36:39
Module desc: command interface that each command will implement.
@author: m.sikarwar
"""
from abc import ABCMeta, abstractmethod


class ICommand(metaclass=ABCMeta):
    """
    command interface that each command will implement.
    """

    @staticmethod
    @abstractmethod
    def execute():
        """
        execute the command.
        """
        pass
