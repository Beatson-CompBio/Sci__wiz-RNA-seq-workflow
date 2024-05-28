#!/usr/bin/env nextflow

/* 
    Process 3: Bulk RNA workflow
    This script is for mapping of the reads to the reference genome
*/

//  Declare the parameters
// params.outdir_mapped = 'results/mapping_results'

// Process 3a: Decommpress the fastq files 
process DECOMPRESS {
    tag "Decompressing $sample_id trimmed read files"
    stageInMode 'copy'

    input:
    tuple val(sample_id), path(trimmed_reads)

    output: 
    path "*.fastq", arity: '1..*', emit: unzipped_reads

    script:
    """
    gunzip -f ${trimmed_reads[0]}
    gunzip -f ${trimmed_reads[1]}
    """
}

// Process 3b
process MAPPING {
    tag "Mapping $sample_id to reference genome "
	publishDir "${params.bam_dir}", pattern: "*Aligned.sortedByCoord.out.bam", mode:'copy', saveAs: { file -> 
                                                                                                        {"${sample_id}.bam"}
                                                                                                    }
    publishDir "${params.qc_alignment}", pattern: "*.tab" , mode: 'copy'
    publishDir "${params.qc_alignment}", pattern: "*.out" , mode: 'copy'

    input:
    tuple val(sample_id), path(trimmed_read_01), path(trimmed_read_02) 
    each path(index)

    output:
    path "${sample_id}.Aligned.sortedByCoord.out.bam", arity : "1..*", emit: sorted_bam_file
    path "${sample_id}.Log.final.out" 
    path "${sample_id}.Log.out"
    path "${sample_id}.Log.progress.out"
    path "${sample_id}.SJ.out.tab"

    script:
    """
    zcat ${trimmed_read_01} > ${sample_id}_1.fastq
    zcat ${trimmed_read_02} > ${sample_id}_2.fastq
    STAR --runThreadN $task.cpus\
        --genomeDir $index\
        --readFilesIn ${sample_id}_1.fastq ${sample_id}_2.fastq \
        --outFileNamePrefix ${sample_id}.\
        --outSAMtype BAM SortedByCoordinate
    """
}