.. _snow_preparingenv:

-------------------------------
Preparing Policies and Projects
-------------------------------

With the additional infrastructure capacity you've unlocked with Nutanix Clusters, one of the goals is to provide users with the ability to request and operate their own VMs and applications. Depending on the user and/or application, PTE needs to ensure that VMs are properly protected for backup and DR purposes, as well as properly secured on the network from the time of creation.

In this exercise, you'll configure example policies in Prism Central for both data protection and microsegmentation that can be applied to apps and VMs. The goal is to have these policies in place prior to provisioning your VMs, so they can be applied and enforced as VMs are created through self-service.

Additionally, you'll configure a Calm project and Blueprint to use as your first self-service VM offering.

Configuring Data Protection
+++++++++++++++++++++++++++

In this exercise you will build a policy to replicate hourly snapshots between your primary and AWS clusters, based on category assignment.

A Prism **Category** is a key value pair. Categories are assigned to entities (such as VMs, Networks, or Images) based on some criteria (Location, Production-level, App Name, etc.). Policies can then be mapped to those entities that are assigned a specific category value.

#. Refer to :ref:`clusterdetails` for your **Prism Central** IP and **admin** credentials.

#. In **Prism Central**, select :fa:`bars` **> Virtual Infrastructure > Categories**.

   .. figure:: images/1.png

#. Click **New Category** and fill out the following:

   - **Name** - USER\ *##*-DP (ex. USER01-DP)
   - **Purpose** - Used for VM data protection and replication policy assignment.
   - **Value** -
      - Bronze
      - Silver
      - Gold

   .. figure:: images/3.png

#. Click **Save**.

#. In **Prism Central**, select :fa:`bars` **> Policies > Protection Policies**.

#. Click **Create Protection Policy** and fill out the following:

   .. note::

      If you are prompted that **Leap is not enabled on Local AZ**, click **Enable > Enable > Enable** to enable the feature. This is a non-disruptive, one-time operation within **Prism Central**. You can then click the **X** to close the warning dialog while **Leap** is enabled in the background.

      .. figure:: images/23.png

   - **Policy name** - USER\ *##*-Bronze (ex. USER01-Bronze)
   - **Primary Location > Location** - Local AZ
   - **Primary Location > Cluster** - AWS-Cluster
   - Click **Save**
   - **Recovery Location > Location** - Local AZ
   - **Recovery Location > Cluster** - *Your POC### Cluster*
   - Click **Save**

   .. figure:: images/5.png

   An **Availability Zone** in Nutanix is what one instance (single or multi-VM) Prism Central manages as a fault domain. For large sites, having a dedicated instance of the management plane for the site makes sense - but this approach would become very resource intensive for managing several smaller sites. As of AOS 5.17, Nutanix allows for replication and failover within the same AZ, as seen in this lab environment.

#. Click **+ Add Schedule** and fill out the following:

   - **Protection Type** - Asynchronous
   - **Take Snapshot Every** - 1 Hour(s)
   - **Retention Type** - Linear
   - **Retention on Local AZ : AWS-Cluster** - 5 Recovery Point(s)
   - **Retention on Local AZ : POC### Cluster** - 5 Recovery Point(s)
   - Select **Reverse retention for VMs on recovery location**

   .. figure:: images/6.png

   Enabling reverse retention will allow bi-directional replication to take place between specified sites, reducing the number of policies needed to be managed for an active/active datacenter configuration.

#. Click **Save Schedule**.

#. Click **Next**.

#. Under **Categories**, select your **USER##-DP : Bronze** value and click **Add**.

   .. figure:: images/7.png

   Observe that there are not currently any VMs on either cluster with that assigned category value. VMs will be provisioned as part of a later exercise and inherit this policy based on being assigned the **USER**\ *##*\ **-DP : Bronze**

#. Click **Create**.

   .. note::

      Optionally, you can create additional policies for Silver and Gold, using the respective category values. For example, a Gold policy could provide Asynchronous snapshots every 5 minutes.

.. _assign_categories:

Configuring Network Isolation
+++++++++++++++++++++++++++++

Similar to the previous exercise, you'll map a microsegmentation policy to specific VM categories. The purpose of the microsegmentation policy is to prevent non-production VMs from communicating with your production webserver VMs.

#. Select :fa:`bars` **> Virtual Infrastructure > VMs**

#. Click **Filters**. Under **Name**, specify your *USER##* lab ID to search for pre-staged VMs.

   .. figure:: images/4.png

   You'll find a CentOS webserver, **USER**\ *##*\ **-FiestaWeb**, running a Node-based inventory management application, and a Microsoft SQL database, **USER**\ *##*\ **-MSSQL-Source** storing its associated data.

   You can view the web interface of the application by opening \http://<*USER##-FiestaWeb-VM-IP*>.

   .. note::

      Ignore the Fiesta deployment with alternate VM names, as these are used in other GTS labs.

   .. note::

      If you have already completed the **Hybrid Cloud Database Management** lab track, you may not be able to access your Fiesta web front end as it is connected to your AAG database. Inability to connect to the app will not impact this lab, you can proceed.

#. Right-click your **USER##-FiestaWeb** VM and select **Manage Categories**.

   .. figure:: images/8.png

   .. note::

      When right-clicking, you may need to scroll down to view all available actions. Alternatively, you can select the VM and click the **Actions** menu toward the top of the screen.

   As these VMs were provisioned as part of a Calm Blueprint, you will observe that they already have multiple categories automatically applied.

#. In the **Search** field, specify the **Environment: Production** category and click :fa:`plus-circle` to add it.

#. Search for the **User** category and select the pre-staged **User:** *##* value (NOT one your **USER**\ *##*\ **-DP** values) based on your :ref:`clusterdetails` assignment.

   .. figure:: images/9.png

#. Click **Save**.

#. Repeat this process to add *ONLY* the **Environment: Production** category to your **USER##-MSSQL-Source** VM.

   .. raw:: html

      <strong><font color="red">Do NOT add the User:## category to this VM!</font></strong><br>

#. In **Prism Central**, select :fa:`bars` **> Policies > Security**.

#. Click **Create Security Policy**.

   Nutanix Flow is capable of modeling and enforcing more sophisticated application policies that whitelist specific incoming, outgoing, and intra-app communications based on IPs, ports, protocols, or Prism categories, but we will use this simple example to demonstrate the ability for policies to follow VMs in an environment regardless of underlying cluster or network.

#. Select **Isolate Environments** and click **Create**.

   .. figure:: images/10.png

#. Fill out the following fields:

   - **Name** - *USER##*-IsolateEnv (ex. USER01-IsolateEnv)
   - **Purpose** - Isolate Dev and Prod USER:*##* VMs
   - **Isolate this category** - Environment:Production
   - **From this category** - Environment:Dev
   - Select **Apply the isolation only within a subset of the datacenter**
   - Specify **User:**\ *##*
   - **Select a Policy mode** - Enforce

   .. figure:: images/11.png

   .. note::

      The **Apply the isolation only within a subset of the datacenter** functions like an **AND** operator, ensuring only VMs tagged as both Production and User## will be isolated from VMs tagged as both Dev and User##. This allows for more fine-grained application of policy.

#. Click **Save and Enforce**.

   If you select your newly created policy, you'll observe that no traffic has yet been discovered, as there are currently no VMs assigned to Environment:Dev and your user designation. This will occur as part of the self-service provisioning process.

.. _create_project:

Creating A Calm Project
+++++++++++++++++++++++

Nutanix Calm allows you to build, provision, and manage your applications across both private (AHV, ESXi) and public cloud (AWS, Azure, GCP) infrastructure.

In order for non-infrastructure administrators to access Calm, allowing them to create or manage applications, users or groups must first be assigned to a **Project**, which acts as a logical container to define user roles, infrastructure resources, and resource quotas. Projects define a of set users with a common set of requirements or a common structure and function, such as a team of developers collaborating on the Fiesta application.

#. In **Prism Central**, select :fa:`bars` **> Services > Calm**.

#. Select **Projects** from the left-hand toolbar and click **+ Create Project**.

   .. figure:: images/12.png

#. Specify **USER**\ *##*\ **-Project** (ex. USER01-Project) as your **Project Name**.

#. Under **Users, Groups, and Roles**, click **+ User** and fill out the following:

   .. note::

      If **+ User** is greyed out, refresh Calm. The **NTNXLAB.local** profile is already configured in Prism Central, but this issue has occurred (rarely) in testing.

   - **Name** - operator\ *##*\ @ntnxlab.local (ex. operator01@ntnxlab.local)
   - **Role** - Operator
   - Click **Save**

   .. figure:: images/13.png

   The purpose of assigning an individual user is simply to limit visibility of other projects in the shared lab environment. In a production environment you would likely be mapping multiple AD Security Groups to specific roles for each project.

#. Under **Infrastructure**, click **Select Provider > Nutanix**.

#. Click **Select Clusters & Subnets**.

#. Specify both your **AWS-Cluster** and **POC###** clusters. As shown in the screenshot below (We know, we're telling you to look at a screenshot for information), select the **User VM Network** and **Secondary** subnets.

   .. figure:: images/14.png

#. Click **Confirm**.

#. Select the :fa:`star` icon to mark the **AWS-Cluster** network as the default and click **Save & Configure Environment**.

   .. figure:: images/15.png

   .. note::

      You **DO NOT** need to complete the **Environment** configuration as you will not be using Marketplace Blueprints in the upcoming exercises.

Uploading A Calm Blueprint
++++++++++++++++++++++++++

A Blueprint is the framework for every application that you model by using Nutanix Calm. Blueprints are templates that describe all the steps that are required to provision, configure, and execute tasks on the services and applications that are created. A Blueprint also defines the lifecycle of an application and its underlying infrastructure, starting from the creation of the application to the actions that are carried out on a application (updating software, scaling out, etc.) until the termination of the application.

You can use Blueprints to model applications of various complexities; from simply provisioning a single virtual machine to provisioning and managing a multi-node, multi-tier application.

For the purposes of this exercise, you will upload an existing Blueprint of a single VM application deployment. Within the customer environment, this Blueprint could represent a pre-configured build tools envrionment for a developer.

#. `Download the Single VM CentOS Blueprint by right-clicking here and saving. <https://raw.githubusercontent.com/nutanixworkshops/gts21/master/snow/plugins/CentOS%20VM.json>`_

#. From the left-hand toolbar in **Calm**, select **Blueprints**.

   .. figure:: images/16.png

#. Click **Upload Blueprint** and select the **CentOS VM.json** file downloaded in Step 1.

#. Update the **Blueprint Name** to include your **USER**\ *##* and select the Calm Project you created in the previous exercise.

   .. figure:: images/17.png

#. Click **Upload**.

   Before the Blueprint can be used, the networks, disk images, and credentials must be configured for your environment. Additionally, you will incorporate the categories associated with your data protection and network isolation policies.

#. Within your **CentOS VM** Blueprint, click **VM Details**.

#. Select the **Cloud** dropdown and observe that, in this environment, Nutanix AHV is the only option.

   While Calm provides the ability to define deployment requirements for multiple different cloud providers within a single Blueprint, one of the key advantages of Nutanix Clusters is being able to utilize a single configuration (Nutanix AHV) regardless of whether the app is being provisioned on-premises or in your elastic, public cloud hosted cluster.

#. Click **VM Configuration**.

   Here you'll see the specifications for the VM being provisioned. Observe that a Calm macro, or variable, is being used to customize the VM name by prepending the user's initials.

#. Click the **Runtime** icon for both **vCPUs** and **Memory** to allow for customization of these values at the time of launch.

   We will use this in a later exercise to allow a ServiceNow administrator to create multiple catalog offerings from the same Blueprint.

   .. figure:: images/18.png

#. Under **Disks > Disk (1) > Image** select **CentOS7.qcow2** to clone from the existing disk stored within the Prism Image Service.

   .. figure:: images/19.png

#. Under **Categories**, add the following categories to assign your data protection and network isolation policies during VM creation:

   - **Environment: Dev**
   - **USER: ##**
   - **USER##-DP: Bronze**

   .. figure:: images/20.png

   .. note::

      While Calm supports category customization at runtime, this functionality is not yet supported in the Calm Plug-in for ServiceNow.

#. Under **NICs**, ensure the **Runtime** option is enabled. Select **User VM Network** with a **Dynamic** IP.

   This will ensure all newly requested VMs are provisioned in the easily expandable AWS Clusters environment by default, ensuring Alex doesn't put any additional pressure on their on-prem environment. Leaving it as a runtime variable will allow a ServiceNow administrator additional flexibility in defining the self-service offering.

   .. figure:: images/21.png

#. Click **Advanced Options**.

#. Under **Credentials**, click **Add/Edit credentials**. Specify a password the **ROOT** credential (ex. *nutanix/4u*).

   This will be configurable for the user at runtime, but Calm requires a default value be provided before the Blueprint can be launched.

   .. figure:: images/22.png

#. Click **Done**.

#. Click **Save**.

   .. note::

      You should no longer see any red error alerts for the Blueprint, but warning alerts related to missing variable values are expected and will not impact the Blueprint.

Takeaways
+++++++++

- Prism provides a single console solution for managing VMs and policies such as snapshot and replication, and microsegmentation.

- Calm Projects allow you to define pools of resources for specific users and groups.

- Calm Blueprints enable repeatable application deployments and lifecycle operations.
