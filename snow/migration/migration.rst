.. _snow_migration:

------------------------------
Cross-Cluster DR and Migration
------------------------------

Using the already configured Data Protection Plan for your self-service provisioned VMs, and Nutanix Leap runbook orchestration capabilities, you can demonstrate how PTE can achieve Disaster Recovery for their active/active datacenter deployment - and also how this same approach can be leveraged to migrate workloads across different clouds.

In this scenario, we'll target a VM that was provisioned on your AWS cluster to migrate back on-premises in order to reduce the latency between the VM and a backend database.

.. note::

   As of AOS 5.19, it is also possible to perform VM Live Migration across multiple Nutanix clusters. This feature requires synchronous replication between clusters, meaning that round trip latency needs to be very low (<5ms RTT). Additionally, the clusters must be in separate Nutanix Availability Zones, each with their own Prism Central instance. This is to ensure management plane availability in the result of a site failure.

Creating A Recovery Plan
++++++++++++++++++++++++

#. In **Prism Central**, select :fa:`bars` **> Policies > Recovery Plans**.

#. Click **Create Recovery Plan**.

#. Fill out the following fields:

   - **Recovery Plan Name** - USER\ *##*\ -DR (ex. USER01-DR)
   - **Primary Location** - Local AZ
   - **Recovery Location** - Local AZ
   - **Primary Clusters** - AWS-Cluster
   - **Recovery Clusters** - Your *PHX###* Cluster

   .. figure:: images/1b.png

#. Click **Next**.

#. Click **+ Add Entities** to define which VMs should be included in the Recovery Plan.

#. Observe that only VMs with recovery points shared between the Primary and Recovery clusters are shown. Select your *Initials*\ -**CentOS####** VM and click **Add**.

   .. figure:: images/2.png

#. Select your VM and observe the available options.

   .. figure:: images/3.png

   AHV Recovery Plans, also referred to as Leap, make it incredibly simple to manage multi-VM failovers, including power-on sequences, delays, and executing scripts on VMs to perform tasks such as updating configuration files or starting services.

#. Click **Next** to begin configuring network mappings between the two sites.

   .. figure:: images/4.png

   Each Recovery Plan allows you to map both **Production** and **Test** networks. Failover tests can be performed to evaluate recovery plans without taking down production VMs by provisioning VM clones to an isolated network.

#. Fill out the following fields:

   - **AWS-Cluster (Primary) > Production** - User VM Network
   - **AWS-Cluster (Primary) > Test Failback** - *Leave blank*
   - **POC### (Recovery) > Production** - Secondary
   - **POC### (Recovery) > Test Failback** - *Leave blank*

   .. figure:: images/5.png

   Observe the default behavior for mapping VM IPs is to match the 4th octet value on the recovery location, making scripting and other updates predictable. Additionally, you can specify custom static IP mapping on a per-VM basis for VMs running Nutanix Guest Tools.

#. Click **Done > Continue** to save your Recovery Plan.

   .. note::

      You can ignore any warnings regarding **Incomplete Network Mapping**.

Executing A Failover
+++++++++++++++++++

#. After you are returned to the list of available **Recovery Plans**, right-click your **USER**\ *##*\ **-DR** plan and select **Failover** to begin your migration.

   .. figure:: images/6b.png

#. Fill out the following fields:

   - **Failover Type** - Planned Failover
   - **Failover From > Cluster** - AWS-Cluster
   - **Failover To > Cluster** - Your *PHX###* Cluster

   Under **Recovery Status** you should observe the plan discover all VMs that would be impacted by the failover. A planned failover is the suitable approach for our migration as this will ensure the VM is gracefully powered off and a final recovery point taken and synced between sites.

   .. figure:: images/7.png

#. Click **Failover**.

#. If prompted about an **Unsupported License** warning, click **Execute Anyway**.

   If you receive a **Network Validation** warning, as shown below, this means the likely the matching IP on your Recovery cluster is already in use and can't be reserved for your VM on failover. *This will result in the VM booting on the Recovery cluster without a NIC and is expected.* In a production environment you would have a dedicated network space reserved for site to site failovers that were not already populated, eliminating the chance of IP collisions.

   .. figure:: images/15.png

   Because the HPOC cluster is heavily populated with VMs to accommodate all the labs, it is likely you will receive this warning.

   .. note::

      Another way to address this is to set up custom VM IP mappings, but this is outside of the scope of the lab.

#. Click on your **USER**\ *##*\ **-DR** plan, and select the **Tasks > Failover** tabs to view the live progress.

   .. figure:: images/8.png

   Due to the lack of proper licensing in the lab environment, it is expected that the **Validating Recovery Plan** task will fail.

   .. note::

      For VMs with aggressive change rates or site-to-site connections with poor bandwidth that could result in extending downtime for the VM to allow the migration to take place, another approach to migration would be to use the **Nutanix Move** tool.

      Move is a Nutanix supported tool that is typically used to migrate between hypervisors, but in the case of this AHV to AHV migration, is capable of taking and syncing snapshots continuously to this migration destination until a minimal cutover window is possible, and can be executed at the administrator's discretion.

Validating the Migration
++++++++++++++++++++++++

#. Once the Recovery Plan has completed, click the **Summary** tab and click the latest **Failover** report to view the full details of the operation.

   .. figure:: images/14.png

#. Return to **Prism Central > Virtual Infrastructure > VMs** and select your **USER**\ *##*\ **-CentOS####** VM. Observe that it is now running on your **POC###** cluster.

   .. figure:: images/9.png

      If you have been impacted by the **Network Validation** warning during failover, your migrated VM will not have a NIC assigned. Update the VM configuration and add a NIC on the **Secondary** network.

#. Under **Recovery Points > Current Protection Status**, observe that your data protection policy is still active, and snapshots are now scheduling to be replicated back to your **AWS-Cluster**, allowing for future migrations or DR events to seamlessly transition back to the public cloud.

   .. figure:: images/10.png

#. Log into **Prism Central** as your **operator**\ *##*\ **@ntnxlab.local** account and verify your user still has the ability to manage their assigned resources post-migration.

   .. figure:: images/11.png

#. SSH into your VM or click **Launch Console** and re-attempt your pings to **USER**\ *##*\ **-FiestaWeb** and **USER**\ *##*\ **-MSSQL-Source** IP addresses. You should observe that you are still isolated from **USER**\ *##*\ **-FiestaWeb** and you now have minimal latency to connect to your **USER**\ *##*\ **-MSSQL-Source** database - goal achieved!

   .. figure:: images/12.png

.. raw:: html

    <H1><a href="http://lookup.ntnxworkshops.com/" target="_blank"><font color="#B0D235"><center>Click Here To Submit Validation Request</center></font></a></H1>

Takeaways
+++++++++

- Native data replication functionality and Nutanix Leap allow you to easily migrate workloads between clouds with minimal downtime

- The same approach can be used to address Disaster Recovery in the event of site failure.

- Through the Nutanix API, you could further automate migrations based on alert or cost triggers
