.. _db_clustersaag:

------------------------------------
Multi-Cloud Application Availability
------------------------------------

In this exercise you will migrate your production Fiesta database from a non-HA SQL Server 2016 VM, hosting multiple other databases, to a dedicated SQL 2019 AlwaysOn Availability Group stretched across your on-prem and AWS environments to provide maximum resiliency.

Registering Your Source
+++++++++++++++++++++++

Registering a database/database server with Era allows you to create a Time Machine for your database, deploy databases to that server, or to use that server as the basis for a Software Profile.

.. note::

   You must meet the following requirements before you register a SQL Server database with Era:

   - A local user account or a domain user account with administrator privileges on the database server must be provided.
   - Windows account or the SQL login account provided must be a member of sysadmin role.
   - SQL Server instance must be running.
   - Database files must not exist in C:\ Drive.
   - Database must be in an online state.
   - Windows remote management (WinRM) must be enabled

#. Refer to :ref:`clusterdetails` for the details required to access your environment.

#. Open **Era** in your browser and log in with the provided credentials.

   .. note::

      You may experienced a delay getting a log in prompt the first time you log into Era. It could take as much as 3 minutes. Era ENG is investigating.

#. From the **Dashboard** dropdown menu, select **Databases** and then **Sources** from the left-hand menu.

   .. figure:: images/1.png

   .. note::

      You will see a **MariaDB** version of your **USER**\ *##*\ **-FiestaDB** already registered. These database servers are used in the **Containerizing Apps and CI/CD** lab track and are unrelated to this exercise.

#. Click **+ Register > Microsoft SQL Server > Database**.

   .. figure:: images/4.png

#. Fill out the following fields:

   - Select **Not Registered**
   - **Nutanix Cluster** - EraCluster
   - **Name of VM** - USER\ *##*\ -MSSQL-Source
   - **Windows Administrator Name** - Administrator
   - **Windows Administrator Password** - Nutanix/4u
   - **Instance** - MSSQLSERVER

      .. note::

         This field will auto-populate if login using the provided credentials is successful. If the field fails to populate, verify you have typed your credentials properly and that the VM is not blocking communication via Windows Firewall.

   - **Connect to SQL Server Login** - Windows Admin User
   - **User Name** - Administrator

   .. figure:: images/5.png

#. Click **Next**.

#. Fill out the following fields:

   - Under **Unregistered Databases**, select **Fiesta**
   - Under **Register**, select **One Database with One Time Machine**
   - **Database Name in Era** - USER\ *##*\ -FiestaSource (ex. USER01-FiestaSource)

   .. figure:: images/6.png

   Note that multiple databases that are currently running on the source database.

#. Click **Next**.

#. Use the default **Time Machine** settings and click **Register**.

   .. figure:: images/7.png

   Time Machines capture and maintain snapshots and transaction logs of your source databases as defined in the Data Access Management policies (DAM policies) and SLA schedules. A Time Machine is created for every source database that you register with Era.

   Once the registration task has started, you can proceed to the next steps. You do **NOT** need to wait for registration to complete to continue the lab.

Adding A Multi-Cluster Network Profile
++++++++++++++++++++++++++++++++++++++

#. From the **Dashboard** dropdown menu, select **Profiles**.

#. Select **Network** from the left-hand menu and click **+ Create > Microsoft SQL Server > Windows Clusters**.

   .. figure:: images/2.png

   This type of Network Profile is used to define per Cluster network mappings for clustered database VM deployments.

#. Fill out the following fields:

   - **Name** - USER\ *##*\ _MSSQL_CLUSTER (ex. USER01_MSSQL_CLUSTER)
   - Select **Era Cluster**
   - **EraCluster vLAN** - Secondary
   - **Select AWS-Cluster**
   - **AWS-Cluster vLAN** - User VM Network

   .. figure:: images/3.png

#. Click **Create**.

Provisioning A Multi-Cluster Database Server
++++++++++++++++++++++++++++++++++++++++++++

SQL Server AlwaysOn Availability Group (AAG) clusters have many moving parts, and deploying a single cluster can easily take several hours or more. *This should take less than an hour!*

Currently, Era allows you to clone databases directly to an AAG if all members of the AAG cluster are on the same Nutanix cluster. Support for multi-cluster cloning will be delivered in a future Era release.

While you can't directly clone, we can use Era to provision a new multi-cluster AAG across our on-prem and AWS environments and then migrate our data post-provisioning - still saving days of work or potentially thousands in services costs.

#. From the **Dashboard** dropdown menu, select **Databases**.

#. Select **Sources** from the left-hand menu and click **+ Provision > Microsoft SQL Server > Availability Database**.

   .. figure:: images/8.png

#. Fill out the following fields:

   - Select **Create New Cluster**
   - **Windows Cluster Name** - USER\ *##*\ -SQLAG (ex. USER01-SQLAG)
   - Under **Select the Nutanix Clusters to host the Windows Cluster**, select *both* **EraCluster** and **AWS-Cluster**
   - **Network Profile** - Your previously created USER\ *##*\ _MSSQL_CLUSTER profile
   - **Windows Domain Profile** - NTNXLAB

   .. figure:: images/9.png

#. Click **Next**.

#. Fill out the following fields:

   - **Software Profile** - MSSQL_19_SYNCED
   - **Compute Profile** - LAB_COMPUTE

      .. note::

         This is a pre-staged 4 vCPU/5GiB RAM profile intended to minimize memory utilization on the shared clusters. Do **NOT** use the out of the box (OOB) Compute Profiles.

   - **Windows License Key** - *Leave blank*
   - **Administrator Password** - nutanix/4u

      .. note::

         This sets the **local** Administrator password for the provisioned VMs, and is independent from your domain or SQL credentials.

   .. figure:: images/10.png

#. Under **Attributes of individual Database Server VMs**, click **Add** to add a third server to your cluster, and make the following **Nutanix Cluster** selections:

   - **USER**\ *##*\ **-SQLAG-1** - EraCluster
   - **USER**\ *##*\ **-SQLAG-2** - EraCluster
   - **USER**\ *##*\ **-SQLAG-3** - AWS-Cluster

   .. figure:: images/11.png

#. Fill out the following fields:

   - **Server Collation** - *Default*
   - **Database Parameter Profile** - DEFAULT_SQLSERVER_INSTANCE_PARAMS
   - **SQL Server Authentication Mode** - Mixed Authentication
   - **SQL Server User** - sa
   - **Password** nutanix/4u

   .. figure:: images/12.png

   .. note::

      There is no need to select **Grant Access to an Account for Windows/SQL Server Administration** as we are using an account with domain administration privileges.

#. Click **Next**.

#. Under **Backup Preferences**, select **Secondary Only**.

   .. figure:: images/13.png

   SQL 2016 and above supports up to 9 secondary replicas.

   The **Primary** server indicates which host you want the AAG to start on.

   **Auto Failover** allows the AAG to failover automatically when it detects the **Primary** host is unavailable. This is preferred in most deployments as it requires no additional administrator intervention, allowing for maximum application uptime.

   **Availability Mode** can be configured as either **Synchronous** or **Asynchronous**.

      - **Synchronous-commit replicas** - Data is committed to both primary and secondary nodes at the same time. This mode supports both **Automatic** and **Manual Failover**.
      - **Asynchronous-commit replicas** - Data is committed to primary first and then after some time-interval, data is committed to the secondary nodes. This mode only supports **Manual Failover**.

      Due to the significant latency between on-prem and AWS clusters, it doesn't make sense to implement synchronous-commit across the WAN, as this would add 10's of milliseconds to each transaction. The asynchronous-commit copy will instead provide a live database with little, or possibly zero, data loss which can quickly be made to act as the active database in the event of a complete site failure.

   **Readable Secondaries** allows you to offload your secondary read-only workloads from your primary replica, which conserves its resources for your mission critical workloads. If you have mission critical read-workload or the workload that cannot tolerate latency (up to a few seconds), you should run it on the primary.

#. Click **Next**.

#. Fill out the following fields:

   - **Database Name in Era** - USER\ *##*\-FiestaHA\ (ex. USER01-FiestaHA)
   - **Database Name on VM** - USER\ *##*\-FiestaHA\
   - **Size (GiB)** - 10
   - **Database Parameter Profile** - DEFAULT_SQLSERVER_DATABASE_PARAMS
   - **Database Collation** - *Default*

   .. figure:: images/14.png

#. Click **Next**.

#. Change the **SLA** to **DEFAULT_OOB_BRONZE_SLA** to enable continuous data protection.

   .. figure:: images/15.png

   Enabling logs and snapshots to replicate across both sites allows users to provision and update clones of this database on either cluster. The elasticity of the AWS-hosted cluster could allow for more capacity for development or testing versions of this database without disrupting on-prem performance of your production database.

#. Click **Provision**.

#. Click the **The operation to provision USER**\ *##*\ **-FiestaHA has started** link to view progress. Alternatively, select **Operations** from the Era dropdown menu.

   Within the first couple minutes, you should see the VMs being provisioned in parallel to your 2 Nutanix clusters.

   .. figure:: images/16.png

   Once the database servers have been provisioned and registered with Era, Era will fully automate the process of installing the Windows Failover cluster, creating the Always-On Availability Group, joining replicas to the group, and finally creating and registering your database.

   This process will take approximately 30-45 minutes to complete.

   .. figure:: https://media.giphy.com/media/ZFnb8G00YssucZnVvf/giphy.gif

   While you wait, you can proceed to :ref:`db_clustersdam` and then return to this exercise.

Importing Your Database
+++++++++++++++++++++++

Once your **Provision Database** operation has successfully completed, you can import your data into the **USER**\ *##*\ **-FiestaHA** database.

In a production environment, you would follow a manual backup/restore procedure from your source to your destination database. For the sake of conserving lab time, you will import data directly into your destination database by executing a SQL query (as the example database is small).

#. From **Prism Central**, launch the VM console of your **USER**\ *##*\ **-SQLAG-1** VM.

#. Log in using the **NTNXLAB\\Administrator** credentials.

#. Enable **Remote Desktop** for the VM as shown in the screenshot below and then **connect via RDP** to enable you to copy/paste into the VM.

   .. figure:: images/20.png

#. Within your **USER**\ *##*\ **-SQLAG-1** VM, launch **Microsoft SQL Server Management Studio** from the Start menu.

#. Click **Connect** to connect to the local database instance as the currently logged in user.

   .. figure:: images/21.png

#. In the **Object Explorer**, expand **USER**\ *##*\ **-SQLAG-1 > Databases**.

#. Right-click the **USER**\ *##*\ **-FiestaHA** database and select **New Query**.

   .. figure:: images/31.png

#. In the **SQLQuery1.sql** field, copy and paste the following:

   .. literalinclude:: FiestaDB-MSSQL.sql
     :caption: FiestaDB Data Import Script
     :language: sql

#. Click **Execute**.

   .. figure:: images/32.png

..   #. Click **Next**.

   #. Select **SQL Server Native Client 11.0** from the **Data Source** dropdown menu.

   #. Fill out the following fields:

      - **Server Name** - Your USER\ *##*\ -MSSQL-Source VM IP address
      - **Authentication** - Use SQL Server Authentication (as the source database server is not joined the the NTNXLAB domain)
      - **Username** - sa
      - **Password** - Nutanix/1234
      - **Database** - Fiesta

      .. figure:: images/23.png

      .. note::

         You may need to click **Refresh** after entering the **sa** credentials of your source server.

   #. Click **Next**.

   #. Select **SQL Server Native Client 11.0** from the **Destination** dropdown menu. Your local host and **USER**\ *##*\ **-FiestaHA** database should be automatically selected.

      .. figure:: images/24.png

   #. Click **Next**.

   #. Select **Copy data from one or more tables or views** and click **Next**.

   #. Select all tables as shown below.

      .. figure:: images/25.png

   #. Ensure **Run immediately is selected** (Default) and click **Finish > Finish** to begin the copy operation.

#. Close your RDP session.

Testing Failover Using Your Application
+++++++++++++++++++++++++++++++++++++++

Before testing failover, you will need to update the configuration of your Fiesta application to point to your new, highly available database. To simplify this process, your Fiesta application Blueprint includes a **Calm Action** to automate this process. **Actions** are a great option for automating post-deployment tasks for an application, such as scaling in or scaling out.

#. In **Era**, from the **Dashboard** dropdown menu, select **Database Server VMs**.

#. Select **List** from the left-hand menu, and click your **USER**\ *##*\ **-SQLAG** cluster to view its details.

   .. figure:: images/17.png

#. Under **Topology**, take note of the **Always On Availability Group** DNS name (ex. **USER01-SQLAG_AG**). This is a round robin DNS entry providing all available listener IP addresses used to connect to the database from your web server VM.

   .. figure:: images/18.png

#. In **Prism Central**, select :fa:`bars` **> Services > Calm**.

#. Under **Applications**, select your **USER**\ *##*\ **-Fiesta** application.

   .. figure:: images/27.png

#. Under the **Manage** tab, click the **Update DB Config** :fa:`play` icon.

   .. figure:: images/28.png

#. Fill out the following fields:

   - **New DB Name** - **USER**\ *##*\ **-FiestaHA** (ex. USER01-FiestaHA)

      .. note::

         This must match the name of your database as it appears within Era and the SQL Management Studio. The value above assumes you have followed the naming conventions provided in the lab.

   - **New DB Server IP Address** - Your fully qualified **USER**\ *##*\ **-SQLAG_AG** from **Step 3** (ex. USER01-SQLAG_AG.ntnxlab.local)
   - **User Name** - Administrator
   - **Domain** - NTNXLAB
   - **Password** - nutanix/4u

   .. figure:: images/29.png

#. Click **Run**.

   The action will update the **config.js** file on your **USER**\ *##*\ **-FiestaWeb** VM and restart the Fiesta service. This process only takes a few seconds and can be verified in the **Audit** tab.

   .. figure:: images/30.png

#. Verify the connection to your new database was successful by browsing to the IP Address of your **USER**\ *##*\ **-FiestaWeb** VM (ex. http://10.0.0.100) and using the web app to make an update to the database.

   This can be done by clicking **Stores > Add New Store** and filling out the required fields.

   .. figure:: images/33.png

   .. note::

      If you cannot access the web interface this indicates there was something wrong with your DB connection.

      Open a VM console to your **USER**\ *##*\ **-FiestaWeb** VM (U\:root P\:nutanix/4u) and run ``cat Fiesta/config/config.js`` to view your DB configuration. Is the database name correct? Are you using the FQDN as **DB_HOST_ADDRESS**?

      You can re-run the Calm action to easily make any fixes and restart the Fiesta service.

#. In **Prism Central**, power off your **USER**\ *##*\ **-SQLAG-1** VM running on your on-premises cluster.

   .. figure:: images/34.png

#. Immediately begin refreshing your Fiesta web interface.

   You should experience less than a minute of downtime while the Availability Group *automatically* fails over to **USER**\ *##*\ **-SQLAG-2**. When the site returns, observe that your newly added store data has been preserved due to the synchronous configuration of your on-premises database servers.

#. Return to **Prism Central** and power off your **USER**\ *##*\ **-SQLAG-2** VM, leaving no local copies of your database.

   .. figure:: images/35.png

#. Open the VM console for your **USER**\ *##*\ **-SQLAG-3** VM and login using the **NTNXLAB\\Administrator** credential.

#. Open the **Microsoft SQL Server Management Studio** from the Start menu.

#. Click **Connect** to connect to the local database instance as the currently logged in user.

#. In the **Object Explorer**, expand **Always On Availability > Availability Groups**. Right-click **USER**\ *##*\ **-SQLAG_AG** and select **Failover** to activate the asynchronous replica database.

   .. figure:: images/36.png

#. Click **Next**.

#. Select your remaining SQL server as the **New Primary Replica**.

   .. figure:: images/37.png

#. Click **Next**.

#. Accept the data loss warning.

   .. figure:: images/38.png

#. Click **Next > Finish** to complete the failover and bring **USER**\ *##*\ **-FiestaHA** back online.

#. Click **Close**.

#. Return to **Era > Database Server VMs > List > USER**\ *##*\ **-SQLAG** and verify that the database is still shown as available.

   .. figure:: images/40.png

   The Fiesta application will not immediately begin working following bringing the database back online, as the **USER**\ *##*\ **-SQLAG_AG.ntnxlab.local** DNS entry used by the web server VM to connect to the database will still attempt to connect to the on-premises listener IP.

#. Optionally, you can update your Fiesta configuration again using the same **Calm Action** to point to your 10.210.X.X listener IP address, as shown in the Topology view in Era.

   In a production scenario, a proper load balancer would be used across both sites to re-direct to whichever SQL listener IP is associated with the primary replica of the database. Additionally, you would also scale the web tier across sites and similarly leverage a load balancer for connectivity.

.. raw:: html

    <H1><a href="http://lookup.ntnxworkshops.com/" target="_blank"><font color="#B0D235"><center>Click Here To Submit Validation Request</center></font></a></H1>

Takeaways
+++++++++

- Nutanix Clusters provides capacity for instant lift and shift of database workloads to the cloud

- Era's multi-cluster support, combined with Nutanix Clusters, allows you to provision highly available databases across clouds in minutes, without deep SQL Server administration knowledge
