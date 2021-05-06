import re

outputFile = open("c:\\Users\\Matt\\Git\\nutanixworkshops\\gts21\\reporting\\GTS_EMEA_Inspection.txt","w")
outliersFile = open("c:\\Users\\Matt\\Git\\nutanixworkshops\\gts21\\reporting\\GTS_EMEA_Inspection-outliers.txt","w")
inputFile = open("c:\\Users\\Matt\\Git\\nutanixworkshops\\gts21\\reporting\\VM_Dump_GTS_EMEA-trimmed.txt","r")
vmData = inputFile.readlines()
clusterIp = []
userId = []
lab= []

for line in vmData:

    # Update cluster IP
    if "Dumping the VMs on" in line:
        clusterIP = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line).group(0)
    
    # Extract 
    elif "user" in line.lower():
        try:
            user = re.search(r'(USER\d{1,2})', line, re.IGNORECASE).group(0)
            userId = user[-1]
        except:
            outliersFile.write(clusterIP + "-" + line + "\n")

        if "centos" in line.lower():
            try:
                outputFile.write(clusterIP + "-" + userId + "-iaas\n")
            except:
                outliersFile.write(clusterIP + "-" + line)

        elif "karbon" in line.lower():
            try:
                outputFile.write(clusterIP + "-" + userId + "-karbon\n")
            except:
                outliersFile.write(clusterIP + "-" + line)

        elif "onprem" in line.lower():
            try:
                outputFile.write(clusterIP + "-" + userId + "-euc\n")
            except:
                outliersFile.write(clusterIP + "-" + line)

        elif "drone" in line.lower():
            try:
                outputFile.write(clusterIP + "-" + userId + "-cicd\n")
            except:
                outliersFile.write(clusterIP + "-" + line)

        elif "sqlag" in line.lower():
            try:
                outputFile.write(clusterIP + "-" + userId + "-dbs\n")
            except:
                outliersFile.write(clusterIP + "-" + line)

    # Print outliers
    else:
        outliersFile.write(clusterIP + "-" + line)


        

        


    