package lib
import static groovy.io.FileType.*
class ConcatFile {

        /* This groovy class has a method that takes three 
        directories. Two sequence runs directories and the destination directory 
        It concat fastq files from the seqences run directory  and returns the 
        concated files in the given destination directory 
        */
       

       static void concatFile(File run1_Dir, File run2_DIR, File destDir) {
        // Create lists to capture the files in both directory 
        List names_A = []
        run1_Dir.eachFileRecurse FILES, { names_A << it }
        List names_B = []
        run2_DIR.eachFileRecurse FILES, { names_B << it }

        // Iteration of the two lists to append the files in dir B to files in dir A
        names_A.each { nom_A ->
            names_B.each { nom_B -> 
                if(nom_A.getParentFile().getName() == nom_B.getParentFile().getName()){
                    if (nom_A.name == nom_B.name) {
                        ["bash", "-c", "zcat $nom_A $nom_B | gzip > $destDir/${nom_A.name}"].execute()
                    }
                }

            }

        }

    }
}

