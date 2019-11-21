package bioinformatics;

import java.util.Scanner;

/**
 *   Interface for bioInformatics App
 *
 *  __Frame shift mutation case__
 *    index:   0  12  24 36
 *     Ref:    A  B   C   D
 *     Inp:    B  A   C   D
 *    index:   12 0   24  36
 *    add this case as frame shift mutation
 *
 */
public class App 
{
    public static void main(String[] args)
    {
        final String refFilePath = "C:\\Users\\shiva kumar dongala\\Desktop\\Mutations\\src\\main\\java\\" +
                "bioinformatics\\referenceFile.txt";
        final int maxStringSize = 128;
        System.out.print("Enter refFilePath: ");
        Scanner inputReader = new Scanner(System.in);
        //refFilePath = inputReader.nextLine();
        System.out.println("ref path is: "+refFilePath);
        Compressor dnaCompressor = new Compressor(refFilePath, maxStringSize);
        try {
            dnaCompressor.createGST();
            final int testSearches = 4;
            for (int i = 0; i < testSearches; i++) {
                String testString = inputReader.nextLine();
                dnaCompressor.searchSubStringFromGST(testString);
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("exception occured!");
        }
    }
}
