#!/usr/bin/env nextflow

/* 
    Process 7: Bulk RNA preprocessing workflow
    This script is for coversion of bam file from MAPPING process to cram file 
*/

//  Declare the parameters 

params.outdir_bam_to_cram = 'results/bam_to_cram'

process BAM_TO_CRAM {
    tag "Converting bam file to cram file"
	publishDir "${params.cram_dir}", mode: 'copy'

    input:
    val(sample_id)
    path(sorted_bam_file)
    each path(reference_fasta)

    output:
    path "${sample_id}.cram"

    script:
    """
    samtools view -@ 30 -C -T $reference_fasta -o ${sample_id}.cram $sorted_bam_file
    """
}