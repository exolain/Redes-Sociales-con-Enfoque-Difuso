/*
 *    This program is free software; you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation; either version 2 of the License, or
 *    (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with this program; if not, write to the Free Software
 *    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

/*
 *    FCM.java
 *    Copyright (C) 2007 Wei Xiaofei
 *
 */
package  weka.clusterers;

import weka.classifiers.rules.DecisionTableHashKey;
import weka.core.Capabilities;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.Option;
import weka.core.Utils;
import weka.core.WeightedInstancesHandler;
import weka.core.Capabilities.Capability;
import weka.core.matrix.Matrix;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.ReplaceMissingValues;

import java.util.Enumeration;
import java.util.HashMap;
import java.util.Random;
import java.util.Vector;
import weka.classifiers.rules.DecisionTableHashKey;
import weka.clusterers.NumberOfClustersRequestable;
import weka.clusterers.RandomizableClusterer;
import weka.core.DenseInstance;

/**
 <!-- globalinfo-start -->
 * Cluster data using the Fuzzy C means algorithm
 * <p/>
 <!-- globalinfo-end -->
 *
 <!-- options-start -->
 * Valid options are: <p/>
 * 
 * <pre> -N &lt;num&gt;
 *  number of clusters.
 *  (default 2).</pre>
 * 
 * <pre> -F &lt;num&gt;
 *  exponent.
 *  (default 2).</pre>
 *  
 * <pre> -S &lt;num&gt;
 *  Random number seed.
 *  (default 10)</pre>
 * 
 <!-- options-end -->
 *
 * @author 
 *      Wei Xiaofei
 *      Natalia Marin
 * @version 1.1
 * @see RandomizableClusterer
 */
public class FuzzyCMeans 
  extends RandomizableClusterer 
  implements NumberOfClustersRequestable, WeightedInstancesHandler {

  /** for serialization */
  static final long serialVersionUID = -2134543132156464L;
  
  /**
   * replace missing values in training instances
   */
  private ReplaceMissingValues m_ReplaceMissingFilter;

  /**
   * number of clusters to generate
   */
  private int m_NumClusters = 2;

  /**
   * D: d(i,j)=||c(i)-x(j)
   */
  private Matrix D;
  
 // private Matrix U;
  
  /**
   * holds the fuzzifier
   */
  private double m_fuzzifier = 2;
  
  /**
   * holds the cluster centroids
   */
  private Instances m_ClusterCentroids;

  /**
   * Holds the standard deviations of the numeric attributes in each cluster
   */
  private Instances m_ClusterStdDevs;

  
  /**
   * For each cluster, holds the frequency counts for the values of each 
   * nominal attribute
   */
  private int [][][] m_ClusterNominalCounts;

  /**
   * The number of instances in each cluster
   */
  private int [] m_ClusterSizes;

  /**
   * attribute min values
   */
  private double [] m_Min;
  
  /**
   * attribute max values
   */
  private double [] m_Max;

  /**
   * Keep track of the number of iterations completed before convergence
   */
  private int m_Iterations = 0;

  /**
   * Holds the squared errors for all clusters
   */
  private double [] m_squaredErrors;

  /**
   * the default constructor
   */
  public FuzzyCMeans () {
    super();
    
    m_SeedDefault = 10;
    setSeed(m_SeedDefault);
  }
  
  /**
   * Returns a string describing this clusterer
   * @return a description of the evaluator suitable for
   * displaying in the explorer/experimenter gui
   */
  public String globalInfo() {
    return "Cluster data using the fuzzy k means algorithm";
  }

  /**
   * Returns default capabilities of the clusterer.
   *
   * @return      the capabilities of this clusterer
   */
  public Capabilities getCapabilities() {
    Capabilities result = super.getCapabilities();

    result.disableAll();
    result.enable(Capability.NO_CLASS);
    
    // attributes
    result.enable(Capability.NUMERIC_ATTRIBUTES);
    result.enable(Capability.NOMINAL_ATTRIBUTES);
    result.enable(Capability.MISSING_VALUES);

    return result;
  }

  /**
   * Generates a clusterer. Has to initialize all fields of the clusterer
   * that are not being set via options.
   *
   * @param data set of instances serving as training data 
   * @throws Exception if the clusterer has not been 
   * generated successfully
   */
  public void buildClusterer(Instances data) throws Exception {

      // can clusterer handle the data?
      getCapabilities().testWithFail(data);

      m_Iterations = 0;

      m_ReplaceMissingFilter = new ReplaceMissingValues();
      Instances instances = new Instances(data);
      instances.setClassIndex(-1);
      m_ReplaceMissingFilter.setInputFormat(instances);
      instances = Filter.useFilter(instances, m_ReplaceMissingFilter);

      m_Min = new double [instances.numAttributes()];
      m_Max = new double [instances.numAttributes()];
      for (int i = 0; i < instances.numAttributes(); i++) {
          m_Min[i] = m_Max[i] = Double.NaN;
      }
    
      m_ClusterCentroids = new Instances(instances, m_NumClusters);
      int[] clusterAssignments = new int [instances.numInstances()];

      for (int i = 0; i < instances.numInstances(); i++) {
          updateMinMax(instances.instance(i));
      }
    
      Random RandomO = new Random(getSeed());
      int instIndex;
      HashMap initC = new HashMap();
      DecisionTableHashKey hk = null;
      for (int j = instances.numInstances() - 1; j >= 0; j--) {
          instIndex = RandomO.nextInt(j+1);
          hk = new DecisionTableHashKey(instances.instance(instIndex), 
                         instances.numAttributes(), true);
          if (!initC.containsKey(hk)) {
                  m_ClusterCentroids.add(instances.instance(instIndex));
                  initC.put(hk, null);
          }
          instances.swap(j, instIndex);
      
          if (m_ClusterCentroids.numInstances() == m_NumClusters) {
                  break;
          }
      }

      m_NumClusters = m_ClusterCentroids.numInstances();
    
      D = new Matrix(solveD(instances).getArray());
      
      int i, j;
      int n = instances.numInstances();
      Instances [] tempI = new Instances[m_NumClusters];
      m_squaredErrors = new double [m_NumClusters];
      m_ClusterNominalCounts = new int [m_NumClusters][instances.numAttributes()][0];
      
      Matrix U = new Matrix(solveU(instances).getArray());
      double q = 0;
      while (true) {
          m_Iterations++;
          for (i = 0; i < instances.numInstances(); i++) {
              Instance toCluster = instances.instance(i);
              int newC = clusterProcessedInstance(toCluster, true);

              clusterAssignments[i] = newC;
          }
      
          m_ClusterCentroids = new Instances(instances, m_NumClusters);
          for (i = 0; i < m_NumClusters; i++) {
              tempI[i] = new Instances(instances, 0);
          }
          for (i = 0; i < instances.numInstances(); i++) {
              tempI[clusterAssignments[i]].add(instances.instance(i));
          }
                
          for (i = 0; i < m_NumClusters; i++) {              

              double[] vals = new double[instances.numAttributes()];
              for (j = 0; j < instances.numAttributes(); j++) {

                  double sum1 = 0, sum2 = 0;
                  for (int k = 0; k < n; k++) {
                      sum1 += U.get(i, k) * U.get(i, k) * instances.instance(k).value(j);
                      sum2 += U.get(i, k) * U.get(i, k);
                  }
                  vals[j] = sum1 / sum2;    
             
              }
              m_ClusterCentroids.add(new DenseInstance(1.0, vals) {});
          }
          
          D = new Matrix(solveD(instances).getArray());          
          U = new Matrix(solveU(instances).getArray());
          double q1 = 0;
          for (i = 0; i < m_NumClusters; i++) {
              for (j = 0; j < n; j++) {
                  /* U(i,j)^m * d(i,j)^2      */
                  q1 += Math.pow(U.get(i, j), getFuzzifier()) * D.get(i, j) * D.get(i, j);
              }
          }                      
          
        
          if (q1 - q < 2.2204e-16) {
              break;
          }    
          q = q1;
      }
      
      m_ClusterStdDevs = new Instances(instances, m_NumClusters);
      m_ClusterSizes = new int [m_NumClusters];
      for (i = 0; i < m_NumClusters; i++) {
          double [] vals2 = new double[instances.numAttributes()];
          for (j = 0; j < instances.numAttributes(); j++) {
              if (instances.attribute(j).isNumeric()) {
                  vals2[j] = Math.sqrt(tempI[i].variance(j));
              } else {
                  vals2[j] = Utils.missingValue();
                  
              }    
          }
          m_ClusterStdDevs.add(new DenseInstance(1.0, vals2));//1.0代表权值, vals2代表属性值
          m_ClusterSizes[i] = tempI[i].numInstances();
      }
      }

  /**
   * clusters an instance that has been through the filters
   *
   * @param instance the instance to assign a cluster to
   * @param updateErrors if true, update the within clusters sum of errors
   * @return a cluster number
   */
  private int clusterProcessedInstance(Instance instance, boolean updateErrors) {
    double minDist = Integer.MAX_VALUE;
    int bestCluster = 0;
    for (int i = 0; i < m_NumClusters; i++) {
      double dist = distance(instance, m_ClusterCentroids.instance(i));
      if (dist < minDist) {
          minDist = dist;
          bestCluster = i;
      }
    }
    if (updateErrors) {
        m_squaredErrors[bestCluster] += minDist;
    }
    return bestCluster;
  }

  /**
   * Classifies a given instance.
   *
   * @param instance the instance to be assigned to a cluster
   * @return the number of the assigned cluster as an integer
   * if the class is enumerated, otherwise the predicted value
   * @throws Exception if instance could not be classified
   * successfully
   */
  public int clusterInstance(Instance instance) throws Exception {
    m_ReplaceMissingFilter.input(instance);
    m_ReplaceMissingFilter.batchFinished();
    Instance inst = m_ReplaceMissingFilter.output();

    return clusterProcessedInstance(inst, false);
  }

  /**
   * d(i,j)=||c(i)-x(j)|| 
   */
  private Matrix solveD(Instances instances) {
      int n = instances.numInstances();
      Matrix D = new Matrix(m_NumClusters, n);
      for (int i = 0; i < m_NumClusters; i++) {
          for (int j = 0; j < n; j++) {
              D.set(i, j, distance(instances.instance(j), m_ClusterCentroids.instance(i)));
              if (D.get(i, j) == 0) {
                  D.set(i, j, 0.000000000001);
              }
          }
      }
      
      return D;
  }
  
  /**
   *  U(i,j) = 1 / sum(d(i,j)/ d(k,j))^(2/(m-1)
   */
  private Matrix solveU(Instances instances) { 
      int n = instances.numInstances();
      int i, j;
      Matrix U = new Matrix(m_NumClusters, n);
      
      for (i = 0; i < m_NumClusters; i++) {
          for (j = 0; j < n; j++) {
              double sum = 0;
              for (int k = 0; k < m_NumClusters; k++) {
                  //d(i,j)/d(k,j)^(2/(m-1)
                  sum += Math.pow(D.get(i, j) / D.get(k, j), 2 /(getFuzzifier() - 1));
              }
              U.set(i, j, Math.pow(sum, -1));
          }
      }
      return U;
  }
  /**
   * Calculates the distance between two instances
   *
   * @param first the first instance
   * @param second the second instance
   * @return the distance between the two given instances
   */          
  private double distance(Instance first, Instance second) {  

      double val1;
        double val2;
        double dist = 0.0;
        
        for (int i = 0; i <first.numAttributes(); i++) {
            val1 = first.value(i);        
            val2 = second.value(i);
                                    
            dist += (val1 - val2) * (val1 - val2);
        }
        dist = Math.sqrt(dist);
        return dist;
  }

  /**
   * Updates the minimum and maximum values for all the attributes
   * based on a new instance.
   *
   * @param instance the new instance
   */
  private void updateMinMax(Instance instance) {  

    for (int j = 0;j < m_ClusterCentroids.numAttributes(); j++) {
      if (!instance.isMissing(j)) {
    if (Double.isNaN(m_Min[j])) {
      m_Min[j] = instance.value(j);
      m_Max[j] = instance.value(j);
    } else {
      if (instance.value(j) < m_Min[j]) {
        m_Min[j] = instance.value(j);
      } else {
        if (instance.value(j) > m_Max[j]) {
          m_Max[j] = instance.value(j);
        }
      }
    }
      }
    }
  }
  
  /**
   * Returns the number of clusters.
   *
   * @return the number of clusters generated for a training dataset.
   * @throws Exception if number of clusters could not be returned
   * successfully
   */
  public int numberOfClusters() throws Exception {
    return m_NumClusters;
  }

  /**
   * @return
   * @throws Exception
   */
  public double fuzzifier() throws Exception {
      return m_fuzzifier;
  }
  /**
   * Returns an enumeration describing the available options.
   *
   * @return an enumeration of all the available options.
   */
  public Enumeration listOptions () {
    Vector result = new Vector();

    result.addElement(new Option(
    "\tnumber of clusters.\n"
    + "\t(default 2).", 
    "N", 1, "-N <num>"));
    
    result.addElement(new Option(
            "\texponent.\n"
            + "\t(default 2.0).",
            "F", 1, "-F <num>"));

    Enumeration en = super.listOptions();
    while (en.hasMoreElements())
      result.addElement(en.nextElement());

     return  result.elements();
  }

  /**
   * Returns the tip text for this property
   * @return tip text for this property suitable for
   * displaying in the explorer/experimenter gui
   */
  public String numClustersTipText() {
    return "set number of clusters";
  }

  /**
   * set the number of clusters to generate
   *
   * @param n the number of clusters to generate
   * @throws Exception if number of clusters is negative
   */
  public void setNumClusters(int n) throws Exception {
    if (n <= 0) {
      throw new Exception("Number of clusters must be > 0");
    }
    m_NumClusters = n;
  }

  /**
   * gets the number of clusters to generate
   *
   * @return the number of clusters to generate
   */
  public int getNumClusters() {
    return m_NumClusters;
  }

  /**
   * Returns the tip text for this property
   * @return tip text for this property suitable for
   * displaying in the explorer/experimenter gui
   */
  public String fuzzifierTipText() {
        return "set fuzzifier";
  }
  
  /**
   * set the fuzzifier
   *
   * @param f fuzzifier
   * @throws Exception if exponent is negative
   */
  public void setFuzzifier(double f) throws Exception {
        if (f <= 1) {
          throw new Exception("F must be > 1");
        }
        m_fuzzifier= f;
      }
  
  /**
   * get the fuzzifier 
   * 
   * @return m_fuzzifier
   */
  public double getFuzzifier() {
      return m_fuzzifier;
  }
  
  /**
   * Parses a given list of options. <p/>
   * 
   <!-- options-start -->
   * Valid options are: <p/>
   * 
   * <pre> -N &lt;num&gt;
   *  number of clusters.
   *  (default 2).</pre>
   * 
   *  <pre> -F &lt;num&gt;
   *  fuzzifier.
   *  (default 2.0).</pre>
   * 
   * <pre> -S &lt;num&gt;
   *  Random number seed.
   *  (default 10)</pre>
   * 
   <!-- options-end -->
   *
   * @param options the list of options as an array of strings
   * @throws Exception if an option is not supported
   */
  public void setOptions (String[] options)
    throws Exception {

    String optionString = Utils.getOption('N', options);

    if (optionString.length() != 0) {
      setNumClusters(Integer.parseInt(optionString));
    }
    
    optionString = Utils.getOption('F', options);
    
    if (optionString.length() != 0) {
        setFuzzifier((new Double(optionString)).doubleValue());
    }
    super.setOptions(options);
  }

  /**
   * Gets the current settings of FuzzyCMeans 
   *
   * @return an array of strings suitable for passing to setOptions()
   */
  public String[] getOptions () {
    int           i;
    Vector        result;
    String[]      options;

    result = new Vector();

    result.add("-N");
    result.add("" + getNumClusters());
    
    result.add("-F");
    result.add("" + getFuzzifier());

    options = super.getOptions();
    for (i = 0; i < options.length; i++)
      result.add(options[i]);

    return (String[]) result.toArray(new String[result.size()]);      
  }

  /**
   * return a string describing this clusterer
   *
   * @return a description of the clusterer as a string
   */
  public String toString() {
    int maxWidth = 0;
    for (int i = 0; i < m_NumClusters; i++) {
      for (int j = 0 ;j < m_ClusterCentroids.numAttributes(); j++) {
    if (m_ClusterCentroids.attribute(j).isNumeric()) {
      double width = Math.log(Math.abs(m_ClusterCentroids.instance(i).value(j))) /
        Math.log(10.0);
      width += 1.0;
      if ((int)width > maxWidth) {
        maxWidth = (int)width;
      }
    }
      }
    }
    StringBuffer temp = new StringBuffer();
    String naString = "N/A";
    for (int i = 0; i < maxWidth+2; i++) {
      naString += " ";
    }
    temp.append("\nFuzzy C-means\n======\n");
    temp.append("\nNumber of iterations: " + m_Iterations+"\n");
    temp.append("Within cluster sum of squared errors: " + Utils.sum(m_squaredErrors));

    temp.append("\n\nCluster centroids:\n");
    for (int i = 0; i < m_NumClusters; i++) {
      temp.append("\nCluster "+i+"\n\t");
      temp.append("\n\tStd Devs:  ");
      for (int j = 0; j < m_ClusterStdDevs.numAttributes(); j++) {
    if (m_ClusterStdDevs.attribute(j).isNumeric()) {
      temp.append(" "+Utils.doubleToString(m_ClusterStdDevs.instance(i).value(j), 
                           maxWidth+5, 4));
    } else {
      temp.append(" "+naString);
    }
      }
    }
    temp.append("\n\n");
    return temp.toString();
  }

  /**
   * Gets the the cluster centroids
   * 
   * @return        the cluster centroids
   */
  public Instances getClusterCentroids() {
    return m_ClusterCentroids;
  }

  /**
   * Gets the standard deviations of the numeric attributes in each cluster
   * 
   * @return        the standard deviations of the numeric attributes 
   *             in each cluster
   */
  public Instances getClusterStandardDevs() {
    return m_ClusterStdDevs;
  }

  /**
   * Returns for each cluster the frequency counts for the values of each 
   * nominal attribute
   * 
   * @return        the counts
   */
  public int [][][] getClusterNominalCounts() {
    return m_ClusterNominalCounts;
  }

  /**
   * Gets the squared error for all clusters
   * 
   * @return        the squared error
  */
  public double getSquaredError() {
    return Utils.sum(m_squaredErrors);
  }

  /**
   * Gets the number of instances in each cluster
   * 
   * @return        The number of instances in each cluster
   */
  public int [] getClusterSizes() {
    return m_ClusterSizes;
  }

  /**
   * Main method for testing this class.
   *
   * @param argv should contain the following arguments: <p>
   * -t training file [-N number of clusters]
   */
  public static void main (String[] argv) {
    runClusterer(new FuzzyCMeans (), argv);
  }
}