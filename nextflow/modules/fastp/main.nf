#!/usr/bin/env nextflow

/* 
    Process 1: Bulk RNA preprocessing workflow
    This script is for trimmimg of the reads 
*/

//  Declare the parameters 

process FASTP {
	tag "Trimming $sample_id with FASTP"
	publishDir "${params.trimmed}", pattern: "*trimmed.fastq.gz", mode: "copy"
	publishDir "${params.qc_fastp}", pattern: "*.html", mode: "copy"
	publishDir "${params.qc_fastp}", pattern: "*.json", mode: "copy"

	input:
	tuple val(sample_id), path(read_01), path(read_02)

	output:
	tuple val(sample_id), path("${sample_id}_R1_001.trimmed.fastq.gz"), path("${sample_id}_R2_001.trimmed.fastq.gz"), \
		emit: trim_reads
	path "${sample_id}_fastp.html", emit: html
	path "${sample_id}_fastp.json", emit: json

	script:
    """
	fastp -w ${task.cpus}\\
	 	-f ${params.trim_front_read_01}\\
		-t ${params.trim_tail_read_01}\\
		-F ${params.trim_front_read_02}\\
		-T ${params.trim_tail_read_02}\\
	  	-i ${read_01}\\
	   	-I ${read_02}\\
	    -o ${sample_id}_R1_001.trimmed.fastq.gz\\
		-O ${sample_id}_R2_001.trimmed.fastq.gz\\
		-h ${sample_id}_fastp.html\\
		-j ${sample_id}_fastp.json \\
	"""
}