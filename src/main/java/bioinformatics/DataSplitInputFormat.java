package bioinformatics;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

import java.io.IOException;
import java.util.StringTokenizer;

public class DataSplitInputFormat extends FileInputFormat<Text,Text> {

	@Override
    public RecordReader<Text, Text> createRecordReader(InputSplit split, TaskAttemptContext context) {
		return new DNARecordReader();
    }

    public class DNARecordReader extends RecordReader<Text, Text> {
        private long start;
        private long end;
        private Path path;
        private int recordLength;
        private Text key;
        private FSDataInputStream fis;
        private FileSplit fileSplit;
        private Text value;
        private boolean processed = false;

        @Override
        public void initialize(InputSplit split, TaskAttemptContext context) throws IOException {
            this.key = new Text();
            this.value = new Text();
            this.fileSplit = (FileSplit) split;
            this.start = fileSplit.getStart();
            this.end = this.start + fileSplit.getLength();
            this.path = fileSplit.getPath();
            this.recordLength = HadoopInitializer.recordLength;
            final FileSystem fs = path.getFileSystem(context.getConfiguration());
            this.fis = fs.open(path);
            this.fis.seek(start);

        }

        @Override
        public boolean nextKeyValue() throws IOException {
            int partitionNumber = (int) (start / recordLength);
            String filename = null;
            key.set(String.valueOf(partitionNumber));
            StringTokenizer stk = new StringTokenizer(path.toString(), "/");

            while(stk.hasMoreTokens()) {
                filename = stk.nextToken();
            }

            key.append(filename.getBytes(), 0, filename.length());

            if(start < end && !processed) {
                byte[] buffer = new byte[(int) fileSplit.getLength()];
                int totalRead = 0;
                int totalToRead = (int) fileSplit.getLength();
                while(totalRead != totalToRead) {
                    totalRead += this.fis.read(buffer, 0, totalToRead);
                    value.set(buffer);
                }
                processed = true;
                return true;
            }
            return false;
        }

        @Override
        public Text getCurrentKey() {
            return key;
        }

        @Override
        public Text getCurrentValue() {
            return value;
        }

        @Override
        public float getProgress() {
            return processed ? 1.0f : 0.0f;
        }

        @Override
        public void close() {

        }
    }
}
