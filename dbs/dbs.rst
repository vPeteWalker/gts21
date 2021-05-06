STAGING

HPOC STAGING:

   Enable App Discovery - this seems to restart PC, so probably wants to go early?
   And enable SQL Server monitoring integration

   Creating User:01 - User:10 category values

   Images:
      Era-Server-2.1.0.qcow2 6G
      MSSQL16-Source-Disk1.qcow2	19G
      MSSQL16-Source-Disk2.qcow2	104M
      MSSQL19-Profile-Disk1.qcow2	17G
      MSSQL19-Profile-Disk2.qcow2 888M

   Import Fiesta-MSSQL-Source Blueprint
      Provision 7 copies (USER00-Fiesta, USER01-Fiesta, etc.)
      Using Primary network
      CENTOS7.qcow2 for WebServer
      MSSQL-Source-Disk1.qcow2/MSSQL-Source-Disk2.qcow2 for Database
      No Check-Login for database (static image)
      root/nutanix/4u creds for ROOT credential

   Provision 1x SQL19 Profile Source VM
      Name - MSSQL19-Profile
      4vCPU/8GB RAM
      Primary Network - want static IP to make registration more predictable
      MSSQL19-Profile-Disk1.qcow2
      MSSQL19-Profile-Disk2.qcow2

   Provision 1x Era VM
      4 vCPU/16GB RAM
      Secondary (not sure if you normally set a static for this)

   Set Era admin password to PC password
   Add HPOC cluster to Era - MAY DEPEND ON SELECTING SelfServiceContainer as the Era container?!v

   Create Era Managed network using 211-253 Secondary range
      era > resource network add nx_cluster_id=79cb2c4e-1455-4798-aa4d-c53929e730ab  name=Secondary ip_managed_in_era gateway=10.42.93.129 subnet_mask=255.255.255.128 primary_dns=10.42.93.41 start_ip=10.42.93.211 end_ip=10.42.93.253 dns_domain=ntnxlab.local

   Create LAB_COMPUTE profile (4vCPU/6GB RAM)
      era > profile compute generate_input_file for_create output_file=LAB_MSSQL_COMPUTE.json

      {
        "type": "Compute",
        "topology": "ALL",
        "dbVersion": "ALL",
        "systemProfile": false,
        "properties": [
          {
            "name": "CPUS",
            "value": "4",
            "secure": false,
            "description": "Number of CPUs in the VM"
          },
          {
            "name": "CORE_PER_CPU",
            "value": "1",
            "secure": false,
            "description": "Number of cores per CPU in the VM"
          },
          {
            "name": "MEMORY_SIZE",
            "value": "8",
            "secure": false,
            "description": "Total memory (GiB) for the VM"
          }
        ]
      }

      era > profile compute create name=LAB_COMPUTE input_file=LAB_MSSQL_COMPUTE.json

   Create NTNXLAB Domain profile

      era > profile windows_domain generate_input_file for_create output_file=NTNXLAB.json

      {
        "engineType": "sqlserver_database",
        "type": "WindowsDomain",
        "topology": "ALL",
        "dbVersion": "ALL",
        "systemProfile": false,
        "properties": [
          {
            "name": "DOMAIN_NAME",
            "value": "NTNXLAB.local",
            "secure": false,
            "description": "Name of the Windows domain (in FQDN format)"
          },
          {
            "name": "DOMAIN_USER_NAME",
            "value": "ntnxlab.local\\Administrator",
            "secure": false,
            "description": "Username with permission to join computer to domain"
          },
          {
            "name": "DOMAIN_USER_PASSWORD",
            "value": "nutanix/4u",
            "secure": false,
            "description": "THIS IS A SENSITIVE FIELD. If left blank, you would be prompted for input during command execution. Password for the username with permission to join computer to domain"
          },
          {
            "name": "DB_SERVER_OU_PATH",
            "value": "",
            "secure": false,
            "description": "Custom OU path for database server VMs"
          },
          {
            "name": "CLUSTER_OU_PATH",
            "value": "",
            "secure": false,
            "description": "Custom OU path for server clusters"
          },
          {
            "name": "SQL_SERVICE_ACCOUNT_USER",
            "value": "ntnxlab.local\\Administrator",
            "secure": false,
            "description": "Sql service account username"
          },
          {
            "name": "SQL_SERVICE_ACCOUNT_PASSWORD",
            "value": "nutanix/4u",
            "secure": false,
            "description": "THIS IS A SENSITIVE FIELD. If left blank, you would be prompted for input during command execution. Sql service account password"
          },
          {
            "name": "ALLOW_SERVICE_ACCOUNT_OVERRRIDE",
            "value": "true",
            "secure": false,
            "description": "Allow override of sql service account in provisioning workflows"
          },
          {
            "name": "ERA_WORKER_SERVICE_USER",
            "value": "ntnxlab.local\\Administrator",
            "secure": false,
            "description": "Era worker service account username"
          },
          {
            "name": "ERA_WORKER_SERVICE_PASSWORD",
            "value": "nutanix/4u",
            "secure": false,
            "description": "THIS IS A SENSITIVE FIELD. If left blank, you would be prompted for input during command execution. Era worker service account password"
          },
          {
            "name": "RESTART_SERVICE",
            "value": "",
            "secure": false,
            "description": "Restart sql service on the dbservers"
          },
          {
            "name": "UPDATE_CREDENTIALS_IN_DBSERVERS",
            "value": "true",
            "secure": false,
            "description": "Update the credentials in all the dbservers"
          }
        ]
      }

      era > profile windows_domain create name=NTNXLAB input_file=NTNXLAB.json

   Enable multi-cluster

      era > cluster multi_cluster enable vlan_name=Secondary
      sleep 900 (seems to take about 8min on average)

   Register MSSQL19-Profile source (U: Administrator P:Nutanix/4u, Instance: MSSQLSERVER)

      Looks like this can be done via API but not Era CLI:

      curl -k -X POST \
      	https://10.42.93.161/era/v0.9/dbservers/register \
      	-H 'Content-Type: application/json' \
      	-H 'Authorization: Basic YWRtaW46dGVjaFgyMDIxIQ==' \
      	-d \
      	'{"actionArguments":[{"name":"same_as_admin","value":true},{"name":"sql_login_used","value":false},{"name":"sysadmin_username_win","value":"Administrator"},{"name":"sysadmin_password_win","value":"Nutanix/4u"},{"name":"instance_name","value":"MSSQLSERVER"}],"vmIp":"10.42.93.64","nxClusterUuid":"79cb2c4e-1455-4798-aa4d-c53929e730ab","databaseType":"sqlserver_database","forcedInstall":true,"workingDirectory":"c:\\","username":"Administrator","password":"Nutanix/4u","eraDeployBase":"c:\\"}'

      Took ~3.5min on test cluster

   Create software profile for MSSQL19

      era > profile software create engine=sqlserver_database nx_cluster_id=79cb2c4e-1455-4798-aa4d-c53929e730ab dbserver_ip=10.42.93.64 name=MSSQL19 base_version_name=BASE_VERSION description="MSSQL 2019 on Windows Server 2019"

      Took ~2.5min on test cluster

AWS STAGING:

   Add AWS to Era

      Used 10.210.X.210 as EraAgent VM IP (as User VM Network range ends at 209 and EraManaged starts at 211)

      curl -k -X POST \
      https://10.42.93.210/era/v0.9/clusters \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Basic YWRtaW46dGVjaFgyMDIxIQ==' \
      -d \
      '{"clusterName":"AWS-Cluster","clusterDescription":"","clusterIP":"10.210.2.52","storageContainer":"SelfServiceContainer","agentVMPrefix":"EraAgent","port":9440,"protocol":"https","clusterType":"NTNX","version":"v2","credentialsInfo":[{"name":"username","value":"admin"},{"name":"password","value":"techX2021!"}],"agentNetworkInfo":[{"name":"vlanName","value":"User VM Network"},{"name":"dns","value":"10.210.0.2"},{"name":"staticIP","value":"10.210.2.210"},{"name":"gateway","value":"10.210.2.129"},{"name":"subnet","value":"255.255.255.128"},{"name":"ntp","value":"169.254.169.123"}]}'

      Took ~12 minutes on test cluster

   Create Era Managed network using 211-253 User VM Network range

      era > resource network add nx_cluster_id=8fba5661-75dd-4eef-b665-fb9e3d5e1544 name="User VM Network" ip_managed_in_era gateway=10.210.2.129 subnet_mask=255.255.255.128 primary_dns=10.42.93.41 start_ip=10.210.2.211 end_ip=10.210.2.253 dns_domain=ntnxlab.local

   Sync MSSQL19 software profile to AWS-Cluster

      Looks like you just need to profile name and both Era cluster UUIDs

      curl -k -X PUT \
   	https://10.42.93.210/era/v0.9/profiles/408aa71a-1b25-41c2-982c-e15cb31c79f0 \
   	-H 'Content-Type: application/json' \
   	-H 'Authorization: Basic YWRtaW46dGVjaFgyMDIxIQ==' \
   	-d \
   	'{"availableClusterIds":["f0717c40-85c6-4fc1-909a-625abea289e8","8fba5661-75dd-4eef-b665-fb9e3d5e1544"],"updateClusterAvailability":true,"name":"MSSQL_19_SYNCED","description":""}'

      Replication took 11~ min on the test cluster. I believe the profile should be ~18.5GiB





Era Domain profile NTNXLAB
Era AD auth, add SSP Operators group with all 3 roles
Add PE to Era
Create Era managed network 211-253 IP range

enable multi-cluster
Spin up 1 copy of source DB
register that DB server
Create software profile from that image

(AWS staging script) Add AWS PE to Era
(AWS staging script) Create Era managed network 210-253 IP range
(AWS staging script) replicate MSSQL software profile to AWS


USE CASE

https://portal.nutanix.com/page/documents/details?targetId=Nutanix-Era-User-Guide-v2_1:Nutanix-Era-User-Guide-v2_1

User with single instance on-prem app (Fiesta webserver/MSSQL DB VM/extra DBs in it)
Customer wants to build in more resiliency for app
Register source DBs (Fiesta)
Use Era to provision AAG across on-prem (2 sync copies) and AWS (1 async copy) - SE would manually import data afterwards ~60 minutes

Register Sample DB from same source VM
Add AWS-Cluster to Sample.DB time machine data access management
Clone Sample.db to another single instance VM (provisioned on AWS)

Use pre-provisioned source DB to do hammer DB stuff

Once AAG is done, update Fiesta webserver to point to AAG VIP
Fail primary AAG VM, confirm web app still works
Fail remaining on-prem AAG VM, log into AWS copy and make active - potential for data loss, but still have up time, need to speak to other considerations for webserver level HA (replicas/load balancers)

Once sample.db clone is done, patch that VM
