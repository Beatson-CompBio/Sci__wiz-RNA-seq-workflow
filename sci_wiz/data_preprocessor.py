#!/usr/bin/env python
"""
Created on 2024-01-23 19:37:39
Module desc: Data preprocessor that uses nextflow workflow to carry out
multiple data processing steps such as trimming, aligning, and count
generation.
@author: m.sikarwar
"""
from pathlib import Path
import json
import logging
from sci_wiz.interface_command import ICommand
from sci_wiz.profiles import vm, hpc


log = logging.getLogger(__name__)


class DataPreprocessor(ICommand):
    def __init__(self, inputJson: dict, engine: str, entryPoint: str = "", ):
        _sitePackages = Path(__file__).parent.parent.absolute()
        _nextflow = _sitePackages.joinpath("nextflow")
        _multiQc = _nextflow.joinpath("multiqc")
        _inputJson = inputJson
        _inputJson["multiqc"] = _multiQc.__str__()
        self._workflow = _nextflow.joinpath("main.nf")
        self._nextflowConfig = _nextflow.joinpath("nextflow.config")
        self._profile = _inputJson.pop("profile")
        self._inputJsonFile = _nextflow.joinpath(
            f"input_params_{self._profile}.json"
        )
        self._entryPoint = entryPoint
        self._engineStr = engine
        with open(self._inputJsonFile, "w") as f:
            json.dump(_inputJson, f, indent=4)

    def execute(self):
        log.info(f"Nextflow input: {self._inputJsonFile}")
        eval(self._profile).trigger_nf(
            workflow=self._workflow,
            inputJson=self._inputJsonFile,
            config=self._nextflowConfig,
            entryPoint=self._entryPoint,
            engineStr=self._engineStr,
        )
        pass
