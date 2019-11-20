package bioinformatics;

import java.io.IOException;

import bioinformatics.suffixtree.GeneralizedSuffixTree;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.output.MultipleOutputs;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class HadoopInitializer {
    private static int partition_size;
    public static int recordLength;
    private static int mss;
    private static String refFilePath;
    private static GeneralizedSuffixTree gst;

    public static class SequenceMapper extends Mapper<Text, Text, DNAWritable, Text> {

        @Override
        protected void setup(Context context) {

        }

        protected void map(Text key, Text value, Context context) {

        }

        protected void cleanup(Context context) {

        }
    }

    public static class SequenceFilePartitioner extends Partitioner<DNAWritable, Text> {
        @Override
        public int getPartition(DNAWritable key, Text val, int num_partitions) {
            return key.fileName.hashCode() % 100;
        }
    }

    public static class SequenceReducer extends Reducer<DNAWritable, Text, Text, Text> {
        private MultipleOutputs mos;

        protected void setup(Context context) {
            mos = new MultipleOutputs(context);
        }

        public void reduce(DNAWritable key, Iterable<Text> value, Context context) {
            try {

            } catch(Exception e) {
                e.printStackTrace();
            }
        }

        protected void cleanup(Context context) throws IOException,InterruptedException {
            mos.close();
        }
    }

    private static void formRefIndex(int maxStringSize, String refFilePath)
    {
        System.out.println("ref path is: "+refFilePath);
        Compressor dnaCompressor = new Compressor(refFilePath, maxStringSize);
        try {
            HadoopInitializer.gst = dnaCompressor.createGST();
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("exception occurred!");
        }
    }

    public static void runJob(String inputPath,String outputPath,String mss,String ref) throws IOException, ClassNotFoundException, InterruptedException
    {
        /*final String refFilePath = "D:\\Reading\\Final Year Project\\Main\\BioInformatics\\Mutation\\src\\main\\" +
                "java\\bioinformatics\\referenceFile.txt";*/
        final int maxStringSize = Integer.parseInt(mss);
        HadoopInitializer.mss = maxStringSize;
        HadoopInitializer.refFilePath = ref;
        formRefIndex(maxStringSize, ref);

        Configuration conf = new Configuration();
        conf.setInt("mss", Integer.parseInt(mss));

        Job job = Job.getInstance();
        job.setJarByClass(HadoopInitializer.class);
        job.setJobName("FileSplitter");

        FileInputFormat.setMinInputSplitSize(job, 10);
        FileInputFormat.setMaxInputSplitSize(job, 400);
        HadoopInitializer.partition_size = 400;
        HadoopInitializer.recordLength = 400;
        FileInputFormat.addInputPath(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path(outputPath));

        job.setInputFormatClass(DataSplitInputFormat.class);
        job.setMapperClass(SequenceMapper.class);
        job.setPartitionerClass(SequenceFilePartitioner.class);
        job.setGroupingComparatorClass(DNAFilePartGroupingComparator.class);
        job.setReducerClass(SequenceReducer.class);
        job.setMapOutputKeyClass(DNAWritable.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileSystem fs = FileSystem.get(new Configuration());
        fs.delete(new Path(""), true);

        job.waitForCompletion(true);
    }
}
