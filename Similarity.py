import sparql
from scipy.spatial import distance
Attributes=["hasIncidentRegion","applicationSector","developedBy","hasStakeholder","hasImpact"]#,"operatedBy"
AllIncidents={}
VectorHeaders=[]

def initialize():

    Stakeholders = sparql.getStakeholders()
    StakeholderIssues = sparql.getStakeholdersIssues()
    Regions = sparql.getDistinctValues("hasIncidentRegion")
    AppSector = sparql.getDistinctValues("applicationSector")
    OpBy = sparql.getDistinctValues("operatedBy")
    DevBy = sparql.getDistinctValues("developedBy")

    AllStakeholders=[]
    AllIssues=[]
    AllRegions=[]
    AllSector=[]
    AllOpBy=[]
    AllDevBy=[]

    for i in Stakeholders:
        AllStakeholders.append(i[0])
    for j in StakeholderIssues:
        AllIssues=AllIssues+(StakeholderIssues[j])
    for i in Regions:
        AllRegions.append(i[0])
    for i in AppSector:
        AllSector.append(i[0])
    for i in OpBy:
        AllOpBy.append(i[0])
    for i in DevBy:
        AllDevBy.append(i[0])

    # print(AllStakeholders)
    # print(AllIssues)
    # print(AllRegions)
    # print(AllSector)
    # print(AllOpBy)
    # print(AllDevBy)

    VectorHeaders=AllStakeholders+AllIssues+AllRegions+AllSector+AllDevBy#+AllOpBy

    print(VectorHeaders)

    IncidentData = sparql.getAllIncidentData()
    print(IncidentData)



    Empty=[]
    for i in range(len(VectorHeaders)):
        Empty.append(0)
    print(Empty)

    for i in IncidentData:
        AllIncidents[i[0]]=Empty.copy()
    print(AllIncidents)

    for i in IncidentData:
        if(i[1] in Attributes):
            print(i)
            #Index of the attribute value in header
            if(i[2] in VectorHeaders):
                index = VectorHeaders.index(i[2])
                arr = AllIncidents[i[0]]
                arr[index]=1
                AllIncidents[i[0]] = arr
    print(AllIncidents)

# from math import dist
#(AllIncidents['AIAAIC0870'],AllIncidents['AIAAIC0864'])

def getSimilarIncidents(Incident):


    Distance_Thresh=100
    Count_Thresh = 20
    SimilarList={}
    count=0
    a = AllIncidents[Incident]#[1, 1, 0]
    for i in AllIncidents.keys():
        if i != Incident:

            b = AllIncidents[i]#[0, 0, 1]
            dst = distance.euclidean(a, b)
            print(i,dst)
            if(dst < Distance_Thresh):
                # SimilarList.append([i,dst])
                SimilarList[i]=dst
                count+=1
                if count==Count_Thresh:
                    break
    sorted_arr =[]
    sorted_keys = sorted(SimilarList, key=SimilarList.get)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_arr.append( [w,SimilarList[w]])



    return sorted_arr



# initialize()
# print(getSimilarIncidents("AIAAIC0800"))