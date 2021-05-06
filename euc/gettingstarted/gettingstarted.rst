.. _snow_gettingstarted:

---------------
Getting Started
---------------

This lab track is designed to showcase Nutanix as an ideal platform for delivering a true hybrid cloud for EUC workloads, leveraging both the flexibility of AWS and Nutanix Clusters and integration with Citrix Virtual Apps and Desktops.

Due to the COVID-19 pandemic, Party Time Excellent has needed to shift much of their staff from their office desktops to working remotely. PTE has previously invested in a small Citrix Virtual Apps & Desktops deployment, running on Nutanix AHV, used to support secure access for short-term contractors.

At the beginning of the pandemic, PTE had limited capacity within their existing infrastructure to accommodate the surge in utilization caused by the sudden demand for virtual desktops. As a Nutanix customer, PTE was able to easily add nodes to their on-premises Nutanix cluster in order to support a percentage of the demand. However, PTE expects the majority of their office workers to return post-pandemic, and therefore does not want to the significant capital investment in on-premises hardware when it expects to only require these virtual desktops for another year.

PTE needs to move **fast** on how to respond to on-going requests for virtual desktop capacity without long-term commitment.

.. raw:: html

   <br><center><img src="https://i.gifer.com/51N.gif"></center><br><br>

..   On-prem environment with limited capacity
   Due to global events, you've seen a significant increase in demand for virtual desktops
   Also have seasonal usage spikes, short term consultants, etc.
   Have an established on-prem golden image
   want security that follows your users
   want to provide service desk operators with the ability to easily add new desktops to the least loaded cluster dynamically

Your Environment
++++++++++++++++

To let you experience the most fun and interesting parts of the lab, as well as accommodate the large number of simultaneous users, multiple components have already been staged for you. *Let's explore!*

.. raw:: html

   <br><center><img src="https://github.com/nutanixworkshops/gts21/raw/master/euc/gettingstarted/images/env.png"><br><i>vGTS 2021 Hybrid Cloud EUC Lab Environment</i></center><br>

Clusters on AWS
...............

A single node Nutanix cluster running in AWS has already been provisioned and registered to your on-premises Prism Central instance.

.. figure:: images/1.png

Citrix Delivery Controller
..........................

A Citrix Delivery Controller (DDC) has been deployed on each shared environment via Calm Blueprint, which can be viewed in **Prism Central > Services > Calm > Blueprints > CitrixBootcampInfra**.

   .. figure:: images/2.png

The DDC is deployed on a Windows Server and acts as the connection broker between your virtual machine and the Citrix Workspace client. Additionally this VM includes services for Citrix web front end (StoreFront), and Citrix Licensing - both are components that would typically run on dedicated infrastructure in a production environment.

A single Citrix Virtual Apps and Desktops site can contain multiple Delivery Controllers and StoreFronts for the purposes of redundancy and scaling out to support increasingly large environments.

Tools VM
........

The Windows Tools VM provides a number of different applications used across multiple Nutanix Bootcamps. Filter for your **USER**\ *##* in **Prism Central > Virtual Infrastructure > VMs** and take note of the IP of your **USER**\ *##*\ **WinToolsVM** VM, as you will be connecting to this VM via RDP (using **NTNXLAB** Administrator credentials).

   .. figure:: images/3.png

In the following labs you will use the Tools VM to access the Citrix DDC using the **Citrix Studio** application, and use the **Citrix Workspace** client on this VM to test the connection to your virtual desktops.

Gold Image
..........

One of the benefits of using Clusters to expand your EUC environment is not having to build, optimize, and test a whole new master image for your desktop pools - so to save you time in the lab, you'll use the Gold Image VM that PTE has provided.

This VM already has the Citrix Virtual Desktop Agent (VDA) installed and optimizations applied. **There is no need to power on this VM.**

   .. figure:: images/4.png
