#!/usr/bin/env nextflow

/* 
    Process 5: Bulk RNA workflow
    This script is for generating a quality report from previous processes"
*/

//  Declare the parameters
// params.outdir_multiqc = 'results/multiqc_results'


process MULTIQC {

    tag "Gathering quality report"
	publishDir "${params.qc_multiqc}", mode:'copy', overwrite: true

    input:
    path ("*")
    path config

    output:
    path 'multiqc_report.html'

    script:
    """
    cp $config/* .
    echo "custom_logo: \$PWD/sicruk_logo.png" >> multiqc_config.yaml
    multiqc *
    """
}