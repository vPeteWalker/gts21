.. _euc_secure:

---------------------------
Securing Desktops with Flow
---------------------------

.. note::

   This exercise depends on completion of the **Hybrid Cloud IaaS** :ref:`snow_preparingenv` exercise to properly categorize VMs that will be used in Flow policies. Refer to the linked section first before proceeding.

As seen in other exercises, Nutanix Flow Security makes it easy to define and enforce network security policies for applications running on Nutanix. ID Firewall is an extension to Flow that allows you to write security policies based on users and groups in an Active Directory domain in which your VDI VMs are attached. When using ID Firewall, you can import groups from Active Directory into Prism Central as categories (in the category key ADGroup), and then write policies around these categories, just as you would for any other category.

This means with the same set of underlying virtual desktops, you can enforce different access policies, at logon, based on who is logged into that desktop VM.

In this exercise you'll configure the Flow VDI Policy to prevent a group of users within your environment from accessing an application on the network.

Configuring ID Based Security
+++++++++++++++++++++++++++++

.. raw:: html

   <strong><font color="red">Configuring the settings in this section only needs to be done once per shared environment.</font></strong><br><br>

.. note::

   You can ignore any warnings about the **Prism-Pro-Cluster** having a version of AOS < 5.17, as this isn't a real cluster.

#. In **Prism Central**, select :fa:`bars` **> Prism Central Settings**.

#. Under **Flow**, select **ID Based Security**.

#. If the **Bootcamp Users** and **SSP Developers** user groups have already been added, review the configuration and skip to :ref:`euc_flowpolicy`. Otherwise, complete the steps below to configure **ID Based Security**.

#. If **No Active Directory Domains** have been added, click **Use Existing AD**.

   .. figure:: images/1.png

#. Select **NTNXLAB** from the **AD Server** dropdown and provide the **NTNXLAB\\Administrator** password as the **Service Account Password**.

   .. figure:: images/2.png

#. Click **Next**.

#. Click **Manually add Domain Controllers**.

   The IP of the primary domain controller (ex. 10.X.X.41) should be automatically populated.

#. Click :fa:`check-circle` to confirm the addition of your domain controller.

   .. figure:: images/3.png

#. Click **Save**.

   .. note::

      ID Based Security requires the following:

      - Prism Central requires WMI access to all the Active Directory Domain Controllers in your network firewall and Active Directory firewall.
      - Minimum supported domain functional level in Active Directory is Windows Server 2008 R2.
      - ID Firewall checks the membership of Security Groups only, Distribution Groups are not supported.
      - NTP must be configured on Active Directory and Prism Central.
      - DNS must be configured on Prism Central if you want to use host name for domain controllers.

#. Under **Referenced AD Groups**, click **+ Add User Group**.

#. Specify **Bootcamp Users** as the **User Group** and click :fa:`check-circle`.

   .. figure:: images/4.png

#. Repeat **Steps 9-10** to add the **SSP Developers** user group.

   .. figure:: images/5.png

.. _euc_flowpolicy:

Adding The Flow VDI Policy
++++++++++++++++++++++++++

.. raw:: html

   <strong><font color="red">Configuring the settings in this section only needs to be done once per shared environment. You wil have an opportunity in the steps below to explore the capabilities of the built-in VDI Policy but the policy will not be applied as it would affect all users of the shared lab environment.</font></strong><br><br>

The VDI Policy needs to be added to Prism Central in order for Flow to start processing Active Directory logins for VMs. This will start automatically adding the **ADGroup** category to VMs that are in use by AD user accounts mapped to the groups that you've configured for ID Based Security in Prism Central.

In addition to the single VDI Policy, which allows you to map whitelist connections to your various ADGroup values, you can also leverage the ADGroup category in Isolation Policies.

#. If the **VDI Policy** already exists, review the steps and proceed to :ref:`euc_flowpolicy2`.

#. In **Prism Central**, select :fa:`bars` **> Policies > Security**.

#. Click **Create Security Policy** and select **Secure VDI Groups (VDI Policy)**.

   .. figure:: images/6.png

   .. note::

      If **Secure VDI Groups (VDI Policy)** appears greyed out, this means the policy has already been created. By design, Flow currently only supports a single VDI Policy, as you are able to perform mappings for multiple Active Directory user groups within a single policy.

      Click **Cancel** and search for **VDI Policy** in the list of available policies. Review the following steps to see how the policy works, but action is not required until you reach `Creating A User Based Isolation Policy`_.

#. Click **Create**.

#. Select **Include all VMs**.

   .. figure:: images/13.png

   Typically you would select **Include VMs by name** and specify whatever portion of your VM naming scheme is shared across all your virtual desktops (ex. VDI or CTX). As the shared environment lacks this consistency, we will target ALL VMs. This will ensure all VMs will be subject to AD logon processing by Prism Central to dynamically assign its **ADGroup** category.

.. #. Select **Add these VMs to a default policy**.

   .. figure:: images/7.png

#. Click **Next**.

#. Click **Import all AD Groups** to add all AD groups configured in **Prism Central ID Based Security** to the policy.

#. Explore the policy builder and observe, similar to a Flow App Policy, it is possible to whitelist inbound and outbound traffic based on IP, subnet, or Nutanix category.

   .. figure:: images/8.png

   Additionally, when mapping inbound or outbound rules to **ADGroups**, you can further narrow your policy by defining specify services based on protocol and port.

   .. figure:: images/10.png

#. After experimenting, click **Next**.

#. Ensure **Monitor** is selected as the **Policy mode** before clicking **Save and Monitor**.

   .. figure:: images/9.png

   .. raw:: html

      <br><br><strong><font color="red">DO NOT ENFORCE THIS POLICY AS IT COULD NEGATIVELY IMPACT OTHER USERS ON YOUR SHARED CLUSTER!</font></strong><br><br>

   .. figure:: https://media.giphy.com/media/yAcKHAu1iFdTvOysZK/giphy.gif

.. _euc_flowpolicy2:

Creating A User Based Isolation Policy
++++++++++++++++++++++++++++++++++++++

In addition to the single VDI Policy, which allows you to map whitelist connections to your various ADGroup values, you can also leverage the ADGroup category in Isolation Policies.

#. In **Prism Central**, select :fa:`bars` **> Policies > Security**.

#. Click **Create Security Policy** and select **Isolate Environments (Isolation Policy)**.

#. Click **Create**.

#. Fill out the following fields:

   - **Name** - USER\ *##*\ -ADIsolation (ex. USER01-ADIsolation)
   - **Purpose** - Blacklisting NTNXLAB Bootcamp Users from category
   - **Isolate this category** - ADGroup:Bootcamp Users
   - **From this category** - User:\ *##* (ex. USER:01)
   - **Select a Policy mode** - Monitor

   .. figure:: images/11.png

   .. note::

      This assumes you have already added the **USER:**\ *##* category to your **USER**\ *##*\ **-FiestaWeb** and **USER**\ *##*\ **-MSSQL-Source** VMs, completed as part of **Hybrid Cloud IaaS** :ref:`assign_categories`.

      If you have not completed this exercise, refer to the linked steps for instruction on how to add the category to the aforementioned VMs.

#. Click **Save and Monitor**.

#. Return to your **USER**\ *##*\ **-WinTools** VM.

#. Sign out of any Citrix desktop sessions you may have left open.

#. Open http://ddc.ntnxlab.local/Citrix/NTNXLABWeb/ and login as **NTNXLAB\\user**\ *##* (ex. NTNXLAB\\user01).

#. Launch your Windows 10 desktop and wait for login to complete.

#. Attempt to ping the IP of your **USER**\ *##*\ **-FiestaWeb** or access the IP via your browser. You should expect the connection to succeed as you have not yet enforced your policy.

   Note the hostname of your desktop VM.

   .. figure:: images/12.png

#. Return to your **USER**\ *##*\ **-ADIsolation** policy in **Prism Central** and observe that traffic flows have been discovered, and your VM has been automatically added to the **ADGroup:Bootcamp Users** category.

   .. figure:: images/14.png

#. Click **Enforce** to start enforcing the policy and return to your desktop to verify you no longer have access to **USER**\ *##*\ **-FiestaWeb**.

   .. figure:: images/15.png

   That's it! Optionally, you can continue logging into desktops as your **user** and **devuser** accounts and validate that categories and policy are applied as expected - whether on-prem or in the cloud!

.. raw:: html

    <H1><a href="http://lookup.ntnxworkshops.com/" target="_blank"><font color="#B0D235"><center>Click Here To Submit Validation Request</center></font></a></H1>

Takeaways
+++++++++

- ID Based Security further extends Flows microsegmentation capabilities to user based policies to better support virtual desktop use cases
