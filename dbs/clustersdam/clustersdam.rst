.. _db_clustersdam:

----------------------------------
Multi-Cloud Data Access Management
----------------------------------

In this exercise you will continue breaking up your overcrowded source SQL database server. Using Era's multi-cluster data access management policies, you will clone a SQL 2016 database on-prem to a SQL 2019 database server that you will provision on your AWS hosted Nutanix cluster.

Registering Your Source
+++++++++++++++++++++++

#. Refer to :ref:`clusterdetails` for the details required to access your environment.

#. Open **Era** in your browser and log in with the provided credentials.

#. From the **Dashboard** dropdown menu, select **Databases**.

   .. figure:: images/1.png

#. Select **Sources** from the left-hand menu and click **+ Register > Microsoft SQL Server > Database**.

#. Select **Registered** and your **USER**\ *##*\ **-MSSQL-Source** VM.

   .. figure:: images/2.png

#. Click **Next**.

#. From the list of remaining **Unregistered Databases**, select **SampleDB**.

#. Update the **Database Name in Era** to include your **USER**\ *##* id (ex. USER01-SampleDB)

   .. figure:: images/3.png

#. Click **Next**.

#. Update the **SLA** to **DEFAULT_OOB_BRONZE_SLA**. *Do not leave the default BRASS policy as this does not include continuous data protection.*

   .. figure:: images/4.png

#. Click **Register**.

Adding A Network Profile
++++++++++++++++++++++++

#. From the **Era** dropdown menu, select **Profiles**.

#. Select **Network** from the left-hand menu and click **+ Create > Microsoft SQL Server > Database Server VMs**.

#. Fill out the following fields:

   - **Name** - USER\ *##*\ _MSSQL (ex. USER01_MSSQL)
   - **Nutanix Cluster** - AWS-Cluster
   - **Public Service vLAN** - User VM Network

   .. figure:: images/5.png

#. Click **Create**.

Provisioning Database Server Target
+++++++++++++++++++++++++++++++++++

#. From the **Era** dropdown menu, select **Database Server VMs**.

#. Select **List** from the left-hand menu and click **+ Provision > Microsoft SQL Server > Single Node Server VM**.

   .. figure:: images/15.png

#. Fill out the following fields to define your database server source:

   - **Provision Database Server VM from** - Software Profile
   - **Nutanix Cluster** - AWS-Cluster
   - Select your **MSSQL_19_USER**\ *##* profile

   .. figure:: images/16.png

#. Click **Next**.

#. Fill out the following fields to configure the database server:

   - **Database Server VM Name** - USER\ *##*\ _SampleDBVM
   - **Compute Profile** - LAB_COMPUTE
   - **Network Profile** - USER\ *##*\ _MSSQL
   - **Windows License Key** - *Leave blank*
   - **Administrator Password** - nutanix/4u
   - Select **Join Domain**
   - **Windows Domain Profile** - NTNXLAB
   - **Database Parameter Profile - Instance** - DEFAULT_SQLSERVER_INSTANCE_PARAMS

   .. figure:: images/17.png

#. Click **Provision**.

#. Return to the **Operations** page in order to monitor the status. While Era is provisioning your **SampleDBVM**, you can continue to the :ref:`dbs_sqlmonitoring` exercise.

   .. note::

      Provisioning should take approximately ~10 minutes to complete.

Enabling Multi-Cluster Data Access Management
+++++++++++++++++++++++++++++++++++++++++++++

#. From the **Era** dropdown menu, select **Time Machines**.

#. Click your **USER**\ *##*\ **-SampleDB_TM** Time Machine from the list.

#. Select the **Nutanix Cluster** dropdown and note that **EraCluster** is the only available option.

   This view provides information about the current data protection status of the VM, including available snapshots and log catch ups.

   .. figure:: images/6.png

#. Select **Data Access Management** from the left-hand column.

#. Under the **Table** view, click **+ Add**

   .. figure:: images/7.png

#. Select your **AWS-Cluster** and the **DEFAULT_OOB_BRONZE_SLA** DAM Policy.

   .. figure:: images/8.png

#. Click **Add**.

#. You can monitor the status on the **Operations** page as Era creates the Log Drive on your remote **AWS-Cluster**.

   .. figure:: images/9.png

   Once this operation is done, there are additional hidden operations that need to complete before you will be able to clone your database to the remote host.

#. In **Operations**, click **Show System Operations** in the left-hand menu. It also helps to filter by **Status: Running** instead of **Status: All**.

   After Era creates a snapshot of your **USER**\ *##*\ **-SampleDB**, it will begin syncing snapshots for both the **DATABASE** and **SOFTWARE** snapshots, as shown below.

   .. figure:: images/25.png

   You only need to wait for the **DATABASE** snapshot to complete in order to continue.

   .. note::

      These jobs will remain at **5%** and then jump to **100%** on completion, they do not show linear progress of the replication. It was take up to an hour for this to complete with multiple users performing replications simultaneously across the lab environment.

#. Return to **Time Machines > USER**\ *##*\ **-SampleDB_TM > Data Access Management** and note that Time Machine data is now available on both clusters.

   .. figure:: images/11.png

#. Return to **Overview** and select **Actions > Authorize Database Server VMs**.

   .. figure:: images/18.png

#. Find and select your **USER**\ *##*\ **_SampleDBVM** and click the **>** icon to add your SQL 2019 Server to the list of VMs authorized to host clones of the **SampleDB** Time Machine.

   .. figure:: images/19.png

#. Click **Update**.

#. Select **AWS-Cluster** from the **Nutanix Cluster** dropdown menu.

#. Click **Actions > Create Database Clone > Database**.

   .. figure:: images/10.png

#. Select **Current Time** to clone your database using the latest available data.

   .. figure:: images/12.png

   .. note::

      If **Point in Time** displays **Invalid**, data is still being synced to the remote site.

#. Click **Next**.

#. Under **Database Server VM**, click **Use Authorized Server** and select your **USER**\ *##*\ **_SampleDBVM** server.

   .. figure:: images/20.png

#. Click **Next**.

#. Select **Schedule Data Refresh** and specify to **Refresh Every 2 Days**.

   .. figure:: images/14.png

   This will automatically refresh the data of your clone based on the source database. Refreshes can also be performed manually in Era.

#. Click **Clone**.

   The clone operation should take < 3 minutes to complete.

#. Once the cloning operation has completed, browse to **Era > Databases > Clones** and select your SampleDB clone. Observe that it is now running on SQL Server 2019 instead of 2016.

   .. figure:: images/21.png

.. raw:: html

    <H1><a href="http://lookup.ntnxworkshops.com/" target="_blank"><font color="#B0D235"><center>Click Here To Submit Validation Request</center></font></a></H1>

Takeaways
+++++++++

- Using Era Data Access Management (DAM) policies to replicate log and snapshot data across clusters can be used to enable dev/test use cases where non-production clones run on separate infrastructure from production Databases

- Era DAM policies can also be used to support backup and recovery scenarios, where a standby database can have access to production snapshots for quick recoveries in the event of site failures or maintenance
