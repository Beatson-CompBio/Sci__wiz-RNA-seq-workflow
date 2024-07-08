# CRUK Scotland Institute Workflow Wizard: sci_wiz

sci_wiz packages Nextflow framework and Python's modular approach under the hood to deliver easy-to-use functionalities for RNA-Seq data pre-processing using standard and widely accepted tools. The package is designed to install all the dependencies required to run the workflow so that you do not have to install them separately.

> [!NOTE]
> You will need to download the STAR index, reference genome, and annotation files separately. The package will not download these files for you.


What *sci_wiz* can do:

1. Data pre-processing: Running data pre-processing workflow will carry out the below steps and generate read count matrix. More information on the tools used in each step can be accessed using the links.
    1. Trimming: uses FastP.
    2. Reads QC: FastQC and MultiQC.
    3. Mapping: we are using [STAR](https://hbctraining.github.io/Intro-to-rnaseq-hpc-O2/lessons/03_alignment.html).
    4. Counting: FeatureCounts.
    5. Bam to Cram: for optimising BAM file storage.

* [System Requirements](#system-requirements)
* [Quick start](#quick-start)
* [Import as a module](#import-as-a-module)

## System Requirements

Running this package will require you to have access to virtual machine or high-performance cluster(hpc). Below are the requirements for running this package:

* Python 3.10 or higher
* Slurm scheduler for running on HPC

> [!NOTE]
> You should have required access to create and remove symlinks.
> Increase the number of file that your system can open using `ulimit -n 3000`. The number mentioned here is a suggestion from STAR developers in this [issue](https://github.com/alexdobin/STAR/issues/1099).It is possible STAR might fails because of open file limit error.

## Quick start

To help you quickly start your RNA-seq analysis, we have developed a package which can be quickly installed. It also provide you options to either use the Command Line Interface(CLI) or import it in a script. We recommend using a using a virtual environment to run all the analyses so that your system configuration remains as it is.

### Installation

* Let's start by creating a virtual environment and activate it. After running commands below, you should see the your virtual env. name at the far left end of the terminal. If not, please refer to python documentation on how to create a *[virtual env](https://docs.python.org/3/library/venv.html)*.

```python
python -m venv .sci_wiz && source .sci_wiz/bin/activate
```

* Download the **latest** package [.whl file](https://github.com/Beatson-CompBio/sci_wiz-rna-seq-workflow/releases) from the release section of this repository and save it into your current working directory. Use the following command to install the package.

```python
pip install sci_wiz-{version}-py3-none-any.whl
```

* You could check all the functionalities that *sci_wiz* provides using `--help` command.

```console
sci_wiz --help
```

### Configuration

* This is a required configuration step that would generate an *user_input.ini* file to store your inputs. Run below command in your terminal:

```console
sci_wiz create-config
```

* You should have an *user_input.ini* file in your current working directory. The *.ini* file will take your input that required to run the data pre-processing smoothly.

```YAML
[USER_INPUT]
project_name = G12_yymm_uniqueName # G12 is group code, yymm: year and month; uniqueName.
profile = hpc    # 'vm' if running on VM, 'hpc' if running on HPC.
reads = /project_name/*/*_{R1,R2}_001.fastq.gz # absolute path
output_dir = /project_name/Data/
index = STAR_75bp_or_150bp
annotation = Org.OrgCode.110.gtf
reference = Org.OrgCode.110.fa
annotation_bed = Org.OrgCode.110.bed
batch_info = false   # batch_info True will require run1, run2 batch_destination, input_reads will be ignored.
run1 = 
run2 = 
batch_destination = 

[TRIMMING]
trim_front_read_01 = 1 # will trim the front bases from read 1
trim_front_read_02 = 1 # will trim front bases from read 2
trim_tail_read_01 = 0 # will trim tail bases from read 1
trim_tail_read_02 = 0 # will trim tail bases from read 2
```

* **project_name**: project name, it will provide you with an option to follow project naming convention.
* **profile**: type of system, such as a virtual machine or high-compute cluster, you are using to run this analysis.
* **reads**: Path to input raw RNA-seq reads in fastq.gz format.
* **output_dir**: Base path for the output directory.
* **index**: Path to the STAR index. *Right now this workflow only supports alignment using STAR.*
* **annotation**: Path to the GTF file containing gene annotations.
* **reference**: Path to the reference genome FASTA file.
* **annotation_bed**: Path to the BED file containing gene annotations.
* **batch_info**: Flag indicating whether raw files are available in multiple batches. If this is *True*, you will need to provide *run1*, *run2*, & *batch_destination*.
* **run1** and **run2**: Paths to raw data for batch setup.
* **batch_destination**: Destination path for organized batch data.
* **trim_front_read_01**: Number of bases trimmed from front of Read_01. Default is 1.
* **trim_front_read_02**: Number of bases trimmed from front of Read_02. Default is 1.
* **trim_tail_read_01**: Number of bases trimmed from tail of Read_01. Default is 0.
* **trim_tail_read_02**: Number of bases trimmed from tail of Read_02. Default is 0.

### Data Pre-processing

> [!IMPORTANT]
> If you want to use the default trimming inputs then directly use the pre-processing command. Otherwise, have a look at this [section](#trimming-raw-data) first.
> Please make sure the system requirements are met before running the below commands.

* Simply trigger the data pre-processing commands. This program will work smoothly if the below two conditions are satisfied
    * Given inputs are as expected.
    * You have permission to read all the required files & folder such as *input.fastq.gz, index folder, annotation.gtf,annotation.bed, & reference.fa*.

```console
sci_wiz run-preprocessing
```

#### Running in a virtual machine(VM)

* Make sure you have entered `vm` as your profile in *user_input.ini*. For example:

```YAML
[USER_INPUT]
profile = vm
...
```

#### Running in a virtual machine(HPC)

**Dependency**: Current workflow is only configured to work with *SLURM*.

* Make sure your input data is available in the shared scratch, preferably in you current working directory.

* *profile* for running data pre-processing in `hpc` should have input as below:

```YAML
[USER_INPUT]
profile = hpc
...
```

### Trimming raw data

The [Illumina Stranded library preparation kit](https://emea.illumina.com/products/by-type/sequencing-kits/library-prep-kits/stranded-mrna-prep.html) is used as the default kit. This kit requires trimming of the first base from both reads. The settings for this are the default in the *user_input.ini* file. **If you are using a different library preparation kit, the trimming parameters may be different.** Please check the documentation for your kit. If the kit requires different trimming or if you want to switch off trimming, you can do this by editing the *user_input.ini* file. The workflow uses [FastP](https://github.com/OpenGene/fastp) and the *user_input.ini* file uses the same flags as FastP but for a controlled set of parameters. The following command will just run the initial QC step, not trimming:

```console
sci_wiz run-initial-qc
```

## Import as a module

Did I mention that you can import rna_seq module and carry out all the above steps in a script or jupyter notebook? Here is a quick example:

```python
from sci_wiz import rna_seq

rna_seq.generate_config()
# run below step after editing user_input.ini
rna_seq.launch_data_preprocessing()
```

Here is a [jupyter notebook](main.ipynb) with same steps that you can expand according to your use case.

## Report issues

If you find any issues with our code, you can reach out to us by:

* Reporting Issues: If you encounter any issues or bugs, please create a detailed issue report on the repository.

* Providing Feedback: Share your feedback on existing features or suggest improvements.

* Documentation Edits: If you find any discrepancies or have suggestions for improving the documentation, feel free to submit edits or open an issue.



## Citation

If you find *sci_wiz* useful in your research, please consider citing it:

```bibtex
@software{
    sci_wiz,
    author = {Ojo, Ifedayo and Sikarwar, Mayank and Kwan, Ryan and Shaw, Robin and Miller, Crispin},
    month = {1},
    title = {CRUK Scotland Institute Workflow Wizard: sci_wiz},
    url = {https://github.com/Beatson-CompBio/RNA-seq-workflow},
    year = {2024}
    }
```

### How to cite dependencies?

We will really appreciate if you could also cite the dependencies using this [bib file](./Documentation/dependencies.bib):

* Nextflow
* Bamtools
* FeatureCounts
* Fastp
* STAR
* Multiqc
