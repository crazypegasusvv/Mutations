package bioinformatics;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class DNAWritable implements  WritableComparable<DNAWritable> {
    public IntWritable partitionNum;
    public Text fileName;

    public DNAWritable() {
        partitionNum = new IntWritable();
        fileName = new Text();
    }

    public void set(IntWritable num,Text name) {
        this.fileName = name ;
        this.partitionNum = num;
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        partitionNum.readFields(in);
        fileName.readFields(in);
    }

    @Override
    public void write(DataOutput out) throws IOException {
        partitionNum.write(out);
        fileName.write(out);
    }

    @Override
    public int compareTo(DNAWritable dna) {
        return fileName.compareTo(dna.fileName) == 0 ? partitionNum.compareTo(dna.partitionNum) :
                fileName.compareTo(dna.fileName);
    }

    public int equals(DNAWritable dna) {
        return this.fileName.equals(dna.fileName) && this.partitionNum == dna.partitionNum ? 0 : -1;
    }
}
