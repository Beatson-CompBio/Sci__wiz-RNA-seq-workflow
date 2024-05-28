/*
This workflow runs a function that grabs reads from the same subdirectories of different 
sequence run batch, cat them together add save in a given destination
*/


workflow setup{
    take:
        run1
        run2
        dest
        
    main:
    merge_run(params.run1, params.run2, params.dest )    
}

// function 
def merge_run (run1, run2, dest){
    
        try {
            
        // check if destination folder exist 
            def baseDir_A = new File (run1) 
            def baseDir_B = new File (run2) 
            def basedir_C = new File (dest)
            if (basedir_C.exists()) {
                basedir_C.deleteDir()
                }
        // create the destination directory
            basedir_C.mkdir()    

    
        // concat run1 and run2 into destination folder
            
            ConcatFile.concatFile(baseDir_A, baseDir_B, basedir_C)                                                   
        
        } catch ( Exception ex){
            println ("Error message : ${ex.getMessage()}")

        }
        

    }
    

