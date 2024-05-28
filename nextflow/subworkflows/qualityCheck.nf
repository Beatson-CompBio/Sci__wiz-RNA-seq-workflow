include { FASTP } from '../modules/fastp'
include { FASTQC } from '../modules/fastqc'
include { MULTIQC } from '../modules/multiqc'

//wworkflow to run QC on raw fastq files to select the number of bases that needed to be trimmed.
workflow rawQc {
    read_ch = channel.fromFilePairs(params.reads, checkIFExists: true)
            | map { row -> 
            Transformer.transformSampleId(row)
    }

    main:
        fastp_json = null
        fastp_html = null
        if (!params.initial_qc) {
            FASTP(read_ch)
            read_ch = FASTP.out.trim_reads
            fastp_json = FASTP.out.json
            fastp_html = FASTP.out.html
        }
        FASTQC(read_ch)
        if (params.initial_qc){
            MULTIQC(FASTQC.out.collect(), params.multiqc_config)
        }

    emit:
        read_ch
        fastp_json
        fastp_html
        fastqc_logs = FASTQC.out.logs_QC
}