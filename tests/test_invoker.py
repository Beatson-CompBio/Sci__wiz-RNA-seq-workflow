#!/usr/bin/env python
"""
Created on 2024-01-30 09:19:48
Module desc: Test module for invoker
@author: m.sikarwar
"""

from sci_wiz.invoker import Invoker, CommandNotRecognised
import pytest
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Command:
    def __init__(self, name):
        self.name = name

    def execute(self):
        logger.info(f"Executing {self.name}")


@pytest.fixture
def invoker():
    return Invoker()


@pytest.fixture
def command():
    return Command("test")


def test_register_command(invoker, command):
    invoker.register("test", command)
    assert "test" in invoker._commands


def test_execute_command(invoker, command, caplog):
    invoker.register("test", command)
    caplog.clear()
    with caplog.at_level(logging.INFO):
        invoker.execute("test")
    assert "Executing" in caplog.text


def test_execute_command_not_recognised(invoker, command, caplog):
    invoker.register("test", command)
    caplog.clear()
    with pytest.raises(CommandNotRecognised) as ex_info:
        invoker.execute("failing_command")
    assert "Command not recognised" in str(ex_info.value)