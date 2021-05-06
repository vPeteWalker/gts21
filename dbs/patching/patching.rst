.. _db_patching:

----------------------------
Patching SQL Server with Era
----------------------------

As the org begins to split up databases across multiple servers and sites to improve performance, availability, and maintenance, policy based patching becomes critical to keep database servers up to date. In this exercise, you will create and apply a SQL Server patch to update your VMs from SQL Server 2016 RTM (15.0.2000.5) to Cumulative Update 4 (15.0.4033.1) via Era Software Profiles.

Creating a Software Profile Version
+++++++++++++++++++++++++++++++++++

Software Profile Versions are created in Era to support patching of SQL Server database server instances. A Software Profile Version can be created simply by uploading a SQL Server update executable. The SQL Server update can then be used to patch other database server VMs or when provisioning new database server VMs with the updated Software Profile.

   .. note::

         The Cumulative Update 4 (CU4) patch has been pre-staged within the lab environment.

         See `KB3177312 - SQL Server 2019 Build Versions <https://support.microsoft.com/en-us/topic/kb4518398-sql-server-2019-build-versions-782ed548-1cd8-b5c3-a566-8b4f9e20293a>`_ for additional patch and download information.

#. Within Era, select **Profiles** from the drop-down menu.

#. Select **Software** from the left-hand menu and click *your* **MSSQL_19_USER**\ *##* profile used to provision your 2019 SampleDB VM.

   .. figure:: images/1.png

   Currently you should only see the base (1.0) version of the profile.

#. Click **+ Create**.

#. Fill out the following fields:

   - **Name** USER\ *##*\ -SQL2019_CU4
   - **Patch File Location** - File Share
   - **File Share** - ``\\10.42.194.11\workshop_staging\era\SQLServer\MSSQL_Patches\sqlserver2019-kb4548597-x64.exe``
   - **User Name** - Refer to **HPOC Frame/VPN Username** in :ref:`clusterdetails`
   - **Password** - Refer to **HPOC Frame/VPN Password** in :ref:`clusterdetails`

   .. figure:: images/2.png

   .. note::

      As the Cumulative Update 4 patch is ~550MB, it makes much more sense to load from an internal file server than trying to download the patch to your local machine and re-upload to Era. If you find yourself doing this, stop. Just stop.

#. Click **Create**.

   .. note::

      Any Software Profile you create must be of a higher version than the previous version, otherwise that Software Profile will fail to create. For example, if you create a profile for SP1-CU9, and then attempt to create another for SP1-CU3, it will fail.

   The **Create Software Profile Version** operation should complete in 1.5 to 3 minutes.

Publishing a Software Profile Version
++++++++++++++++++++++++++++++++++++++

After profile creation is successful, you must publish the profile to make the profile version visible to other Era users.

#. Within Era, select **Profiles** from the drop-down menu.

#. Select **Software** from the left-hand menu and click *your* **MSSQL_19_USER**\ *##* profile.

#. Select the **USER**\ *##*\ **-SQL2019_CU4** (2.0) profile version and click **Update**.

#. Under **Status**, select **Published**, and click the disclaimer indicating that a recommendation to upgrade for all databases using an earlier version of the profile will appear.

   .. figure:: images/3.png

#. Click **Next > Update**.

Patching a SQL Server Database Server VM
++++++++++++++++++++++++++++++++++++++++

Perform the following procedure to apply updates from the available software profile versions to a provisioned/registered database server VM.

#. Within Era, select **Database Server VMs** from the drop-down list.

#. Select **List** from the left-hand menu and click the **USER**\ *##*\ **-SampleDBVM** you had previously cloned from your SampleDB source.

   As indicated during publishing, **Software Profile Version** shows your newly added profile version as a recommendation.

   .. figure:: images/4.png

#. Click **Update**.

   If you have multiple versions available, you could choose your desired Software Profile Version from the dropdown menu.

#. Specify your **Database Server VM Name** as instructed by the dialog to confirm the request to update.

   .. figure:: images/5.png

#. Click **Update**.

   Monitor the progress in **Operations**.

#. Upon completion, you can validate the patch process was successful, by closing and re-opening MS SQL Server Management Studio, and observing the server version has been upgraded from the RTM build version (**15.0.2000.5**) to the CU4 build version **15.0.4033.1**.

   .. figure:: images/6.png

.. raw:: html

    <H1><a href="http://lookup.ntnxworkshops.com/" target="_blank"><font color="#B0D235"><center>Click Here To Submit Validation Request</center></font></a></H1>

Takeaways
+++++++++

We've demonstrated the process of creating just a single Software Profile, and utilizing that to apply a single patch, to a single SQL server. Let's imagine the time and effort we've saved using Era for just this example shown here. Just for fun, think of the amount of time you think that might take. It's ok, just take your best guess. Got it? Alright.

What if we were to expand this example to a handful of servers? What about dozens? More? Now consider that Microsoft released eight Cumulative Updates in the span of just 11 months from releasing SQL Server 2019.

Remember that guess you made? Alright, now take it and multiply it by even a handful of SQL Servers. Then consider taking that amount of time, and spending it just on patching SQL Servers once every ~6 weeks on average.

Think of what else you could be doing to help your company with that time.

This is only one of many powerful features Nutanix Era brings to the table.
