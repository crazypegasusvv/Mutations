package bioinformatics;

import bioinformatics.suffixtree.GeneralizedSuffixTree;
import org.jetbrains.annotations.Contract;

import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;

import static java.util.Collections.sort;

public class Compressor {

        /**
         *   Create GeneralizedSuffixTree from inputFile
         *   @param  maxStringSize     max length of each string in GST
         *   @param  refFilePath       reference file input
         *
        */
        private final int              maxStringSize;
        private final String           refFilePath;
        private GeneralizedSuffixTree  gst;

        @Contract(pure = true)
        public Compressor(String  refFilePathInput, int stringMaxSizeInput) {
            this.refFilePath = refFilePathInput;
            this.maxStringSize = stringMaxSizeInput;
        }

        public void createGST()  {
            try {
                gst = new GeneralizedSuffixTree();
                FileInputStream refFileStream = new FileInputStream(refFilePath);
                StringBuilder sb = new StringBuilder();
                int stringIndex = 0;
                System.out.println("-------- Tree Generation begin -------");
                int startTime = (int) System.currentTimeMillis();
                while(refFileStream.available() > 0 && stringIndex < 87654) {
                    char ch = (char)refFileStream.read();
                    if(Character.isLetter(ch)) {
                        if(sb.length() == maxStringSize) {
                           // System.out.println("string put in gst:  with index: " + stringIndex);
                            gst.put(sb.toString(), stringIndex++);
                            sb.delete(0, 1);
                        }
                        sb.append(ch);
                    }
                }
                //System.out.println("string put in gst: " + sb.toString() + " with index: " + stringIndex);
                gst.put(sb.toString(), stringIndex++);
                int endTime = (int) System.currentTimeMillis();
                System.out.println("-------- Tree Generated -----------");
                System.out.println("start-time: " +startTime+ " end-time: "+endTime);
                System.out.println("Time taken is: "+ (endTime - startTime)+" ms");
            } catch(Exception e) {
                e.printStackTrace();
                System.out.println("Failed to open refFile");
            }
        }

        public void searchSubStringFromGST(final String dnaSequence) {
            List<Integer> indexList = new ArrayList<Integer>(gst.search(dnaSequence));
            sort(indexList);
            if(indexList.isEmpty()) {
                System.out.println("string not found in generalized suffix tree!");
            } else {
                System.out.println("string found at index: "+ indexList.get(0));
            }
        }
}
