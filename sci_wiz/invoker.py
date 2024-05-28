#!/usr/bin/env python
"""
Created on 2024-01-25 10:47:32
Module desc: Module to register command for sci wizard.
@author: m.sikarwar
"""


class CommandNotRecognised(Exception):
    pass


class Invoker:
    def __init__(self):
        self._commands = {}

    def register(self, command_name, command):
        self._commands[command_name] = command

    def execute(self, command_name):
        if command_name in self._commands.keys():
            self._commands[command_name].execute()
        else:
            raise CommandNotRecognised("Command not recognised")
