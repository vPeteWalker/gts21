.. _karbon_environment_deploy:

----------------------------
Deploying Fiesta Web Service
----------------------------

In the **Containerizing Apps & CI/CD** lab, we explored how to create container images from a legacy VM-based application. What we were ignoring was the infrastructure on which the container ran: our single VM development environment.

In this exercise we will build on that experience by deploying a Fiesta container and publishing as a service on the Kubernetes cluster, able to take advantage of all of the orchestration and resiliency that Kubernetes can provide.

.. note::

   This exercise does not depend on previous completion of the **Containerizing Apps & CI/CD** lab. This lab will use a pre-built **Fiesta** container image.

Creating The Manifest
+++++++++++++++++++++

We'll begin by creating the manifest file for the **Fiesta** web frontend and then dissect the different components of the file.

#. Open **Visual Studio Code** in your **USER**\ *##*\ **-WinToolsVM** VM.

#. Select **File > New File** and paste the following into the blank file:

   .. code-block:: yaml

      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: fiesta-web-pods
        namespace: default
      spec:
        replicas: 3
        selector:
          matchLabels:
            run: fiesta-web
        template:
          metadata:
            labels:
              run: fiesta-web
          spec:
            containers:
            - name: npm-fiesta
              image: public.ecr.aws/n5p3f3u5/npm-fiesta:latest
              ports:
              - containerPort: 3000
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: fiesta-web-svc
        namespace: default
      spec:
        ports:
        - port: 3000
          protocol: TCP
        selector:
          run: fiesta-web

#. Save the file as **fiesta_app.yaml** in your **Downloads** folder.

   .. figure:: images/13.png

   *So what does this manifest DO?*

   **TL;DR**

      The manifest downloads the Fiesta container from a public repository and provisions 3 copies and are exposed as a Service in the Kubernetes cluster named **fiesta-web-svc** and listening on port **3000**. The lack of **LoadBalancer** service in the manifest means we will not have external IP for the service.

   **Lines 1-20** define the **Deployment**

      - **kind**: Deployment

         `Deployments <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>`_ describe the desired state for Pods and ReplicaSets and functions similar to an installation script.

      - **namespace**: default

         `Namespace <https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_ are used to provide logical separation between Pods deployed on a Kubernetes cluster. They define virtual clusters much the same way VLANs provide logical separation on a network. This allows different applications with conflicting Resource names (think two apps that each have a Service named **gateway** used to expose their web interface) to run on the same cluster.

      - **spec > replicas:** 3

         This defines how many copies of the Pod should be started. Multiple copies of a Pod are typically used for high availability or scaling performance.

      - **spec > metadata > labels:** run: fiesta-web

         `Label selectors <https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors>`_ are used to identify and group Kubernetes Resources. This label will be referenced by our Service so it knows which **Deployment** to execute.

      - **spec > template > spec > containers > image:** public.ecr.aws/n5p3f3u5/npm-fiesta:latest

         This defines the repository location of the Docker container which will be downloaded as part of the Deployment. In this case, our Fiesta container is being hosted on the Amazon Elastic Container Registry.

      - **spec > template > spec > containers > ports > containerPort:** 3000

         This is the port that the Docker container NodeJS webserver is listening on. It is hard coded as part of the container image.

   **Lines 19-29** define the **Service**

      - **kind**: Service

         `Services <https://kubernetes.io/docs/concepts/services-networking/service/>`_ allow you to expose a set of Pods as a service on the network.

      - **metadata > name:** fiesta-web-svc

         This is the name of the service that will be advertised on the cluster.

      - **spec > ports > port:** 3000

         Which port the Service will use on the network. This does **not** need to match the container port, this choice was made to reduce lab mistakes.

      - **spec > selector:** run: fiesta-web

         This is what ties the Service to the Deployment. Note the Selector value matches the same **run: fiesta-web-pods** label applied to the Deployment. The benefit of using labels to define the resource requirement for the Service is that labels are independent of scale (# of Pods) or IPs. This is similar to the concept of using Nutanix Categories, for example when tagging VMs for Flow or Data Protection policies.

Deploying Fiesta
++++++++++++++++

Now that you have created your manifest and understand the actions it will perform, we can appply the file to the cluster.

#. Return to **PowerShell** and run ``kubectl apply -f fiesta_app.yaml``

#. Return to **Lens** and select **Workloads > Pods** to view your deployment in the dashboard.

   .. figure:: images/14.png

   You should observe 3 **fiesta-web-pods** running. You can select an individual Pod to view the Node on which the Pod is running, its internal IP, labels, performance, etc.

#. Return to **Visual Studio Code** and reduce the **replicas** from **3** to **2** and save your **fiesta_app.yaml** file.

#. Run ``kubectl apply -f fiesta_app.yaml`` to apply the change.

   With Kubernetes, you can rapidly update configurations without first having to clean up your old configuration.

#. In **Lens**, observe that one of your Pods is being **Terminated** as it is no longer required.

   .. figure:: images/14.png

   Imagine applying the same Infrastructure-as-Code CI/CD methodology covered in the **Containerizing Apps and CI/CD** lab to this environment - your **YAML** files would exist in a source repository, and changes like the update to the number of replicas would become commits generating build tasks that would apply the changes to your Kubernetes cluster - *powerful stuff!*

   Our containers hosting the web service are now running, but we have a problem - *how do we access them?*

Configuring Traefik
+++++++++++++++++++

In order to get access to our **Fiesta** web frontend, we need to define a new **IngressRoute**. An **IngressRoute** is a custom resource type (**kind**) created by the **Custom Resource Definition** for **Traefik** during its installation.

#. Return to **Visual Studio Code** and click **File > New File**.

#. Paste the following into the blank file:

   .. code-block:: yaml

      apiVersion: traefik.containo.us/v1alpha1
      kind: IngressRoute
      metadata:
        name: simpleingressroute
        namespace: default
      spec:
        entryPoints:
          - web
        routes:
        - match: Host(`fiesta.lab.local`)
          kind: Rule
          services:
          - name: fiesta-web-svc
            port: 3000

   This will define a new rule in **Traefik** that will forward HTTP (**web**) traffic for **fiesta.lab.local** hostname to the **fiesta-web-svc**, which is the advertised name exposing your **fiesta-web-pods** on the internal cluster network.

#. Save the file as **traefik-routes.yaml** in your **Downloads** folder.

#. In **PowerShell**, run ``kubectl apply -f traefik-routes.yaml`` to add your **Traefik IngressRoute**.

#. In **PowerShell**, run ``kubectl get svc`` and note your **Traefik EXTERNAL-IP**.

   .. figure:: images/16.png

#. In **Traefik** (\http://*<TRAEFIK-EXTERNAL-IP>*:8080), select **HTTP** from the toolbar to verify your new route appears.

   .. figure:: images/7b.png

   In a production environment, your **Host** value would be an accessible DNS entry. To simplify the lab, you will create a local entry in the Windows **/etc/hosts** file instead of a DNS A Record.

#. Replace *<TRAEFIK-EXTERNAL-IP>* with the IP from **Step 5** and run the following command in **PowerShell**:

   .. code-block:: powershell

      Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "<TRAEFIK-EXTERNAL-IP>`tfiesta.lab.local" -Force
      
      cat C:\Windows\System32\drivers\etc\hosts

   .. note::

      No, ``<TRAEFIK-EXTERNAL-IP>`tfiesta.lab.local`` isn't a typo. ```t`` in PowerShell inserts a tab between the **<TRAEFIK-EXTERNAL-IP>** value and **fiesta.lab.local**.

   .. figure:: images/17.png

#. Open \http://fiesta.lab.local in your **USER**\ *##*\ **-WinToolsVM** browser. *Looking good!*

   .. figure:: images/18.png

#. Click **Stores** or **Products**.

   *Whoops! Maybe not looking so good.*

   We're now able access our highly available set of **fiesta-web-pods** through our **LoadBalancer** and **Ingress Controller**, but we forgot about the database!

Configuring The Database Connection
+++++++++++++++++++++++++++++++++++

As seen in the **Containerizing Apps & CI/CD** lab, the **npm-fiesta** container image can accept multiple environment variables to dynamically configure the application at runtime.

Kubernetes can `set environment variables <https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container>`_ as part of the manifest file.

#. Return to **Visual Studio Code** and open your **fiesta_app.yaml** file.

#. In the **containers:** section, add the following lines below the **image:** line:

   .. code-block:: yaml

      env:
        - name: DB_PASSWD
          value: fiesta
        - name: DB_USER
          value: fiesta
        - name: DB_SERVER
          value: <IP ADDRESS OF YOUR MARIADB SERVER>
        - name: DB_TYPE
          value: mysql

   The indentation should match the screenshot below.

   .. figure:: images/10.png

#. **IMPORTANT!** Change *<IP ADDRESS OF YOUR MARIADB SERVER>* to the IP address of your **User**\ *##*\ **-MariaDB_VM** VM.

   .. note::

      The database VM has already been provisioned for you, you do not need to deploy the database.

      .. figure:: images/21.png

#. Save the file and run ``kubectl apply -f fiesta_app.yaml`` to update your deployment.

#. Wait a minute, and refer \http://fiesta.lab.local in your **USER**\ *##*\ **-WinToolsVM** browser.

   .. figure:: images/20.png

   *That's better!*

.. raw:: html

    <H1><a href="http://lookup.ntnxworkshops.com/" target="_blank"><font color="#B0D235"><center>Click Here To Submit Validation Request</center></font></a></H1>

You now have a highly available web front end for your **Fiesta** application to is accessible to the outside world on a standard HTTP port, while maintaining the ability to share port 80 with other services that could be deployed to the Kubernetes cluster in the future.

In the final exercise we will explore common **Day 2 Operations** for managing Karbon Kubernetes infrastructure.
