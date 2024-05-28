#!/usr/bin/env nextflow

/*
    Process 2: Bulk RNA workflow
    This script is for performing quality check the raw reads after trimming
*/

// params.outdir_fastqc = 'results/fastqc_results'
process FASTQC {
	tag "FASTQC quality assessment on  $sample_id "
	publishDir "${params.qc_fastqc}", mode:'copy'	

	input:
	tuple val(sample_id), path(trimmed_read_01), path(trimmed_read_02)

	output:
	path "fastqc_${sample_id}_result", emit: logs_QC



	script:
	"""
	mkdir fastqc_${sample_id}_result
	fastqc -o fastqc_${sample_id}_result -t $task.cpus $trimmed_read_01 $trimmed_read_02
	"""
}