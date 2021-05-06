.. _dbs_sqlmonitoring:

------------------------------------------
Application Monitoring with Prism Ultimate
------------------------------------------

For years, Prism Pro has enabled smart automation to our customer’s daily IT operations. With Prism Ultimate, we expand this smart automation and intelligent learning to the application and services layers. The typical operations workflow is a continuous cycle of monitoring, analyzing and taking action where necessary. Prism Pro mirrors traditional IT Admin's workflows to improve operations efficiency and Prism Ultimate combines that with full-stack visibility. With Prism Ultimate, IT Admins are able to connect insights from application machine data to automate this typical flow using the power of the machine learning engine X-FIT and the X-Play automation engine.

   .. figure:: images/1.png

In this lab you will learn how Prism Ultimate can help IT Admins monitor, analyze and automatically act when a SQL Server's performance is impacted. You will also see how you can discover applications running on your cluster with Prism Ultimate.

SQL Server Monitoring with Prism Ultimate
+++++++++++++++++++++++++++++++++++++++++

Prism Ultimate licensing includes the SQL Server monitoring pack, which allows IT admins to understand how infrastructure may impact applications and vice versa. This is an agentless solution that gives visibility into databases, queries, SQL metrics and applies the X-FIT behavior learning and anomaly detection capabilities.

#. Within Prism Central, click on :fa:`bars` **> Virtual Infrastructure > VMs**.

#. Select your **USER**\ *##*\ **-MSSQL-Source** VM and note the IP Address.

   .. figure:: images/3.png

#. Within Prism Central, click on :fa:`bars` **Operations > Integrations**.

#. If prompted, click **Get Started**.

   .. note::

      This is a one-time operation that may have already been completed by another user sharing the cluster.

#. Click **Configure Instance**.

   .. figure:: images/4.png

#. Select **Microsoft SQL Server** from the **External Entity Type** dropdown menu.

#. If prompted that **Nutanix Collector is not enabled**, select **I have increased PC VM's Memory and vCPU** and click **Enable**.

   Nutanix Collector is the service that runs within PC to gather statistics from SQL Server and vCenter entities.

   .. figure:: images/16.png

   .. note::

      This is a one-time operation that may have already been completed by another user sharing the cluster.

#. Fill out the following fields to add your SQL Server:

   - **External Entity Type** - Microsoft SQL Server
   - **Microsoft SQL Server Host** - Your USER\ *##*\ -MSSQL-Source IP Address
   - **Microsoft SQL Server Port** - 1433
   - **Username** - sa
   - **Password** - Nutanix/1234

   .. figure:: images/5.png

#. Click **Test Connection**.

   .. note::

      If the connection test fails, verify you have the correct IP and your VM is powered on. Additionally verify the Windows Firewall is disabled on your **USER**\ *##*\ **-MSSQL-Source** VM (or at least allows TCP 1433).

#. After a successful test, click **Save**.

   Once complete, your SQL Server will be listed under **External Entity Instances** as shown below.

   .. figure:: images/6.png

#. Click on the IP Address of the server, under the *Name* column, to access the summary view.

   .. figure:: images/7.png

#. Select **Queries** from the left-hand menu to access the table of queries executed against the server.

   You can easily sort by **Average Execution Time** to identify problematic, long running queries, **Execution Count** to identify common queries and their performance, as well as the most recently executed queries.

   .. figure:: images/8.png

#. Select **Metrics** from the left-hand menu.

   As SQL Monitoring has just been configured for this host, you will not be able to view historical data, which will populate over time.

   .. figure:: images/9.png

   Based on the example above, you can see that Prism Ultimate has identified a **CPU Utilitization** anomaly, based on its machine learned performance baseline. In additional to typical performance metrics, you can see other key application metrics such as active connections, buffer page life expectancy, SQL compilations rate, etc.

   Next you will test Prism's ability to raise alerts based on application metrics by applying artificial load to your **USER**\ *##*\ **-MSSQL-Source** database.

#. Scroll to the **Buffer Pool Size** metric and select **Actions > Alert Settings**.

   .. figure:: images/11.png

   .. note::

      Users have reported an inconsistent issue where Alert Settings may not appear in the dropdown menu. Refreshing the page or returning to the list of **External Entity Instances** and trying again resolves the issue. It may take multiple attempts. Standing on one leg, rubbing your stomach, while patting your head also seems to help.

      The issue also appears to affect Firefox more often than Chrome.

#. Fill out the following fields:

   - **Policy Name** - USER\ *##* - SQL Buffer Alert
   - **Static Threshold > Alert Critical if** - >= 100 mib
   - **Trigger alert if conditions persist for** - 0 Minutes

   .. figure:: images/12.png

#. Click **Save**.

Triggering Prism SQL Server Alert
+++++++++++++++++++++++++++++++++

#. Within Prism Central, click on :fa:`bars` **Virtual Infrastructure > VMs**.

#. Select your **USER**\ *##*\ **-MSSQL-Source** VM and **Launch Console**.

#. Log in using the following credentials:

   - **Username** Administrator
   - **Password** Nutanix/4u

   We will now artificially generate the required usage to activate the alert we previously created. To do so, we will be executing a PowerShell script, which utilizes a program called HammerDB.

#. Using **File Explorer**, navigate to **Local Disk(C:) > Program Files > HammerDB-3.3**.

#. Right-click on the file *workload.ps1*, and select **Run with Powershell**.

      .. figure:: images/13.png

#. It may take up to 5 minutes for the activity generated by the PowerShell script to meet the requirements for the alert.

#. The alert will appear in **Prism Central** under **Activity > Alerts**, or by clicking the :fa:`bell` icon in the upper right hand corner.

      .. figure:: images/15.png

   If you were waiting on your SQL Server to provision in the :ref:`db_clustersdam` exercise, you should now be able to return and complete the exercise.

.. raw:: html

    <H1><a href="http://lookup.ntnxworkshops.com/" target="_blank"><font color="#B0D235"><center>Click Here To Submit Validation Request</center></font></a></H1>

Takeaways
+++++++++

- Prism Ultimate bridges the gap between infrastructure, applications, and services. It satisfies IT OPS processes ranging from intelligent detection, to automated remediation.

- Prism Ultimate allows the admin to understand the relationship between their applications and infrastructure, with broader visibility and intelligent insights learning.

- X-Play can be used seamlessly with the application data monitored via Prism Ultimate to build smart automation that can alert and remediate issues both on the infrastructure and on applications.
