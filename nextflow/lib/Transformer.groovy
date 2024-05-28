package lib
// Helper functions 
class Transformer {

        static List transformSampleId(List readsWithMetadata){
        // get the index of the sample identifier
                if (readsWithMetadata[0].tokenize("_").any{it ==~ /^S\d+$/}){
                        def index = readsWithMetadata[0].tokenize("_").findIndexOf{ it ==~ /^S\d+$/}
                        // check identifier and transform if necessary
                        def prefix
                        if (readsWithMetadata[0].tokenize('_')[index].size() == 2) {
                              prefix = readsWithMetadata[0].tokenize('_')[index][0] + '0' + readsWithMetadata[0].tokenize('_')[index][1]
                        } else if (readsWithMetadata[0].tokenize('_')[index].size() == 3){
                             prefix = readsWithMetadata[0].tokenize('_')[index]
                        }
                        // Re-arrange the sampele id
                        def suffix = readsWithMetadata[0].tokenize('_')
                        suffix.remove(index)
                        def sample_id = [prefix, *suffix].join('_')
                        def reads = readsWithMetadata[1]
                        return [sample_id, reads[0], reads[1]]
                }
                else {
                        // pipeline does proceed if the sample name is not in the usual(beatson) format.
                        // considerring scenario when fastq file does not have sample identifier
                        // println "Error: check if the file ${readsWithMetadata[1]} has a sample identifier"
                        return [readsWithMetadata[0], readsWithMetadata[1][0], readsWithMetadata[1][1]]
                }
        
        }

}
