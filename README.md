# Sap Hana TO Big Query
## About
This Project is about fetching Data from Sap Hana Cloud To Big Query Using Apache Beam using Gcp serverless Etl solution i.e. Dataflow as a back end engine to extract the data from the source. We are orchestrating the entire workflow using GCP Composer which is the managed version of Apache Airflow. We are Also Using GCP Secret Manger to Store And Fetch the Sap Hana Credentials At Run Time.  
## Toolbox 🧰
<img src="https://www.yash.com/wp-content/uploads/2017/12/sap_hana_cloud.png" width="200" height="70" alt="SAP HANA"/> &emsp; <img src="https://lh6.googleusercontent.com/1MICxjbrbRPtEnzE54g2shaMRD2RocCIcuSOrqwaqryObCR6IrsXNb3Sd5MjBBwmoLeVcgVu_SE3vw-IbRA24SFhH4IT1xppVuuNGodDtFEykgD0Cw1vB2jITTsOgBNHvWfw27icmMs30SYgWQ" width="200" alt="GCP DTAFLOW" height="70"/>
&emsp; <img src="https://miro.medium.com/max/600/1*HEzofakm1-c4c_Qn4zjmnQ.jpeg" width ="170" height="75" alt="Apache Beam"/>
&emsp;<img src ="https://cloudzone.io/wp-content/uploads/2021/06/google-cloud-composer.jpeg" width="170" height="70" alt="GCP COMPOSER"/> &emsp;
<img src ="https://i.ytimg.com/vi/s6ytxB0YSR0/mqdefault.jpg" width="170" height="70" alt="Secret Manager"/> &emsp;
<img src ="https://marketplace.workiva.com/sites/marketplace/files/images/logos/google-cloud-storage-logo-16-7-en.svg" width="200" height="100" alt="Google Cloud Storage"/> &emsp;
<img src ="https://cxl.com/wp-content/uploads/2019/10/google-bigquery-logo-1.png" width="170" height="100" alt="Google Big Query"/> &emsp;
<img src ="https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png" width="170" height="100" alt="Python"/> &emsp;

##Architecture Diagram

<img src ="https://github.com/choco30/Sap_Hana_To_Big_Query_Ingestion/blob/main/SAP%20To%20Big%20Query%20architecture%20Diagram.png" width="900" height="900" alt="Python"/> &emsp;

## Installation Steps
1.For running Dataflow We need to install Java Jdk 8 on the master node. FOr that we are making use of GCS Bucket to hold the JDk 8 Package and installing the dependency at run time on the master Node.<br>
2.We are making use of Setup.py file to pass on the list of all the dependency that needs to be installed at run time on the worker nodes.
A better production approach could be to make a custom container having all the required dependency installed and will be provided to the dataflow job at run time which will increases the job efficiency as need to install dependency seprately on each worker node during up scalling will vanquish. <br>
3.For security purpose we are making use of Gcp Secret Manager to hold the SAP HANA Login Credentials and are fetching them at run time.<br>
4.We are holding the Schema of Big Query Tables as json in GCS Bucket and fetching them at run time.<br>


## Deployment Process
### Triggering dataflow Job
For Running Dataflow Job we are making use of Gcp composer which is the maged version of apache airflow to orchestrate the entire ELT Pipeline which is scheduled dat daily midnight. we are making use of SMTPLIB library to sent the email notification in case of success and failuer of JOb./ 
