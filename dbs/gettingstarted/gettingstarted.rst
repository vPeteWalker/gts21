.. _snow_gettingstarted:

---------------
Getting Started
---------------

This lab track is designed to showcase Nutanix as an ideal platform for delivering a true hybrid cloud for Database workloads, leveraging both the flexibility of AWS and Nutanix Clusters and new multi-cluster support in Nutanix Era.

As Party Time, Excellent Inc. seeks to modernize their sales and services offerings, their database management challenges are holding them back from delivering the kind of availability and performance required.

Current SQL Server deployments inside of PTE do not follow Microsoft best practices, and contain overcrowded database servers, hosting databases for several applications, often from a single vDisk. This approach has caused availability issues where maintenance or failure has taken several applications offline, and "noisy neighbor" performance issues across apps. To make matters worse, critical applications such as PTE's retail inventory management application, Fiesta, is hosted on a single instance VM, providing no high availability in the event of failure.

Ideally, PTE would be able to separate their overcrowded database servers, but they lack the on-premises capacity. Additionally, they have concerns about keeping up to date with the latest versions of SQL Server and patching if they were to host each database on its own server - not to mention how to monitor all of those additional servers.

.. .. raw:: html

   <strong><font color="red">Due to a late emerging issue with the SQL Server patching lab and the way the GTS clusters were staged, the patching lab needed to be removed. Stay tuned for Star Wars X: Return of the Patching Lab, coming to a multi-cluster Era bootcamp near you!</font></strong><br>

Your Environment
++++++++++++++++

To let you experience the most fun and interesting parts of the lab, as well as accommodate the large number of simultaneous users, multiple components have already been staged for you. *Read on to learn more!*

.. raw:: html

   <br><center><img src="https://github.com/nutanixworkshops/gts21/raw/master/dbs/gettingstarted/images/env.png"><br><i>vGTS 2021 Hybrid Cloud Database Management Lab Environment</i></center><br>

Clusters on AWS
...............

A single node Nutanix cluster running in AWS has already been provisioned and registered to your on-premises Prism Central instance.

.. figure:: images/0.png

Source Database and App Servers
...............................

Using a Calm Blueprint, each on-premises (HPOC) cluster has been pre-staged with the following VMs for each **USER**:

   .. figure:: images/1.png

   - **USER**\ *##*\ **-MSSQL-Source**

      A single instance SQL Server 2016 database server on Windows Server 2019, containing the following 3 databases: **Fiesta, SampleDB, tpcc**. Each of these databases will be used in the lab track.

   - **USER**\ *##*\ **-FiestaWeb**

      A CentOS 7 VM running a NodeJS-based web application used to access the Fiesta database. The Fiesta app is a simple example of a web application for performing inventory management for party goods supply stores.

      You can validate your Fiesta application is capable of reaching your source database by browsing to \http://*USER##-FiestaWeb-IP-ADDRESS*\ /

   .. figure:: images/3.png



Nutanix Era
...........

Each shared environment has been pre-staged with a Nutanix Era server, configured as follows:

   - Era multi-cluster support enabled, with both **EraCluster** (HPOC) and **AWS-Cluster** Nutanix clusters registered. When enabling multi-cluster, an Era Cluster Agent VM (4vCPU/4GB) is automatically deployed to each registered cluster, including the cluster running the Era server.

      .. figure:: images/4.png

      The Era Agent VM is responsible for managing, scheduling, and executing database operations on its cluster, offloading these operations and relaying status back to the parent Era server VM.

   - **Era Managed** networks were configured for a subset of the available IP range for both **EraCluster** (HPOC) and **AWS-Cluster**. While external IPAM solutions (including AHV IPAM) can be used for single instance database deployments, Era must control the IP pool for provisioning highly available database clusters, such as SQL Always-On Availability Groups.

      .. figure:: images/6.png

   - **MSSQL_19_SYNCED** Software Profile pre-created using a vanilla Windows Server 2019/SQL Server 2019 VM, and replicated across both **EraCluster** and **AWS-Cluster**.

      Software Profiles are templates that include the database engine installation and the host operating system, and are used for provisioning and cloning operations. This template exists as a hidden disk image on your Nutanix storage.

..   - **MSSQL_19_USER**\ *##* Software Profiles pre-created using the same VM, but located only on **AWS-Cluster**.

      .. figure:: images/5.png

      You will each require your own Software Profile to complete the :ref:`db_patching` exercise. These individual profiles were not replicated across clusters to reduce time and bandwidth consumption during the lab staging process (*~19GiB per profile \* Hundreds of Users, yikes!*).
