#!/usr/bin/env nextflow

/* 
    Process 4: Bulk RNA workflow
    This script is for counting of mapped reads for genes
*/

//  Declare the parameters


process IDENTIFY_STRAND {

    tag "Detect the strandedness of the read"
	publishDir "${params.feature_count_dir}", pattern: "*.txt", mode:'copy'


    input:
    path (annotation_bed)
    path (sorted_bam_file)
    path (get_strand)

    output:
    path 'rseqc_result.txt'
    stdout emit: strand 

    script:
    """
    infer_experiment.py -r $annotation_bed -i ${sorted_bam_file[0]} > rseqc_result.txt &&

    python $get_strand rseqc_result.txt FC

    """
}
process COUNT {
    tag "Counting mapped reads "
	publishDir "${params.feature_count_dir}", mode:'copy', saveAs: { file -> 
                                                                        if (file.endsWith(".tsv")){ 
                                                                            "${params.project_name}_raw_counts_fc.tsv"
                                                                            }
                                                                        else if (file.endsWith(".txt")){ 
                                                                            "${params.project_name}_raw_counts_meta_fc.txt"
                                                                            }
                                                                        else { file }
                                                                    }


    input:
    path(sorted_bam_file)
    path(annotation_gtf)
    val strand
    path(clean_counts)

    output:
    path 'counts.txt.summary', emit: log
    path 'clean_count.tsv'
    path 'counts.txt'
    path 'featurecounts.screen-output.log'

    script:
    """
    featureCounts -p --countReadPairs -t exon -T $task.cpus -M -g gene_id -s ${strand.toInteger()} -a $annotation_gtf \\
    -o counts.txt $sorted_bam_file 2> featurecounts.screen-output.log &&
    python $clean_counts counts.txt
    """
}
