#!/usr/bin/env python
"""
Created on 2024-01-30 09:32:46
Module desc: Test module for rna seq app.
@author: m.sikarwar
"""
from typer.testing import CliRunner
from sci_wiz.rna_seq import app
import logging

runner = CliRunner()


def test_create_config(caplog):
    caplog.clear()
    with caplog.at_level(logging.INFO):
        result = runner.invoke(app, ["create-config"])
    assert result.exit_code == 0
    assert "user_input.ini" in caplog.text


def test_run_initial_qc(caplog):
    caplog.clear()
    with caplog.at_level(logging.INFO):
        runner.invoke(app, ["run-initial-qc"])
    assert "Nextflow" in caplog.text


def test_run_preprocessing(caplog):
    caplog.clear()
    with caplog.at_level(logging.INFO):
        runner.invoke(app, ["run-preprocessing"])
        print(caplog.text)
    # assert result.exit_code == 0
    assert "Nextflow" in caplog.text


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "sci-wiz:" in result.stdout


def test_check_nf_version():
    result = runner.invoke(app, ["check-nf-version"])
    assert result.exit_code == 0
