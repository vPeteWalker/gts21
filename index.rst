.. title:: Nutanix Global Tech Summit 2021

.. toctree::
   :maxdepth: 2
   :caption: Event Info
   :name: _info
   :hidden:

   info/details
   info/help
   info/validate

.. toctree::
   :maxdepth: 2
   :caption: Hybrid Cloud IaaS
   :name: _hybridiaas
   :hidden:

   snow/gettingstarted/gettingstarted
   snow/policies/policies
   snow/snowcalm/snowcalm
   snow/migration/migration
   snow/alerts/alerts
   snow/webhook/webhook

.. toctree::
   :maxdepth: 2
   :caption: Hybrid Cloud Database Management
   :name: _hybrideuc
   :hidden:

   dbs/gettingstarted/gettingstarted
   dbs/clustersaag/clustersaag
   dbs/clustersdam/clustersdam
   dbs/patching/patching
   dbs/sqlmonitoring/sqlmonitoring

.. toctree::
   :maxdepth: 2
   :caption: Hybrid Cloud EUC
   :name: _hybrideuc
   :hidden:

   euc/gettingstarted/gettingstarted
   euc/expand/expand
   euc/runbook/runbook
   euc/secure/secure

.. toctree::
   :maxdepth: 2
   :caption: Containerizing Apps and CI/CD
   :name: _cicd
   :hidden:

   cicd/start/start
   cicd/basic/basic
   cicd/phase2/phase2
   cicd/phase3/phase3
   cicd/phase4/phase4
   cicd/phase5/phase5

.. toctree::
   :maxdepth: 2
   :caption: Cloud Native Apps on Nutanix
   :name: _k8s
   :hidden:

   karbon/gettingstarted/gettingstarted
   karbon/preparation/preparation
   karbon/karbon/karbon
   karbon/deploy/deploy
   karbon/day-2/day-2


.. raw:: html

   <br><center><img src="https://github.com/nutanixworkshops/gts21/raw/master/images/welcome.png" alt="Welcome to Nutanix Virtual Global Tech Summit 2021"></center><br>

.. .. image:: images/welcome.png
   :align: center

**Welcome!** This year we're celebrating how we power customer use cases by exposing you to exciting new hybrid cloud use cases enabled by our core platform, our portfolio products, and Nutanix Clusters on AWS. Here's a quick look at the available labs:

   - **Hybrid Cloud IaaS**

      Take self-service to the next level with Nutanix ServiceNow integrations. Configure self-service VM provisioning across your multi-cloud environment with ServiceNow and Calm. Secure, protect, and migrate workloads with Flow and Leap. Automatically remediate performance issues with ServiceNow and Prism X-Play.

   - **Hybrid Cloud Database Management**

      Provision, clone, patch, and monitor Microsoft SQL Server across multiple clouds with Nutanix Era and Prism Ultimate.

   - **Hybrid Cloud EUC**

      Find out how you can go from hundreds to thousands of Citrix Desktops in hours versus weeks. Use Calm Runbooks to build powerful, repeatable automation to intelligently provision new desktops. Secure your desktop environment with Flow's VDI Policy.

   - **Containerizing Apps and CI/CD**

      Learn about the benefits and challenges of re-platforming applications first hand by containerizing an application with Docker. Build a full CI/CD pipeline with Git and Drone. Integrate with Era APIs for database cloning.

   - **Cloud Native Apps on Nutanix**

      Lift and shift may not be for you, but there are still economic and security benefits to running your containerized apps on-prem. Deploy and manage Nutanix Karbon and Objects, plus third party integrations, to deliver a full Kubernetes stack to support Cloud Native Apps.

.. raw:: html

   <strong><font color="red">Before beginning any labs, review the following sections for important information regarding your lab environment, scenario, and FAQs.</font></strong><br><br>

Your Environment
++++++++++++++++

Labs will be completed on a shared hybrid cloud environment consisting of:

   - 1x 4 Node RF2 Nutanix "HPOC" Cluster running in either Nutanix PHX or RTP datacenters
   - 1x 1 Node RF1 Nutanix "Public Cloud" Cluster running in AWS US-WEST-2 datacenter
   - To conserve resources, both clusters are joined to a single Prism Central instance running on the "HPOC" cluster
   - To conserve resources, both clusters use a single Domain Controller VM for Active Directory and DNS
   - **Each of these environments will be shared by up to 7 users, please be mindful not to waste memory and IP resources**

Refer to :ref:`clusterdetails` for your specific lab assignment information, as the provided diagram is a generic, high level representation of your environment.

.. raw:: html

   <br><center><img src="https://github.com/nutanixworkshops/gts21/raw/master/images/env.PNG"><br><i>vGTS 2021 Lab Environment</i></center><br>

Meet Your Customer
++++++++++++++++++

For vGTS21, you'll be playing the part of a scrappy IT consultant attempting to win hearts and minds (and open wallets) inside of **Party Time, Excellent Inc.**, by demonstrating solutions to some of their most pressing challenges.

Founded by former public access television rock star duo, Wayne Campbell and Garth Algar, in 1992, Party Time, Excellent, Inc. (PTE) has become an established name in both manufacturing and retail. Starting out of a garage in Aurora, Illinois, fashioned into a store selling balloons, streamers, and other "party accessories," PTE has grown to over 2,000 retail locations worldwide. Through acquisitions in the late 90's and early 00's, PTE vertically integrated into related industries, including manufacturing, helium distribution, and party planning services.

.. raw:: html

   <br><center><img src="https://github.com/nutanixworkshops/gts21/raw/master/images/waynes_car2a.jpg"><br><i>Founders Campbell and Algar photographed for the 1996 Wall Street Journal article: PTE IPO FTW</i></center><br>

Despite the positive outlook from Chairman Wayne Campbell, PTE is facing significant challenges. In particular, the COVID-19 pandemic has slashed retail sales. Stores are open in many locations, but customers are simply no longer planning parties. In order to survive, PTE has to take massive steps to re-invent itself - **and requires the right technologies and processes to support that transformation.**

.. raw:: html

   <br><center><img src="https://media.giphy.com/media/y0IjNxdBMPJjG/giphy.gif"><br><i>Chairman Wayne Campbell after being informed that moving to the cloud does not involve airplanes.</i></center><br>

The **Getting Started** section of each lab track will continue the journey.

Frequently Asked Questions
++++++++++++++++++++++++++

.. raw:: html

   <br><center><img src="https://media.giphy.com/media/9Pk1GBaXV8QGbsoaUF/giphy.gif"></center><br><br>

Should I Copy Name & IP Information Directly From Screenshots?
..............................................................

**NO!** Screenshots are meant to provide navigational context. Screenshot values such as **XYZ** and **USER00** should be replaced with your actual initials or user ID value, as directed in the text of the lab. Similarly, IP addresses used should be relevant to **YOUR** cluster/VM/application/etc.

.. raw:: html

   <br><center><img src="https://github.com/nutanixworkshops/gts21/raw/master/images/skeleton.png"></center><br><br>

Do The Names Provided In The Labs Really Matter?
................................................

William Shakespeare once wrote "*What's in a name? That which we call a rose by another other name would smell as sweet.*" William Shakespeare never tried to support hundreds of people simultaneously doing hands-on labs. Had he, Romeo and Juliet would have been a very different play.

If the lab tells you to include your **USER**\ *##* ID in something, *please do it*. If the lab tells you to name a policy, or Blueprint, or VM, etc. a certain value, *please do it*.

This make it far easier for our limited staff of SMEs to help you if and when you have issues.

.. raw:: html

   <br><center><img src="https://media.giphy.com/media/3orif35YFvvYrWAWmA/giphy.gif"></center><br><br>

Can I Run LCM Updates On My Cluster?
....................................

**PLEASE NO!** The versions of PC, Karbon, Calm, etc. used in the labs are what have been verified. The latest version of Calm introduces some UI changes that would make the lab more difficult to follow. The latest version of PC introduces a Leap UI bug that that will impact the **Hybrid Cloud IaaS** lab.

.. raw:: html

   <br><center><img src="https://media.giphy.com/media/F8BGFOzGhswhRUS1w8/giphy.gif"></center><br><br>

I Have An Issue, Should I Reboot Prism Central On My Cluster?
.............................................................

I can't believe I have to say this, but **NO**, please do not reboot Prism Central or Prism Central services on your cluster **THAT IS BEING SHARED WITH SEVERAL OTHER PEOPLE**. Reach out in the appropriate Slack channel for assistance with your lab issue.

See :ref:`help` for complete instructions.

.. raw:: html

   <br><center><img src="https://media.giphy.com/media/l3V0H7bYv5Ml5TOfu/giphy.gif"></center><br><br>

Where Is The Lab For Provisioning Clusters?
...........................................

**On the way!** Enablement is finishing a standalone Bootcamp that will focus on teaching you how to provision a cluster with AWS and deploy a VPN virtual appliance. Unfortunately the logistics for delivering something like this as part of GTS *just don't work* (lack of AWS baremetal capacity, time taken to "stage" cluster post-provisioning to complete additional labs, etc.).

We'll communicate to the field as soon as this is ready for on-demand self-enablement!

How Long Do I Have Access To The Labs?
......................................

The lab environments will be available all day Tuesday and Wednesday. The labs will be supported by a team of SMEs during the following periods:

- **Tuesday** - 09:00AM AEST - 10:00PM AEST
- **Wednesday** - 09:00AM AEST - 10:00PM AEST

The lab environments will continue to be available until 11:59PM JST on Wednesday if you wish to continue working on labs after the closing session. *SME support and lab validation will be available on a best effort basis after Wednesday's closing session.*

Do I Have To Complete The Lab Tracks In Order?
..............................................

Within a **Lab Track** (ex. **Hybrid Cloud EUC**), individual exercises should be completed in order (**Getting Started -> Provision and Expand -> ...**). However, you should be able to complete the tracks in your order of interest.

.. note::

   The **Hybrid Cloud EUC** track depends on the completion of :ref:`snow_preparingenv` at the beginning of the **Hybrid Cloud IaaS** track in order to create your dedicated Calm project and properly categorize VMs.

How Many Labs Should I Complete?
................................

With 1.5 days of supported lab time, you should be able to complete **at least** 3 of the available lab tracks.

What Happens To The Labs Post-Event?
....................................

Following the event, we will be integrating the GTS labs into new and existing Bootcamps for you to drive prospect and customer engagement during 2021.

How Do I Get My Cluster Assignment Info?
........................................

See :ref:`clusterdetails` for complete instructions.

How Do I Get Support?
.....................

Supporting virtual events can be tricky, but to keep the experience familiar for users we made the conscious decision to not introduce new 3rd party tools, instead opting for a process that relies on both **Slack** and **Zoom**.

See :ref:`help` for complete instructions.

How Do I Validate My Labs?
..........................

This year we're introducing self-service validation requests to keep you focused and productive.

See :ref:`validate` for complete instructions.

Where Can I Access More Clusters Demo Resources?
................................................

- Hands-On Clusters Deployment Workshop - *Coming soon!*

- `Clusters Test Drive <https://www.nutanix.com/one-platform?type=clusters>`_ - Sign-up to provide a prospect with a 2 hour, interactive demo of Clusters on AWS.

- `Standalone Clusters Deployment Demo <https://clusters.nutanixtestdrive.com/>`_ - On-demand MCM Clusters on AWS deployment demo *without a Test Drive sign-up.* A great option for quick demos of how easily Clusters can be provisioned.

- `Nutanix YouTube Clusters Playlist <https://www.youtube.com/playlist?list=PLAHgaS9IrJeevEB17CSW5BE8Y9n9v18bU>`_ - Short videos covering topics like deployment, networking, security, and hibernation.
