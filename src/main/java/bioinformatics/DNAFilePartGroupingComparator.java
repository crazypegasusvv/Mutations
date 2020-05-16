package bioinformatics;

import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;

public class DNAFilePartGroupingComparator extends WritableComparator {
	 public DNAFilePartGroupingComparator() {
		 super(DNAWritable.class, true);
	 }

	 public int compare(WritableComparable wc1, WritableComparable wc2) {
		 DNAWritable dw1 = (DNAWritable) wc1;
		 DNAWritable dw2 = (DNAWritable) wc2;
		 return dw1.fileName.compareTo(dw2.fileName);
	 }
}
