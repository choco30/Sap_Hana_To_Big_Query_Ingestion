# Sap Hana TO Big Query
## About
This Project is about fetching Data from Sap Hana Cloud To Big Query Using Apache Beam using Gcp serverless Etl solution i.e. Dataflow as a back end engine to extract the data from the source. We are orchestrating the entire workflow using GCP Composer which is the managed version of Apache Airflow. We are Also Using GCP Secret Manger to Store And Fetch the Sap Hana Credentials At Run Time.  
## Toolbox 🧰
<img src="https://www.yash.com/wp-content/uploads/2017/12/sap_hana_cloud.png" width="200" height="70" alt="SAP HANA"/> &emsp; <img src="https://lh6.googleusercontent.com/1MICxjbrbRPtEnzE54g2shaMRD2RocCIcuSOrqwaqryObCR6IrsXNb3Sd5MjBBwmoLeVcgVu_SE3vw-IbRA24SFhH4IT1xppVuuNGodDtFEykgD0Cw1vB2jITTsOgBNHvWfw27icmMs30SYgWQ" width="200" alt="GCP DTAFLOW" height="70"/>
&emsp; <img src="https://miro.medium.com/max/600/1*HEzofakm1-c4c_Qn4zjmnQ.jpeg" width ="200" height="75" alt="Apache Beam"/>
&emsp;<img src ="https://cloudzone.io/wp-content/uploads/2021/06/google-cloud-composer.jpeg" width="200" height="70" alt="GCP COMPOSER"/> &emsp;
<img src ="https://i.ytimg.com/vi/s6ytxB0YSR0/mqdefault.jpg" width="200" height="70" alt="Secret Manager"/> &emsp;
<img src ="https://marketplace.workiva.com/sites/marketplace/files/images/logos/google-cloud-storage-logo-16-7-en.svg" width="200" height="100" alt="Google Cloud Storage"/> &emsp;
<img src ="https://cxl.com/wp-content/uploads/2019/10/google-bigquery-logo-1.png" width="100" height="100" alt="Google Big Query"/> &emsp;
<img src ="https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png" width="100" height="100" alt="Python"/> &emsp;

## Installation Steps
1.First we need to install Python(3.7) and java(jdk 8) On the machine for this projet to work appropiately.<br>
2.After the successfull installation of above we need to download and <a href="https://kafka.apache.org/">Install Kafka</a> version 2.6.0 with scala version 2.12.<br>
3.Now we Need to Download Apache Spark <a href ="https://spark.apache.org/downloads.html">Apache Spark </a>version 3.3.0 with hadoop version 3.3. Download the <a href="https://github.com/cdarlint/winutils">winUtils file</a> for hadoop version 3.<br>
4.Now we need to setup the path in enviornment variables for spark and haddop.<br>
5.Login to your mongo db atlas cluster and get the connection string to coonect to the database.<br>

## Deployment Process
### starting up zookeeper server on local host 9092
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
### starting up kafka broker
.\bin\windows\kafka-server-start.bat .\config\server.properties
### Creating kafka topic 
.\bin\windows\kafka-topics.bat --create --topic <topic_name> --replication-factor 1 --partitions 1<br><br>
Now you kafka Broker is up , you need to deploy the above code in any on the IDE of your choice and you will start seeing the data in your mongodb cluster 

## Note
1.Since the kafka and mongo db connector are not part of the default spark package you need to define the connectors as the configuration while creating the spark session as mentioned in the code.<br>

2.While working with any IDE you need to import the spark and hadoop enviornment variable in the project structure under settings.
