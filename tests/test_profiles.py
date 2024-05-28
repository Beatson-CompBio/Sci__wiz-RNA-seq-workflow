#!/usr/bin/env python
"""
Created on 2024-01-29 13:28:36
Module desc: Test Module for profile
@author: m.sikarwar
"""
from sci_wiz.profiles import vm, hpc, ErrorAtSlurmSubmission, ErrorInNextflowProc
import pytest
from unittest import mock


@pytest.fixture
def vm_profile():
    return vm()


@pytest.fixture
def hpc_profile():
    return hpc()


@pytest.fixture
def mock_subprocess():
    with mock.patch("sci_wiz.profiles.subprocess") as mock_subprocess:
        yield mock_subprocess


@pytest.fixture
def mock_subprocess_run():
    with mock.patch("sci_wiz.profiles.subprocess.run") as mock_subprocess_run:
        yield mock_subprocess_run


@pytest.fixture
def mock_time():
    with mock.patch("sci_wiz.profiles.time.sleep") as mock_time:
        yield mock_time


@pytest.fixture
def mock_getlogin():
    with mock.patch("sci_wiz.profiles.getuser") as mock_getlogin:
        yield mock_getlogin


@pytest.fixture
def mock_template():
    with mock.patch("sci_wiz.profiles.Template.render") as mock_template:
        yield mock_template


def test_vm_trigger_nf_positive_case(mock_subprocess):
    """
    Test the trigger_nf function in the vm profile
    """
    mock_subprocess.Popen().__enter__().wait.return_value = 0
    vm.trigger_nf(workflow="workflow.nf", config="config.nf", inputJson="input.json")
    mock_subprocess.Popen.assert_called()
    pass


def test_vm_trigger_nf_negative_case(mock_subprocess):
    """
    Test the trigger_nf function in the vm profile
    """
    with pytest.raises(ErrorInNextflowProc) as ex_info:
        vm.trigger_nf(
            workflow="workflow.nf", config="config.nf", inputJson="input.json"
        )
    assert mock_subprocess.Popen.call_count == 1
    assert mock_subprocess.wait() != 0


def test_hpc_wait_for_slurm_job_completed(mock_subprocess_run):
    """
    Test the trigger_nf function in the hpc profile
    """
    mock_subprocess_run.side_effect = [
        mock.Mock(
            stdout="JOBID PARTITION     NAME USER    STATE   TIME\n", returncode=0
        ),  # squeue
        mock.Mock(
            stdout="JobID           JobName  Partition    Account  AllocCPUS      State ExitCode \n------------ ---------- ---------- ---------- ---------- ---------- -------- \n16870_2            pump    compute        y90          6  COMPLETED      0:0 \n16870_2.bat+      batch                   y90          6  COMPLETED      0:0 \n",
            returncode=0,
        ),
        # mock.Mock(
        #     stdout="JobID           JobName  Partition    Account  AllocCPUS      State ExitCode \n------------ ---------- ---------- ---------- ---------- ---------- -------- \n16870_2            pump    compute        y90          6  COMPLETED      0:0 \n16870_2.bat+      batch                   y90          6  COMPLETED      0:0 \n",
        #     returncode=0,
        # ),
    ]
    hpc.wait_for_slurm_job("12345")
    mock_subprocess_run.assert_has_calls(
        [
            mock.call(["squeue", "-j", "12345"], capture_output=True, text=True),
            mock.call(["sacct", "-j", "12345"], capture_output=True, text=True),
        ]
    )


def test_wait_for_slurm_job_in_progress(mock_subprocess_run, mock_time, mock_getlogin):
    # Simulate a job still in progress
    mock_subprocess_run.side_effect = [
        mock.Mock(
            stdout="JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)\n12345      job123      normal       user123 PD       0:0      2 (Resources)\n",
            returncode=0,
        ),  # squeue
        mock.Mock(
            stdout="JobID           JobName  Partition    Account  AllocCPUS      State ExitCode \n------------ ---------- ---------- ---------- ---------- ---------- -------- \n16870_2            pump    compute        y90          6  COMPLETED      0:0 \n16870_2.bat+      batch                   y90          6  COMPLETED      0:0 \n",
            returncode=0,
        ),
        mock.Mock(
            stdout="JOBID PARTITION     NAME USER    STATE   TIME\n", returncode=0
        ),  # squeue
        mock.Mock(
            stdout="JobID           JobName  Partition    Account  AllocCPUS      State ExitCode \n------------ ---------- ---------- ---------- ---------- ---------- -------- \n16870_2            pump    compute        y90          6  COMPLETED      0:0 \n16870_2.bat+      batch                   y90          6  COMPLETED      0:0 \n",
            returncode=0,
        ),
    ]
    mock_getlogin.return_value = "user123"
    hpc.wait_for_slurm_job("12345")
    mock_subprocess_run.assert_has_calls(
        [
            mock.call(["squeue", "-j", "12345"], capture_output=True, text=True),
            mock.call(["squeue", "-u", "user123"], capture_output=True, text=True),
            mock.call(["squeue", "-j", "12345"], capture_output=True, text=True),
            mock.call(["sacct", "-j", "12345"], capture_output=True, text=True),
        ]
    )
    mock_time.assert_called_once_with(60)


def test_trigger_nf_successful_submission(mock_subprocess_run, mock_template):
    mock_subprocess_run.side_effect = [
        mock.Mock(returncode=0, stdout="Submitted batch job 12345"),  # sbatch
        mock.Mock(
            stdout="JOBID PARTITION     NAME USER    STATE   TIME\n", returncode=0
        ),  # squeue
        mock.Mock(
            stdout="JobID           JobName  Partition    Account  AllocCPUS      State ExitCode \n------------ ---------- ---------- ---------- ---------- ---------- -------- \n16870_2            pump    compute        y90          6  COMPLETED      0:0 \n16870_2.bat+      batch                   y90          6  COMPLETED      0:0 \n",
            returncode=0,
        ),
    ]
    mock_template.return_value = "...slurm script content..."

    hpc.trigger_nf(
        profile="test_profile",
        workflow="test_workflow",
        config="test_config",
        inputJson="test_inputJson",
    )

    mock_subprocess_run.assert_has_calls(
        [
            mock.call(
                ["bash", "-c", "echo -e '...slurm script content...' | sbatch"],
                capture_output=True,
                text=True,
            ),
            mock.call(["squeue", "-j", "12345"], capture_output=True, text=True),
            mock.call(["sacct", "-j", "12345"], capture_output=True, text=True),
        ]
    )


def test_trigger_nf_failed_submission(mock_subprocess_run, mock_time, mock_template):
    mock_subprocess_run.return_value = mock.Mock(
        returncode=1, stderr="Error submitting job"
    )
    mock_template.return_value = "...slurm script content..."

    with pytest.raises(ErrorAtSlurmSubmission) as ex_nifo:
        hpc.trigger_nf(
            profile="test_profile",
            workflow="test_workflow",
            config="test_config",
            inputJson="test_inputJson",
        )

    mock_subprocess_run.assert_called_once_with(
        ["bash", "-c", "echo -e '...slurm script content...' | sbatch"],
        capture_output=True,
        text=True,
    )
    mock_time.assert_not_called()
    assert """Something went wrong with slurm submission with error""" in str(
        ex_nifo.value
    )
