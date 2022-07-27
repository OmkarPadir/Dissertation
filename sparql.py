from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:7200/repositories/Dissertation")
sparql_insert = SPARQLWrapper("http://localhost:7200/repositories/Dissertation/statements")

def query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print("Results  ",results)
    return results

def insert(query):
    sparql_insert.setQuery(query)
    sparql_insert.method = 'POST'
    # sparql_insert.setReturnFormat(JSON)
    results = sparql_insert.query()#.convert()
    # print("Results  ",results)
    return results

def getValues(results):
    # print(results)
    # print(results['head']['vars'])
    message = []
    # message.append(results['head']['vars'])
    for i in results['results']['bindings']:
        temp = []
        for j in results['head']['vars']:
            temp.append (i[j]['value'].split('/')[-1])#str_mine.split('/')[-1]
        message.append(temp)
    # print(message)
    return message

def getStakeholders():
    sparql_query='''
        PREFIX Ir: <http://foo.example/IncidentReporting/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?st ?s where { 
    ?st rdfs:label ?s.
	?st rdfs:subClassOf Ir:Stakeholder.
    FILTER NOT EXISTS{?q rdfs:subClassOf Ir:Stakeholder. ?st rdfs:subClassOf ?q.}     
}

    '''
    results= query(sparql_query)
    return getValues(results)

def getStakeholdersIssues():
    sparql_query='''
    PREFIX Ir: <http://foo.example/IncidentReporting/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?st ?I where { 
       
    ?st rdfs:subClassOf Ir:Stakeholder .
	?IssueNode owl:allValuesFrom ?st.
    ?IssueClass rdfs:subClassOf	?IssueNode.
    ?I	rdf:type ?IssueNode.
    
}
'''
    results= query(sparql_query)
    res_arr = getValues(results)

    #Get Stakeholders
    Stakeholders = getStakeholders()
    StakeholderIssues={}
    for s in Stakeholders:
        temp=[]
        for r in res_arr:
            if s[0] == r[0]:
                temp.append(r[1])
        StakeholderIssues[s[0]] = temp

    # print(StakeholderIssues)
    return StakeholderIssues


def getIssueDescription(StakeholderIssues):

    sparqlQuery= '''
    PREFIX Ir: <http://foo.example/IncidentReporting/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?I ?desc where {
    ?I Ir:description ?desc.
    ?st rdfs:label ?stakeholder.    
    ?st rdfs:subClassOf Ir:Stakeholder .
	?IssueNode owl:allValuesFrom ?st.
    ?IssueClass rdfs:subClassOf	?IssueNode.
    ?I	rdf:type ?IssueNode.    
}

    '''

    results= query(sparqlQuery)
    res_arr = getValues(results)

    res_dict={}
    for t in res_arr:
        res_dict[t[0]] = t[1]

    # print(res_dict)

    return  res_dict


def is_filled(data):
    if data == None:
        return False
    if data == '':
        return False
    if data == []:
        return False
    if data=="nan":
        return False
    return True

def stakeholderImpactTriplet(Triplets,StakeholderList,ImpactList):
    if is_filled(StakeholderList):
        Triplets += ";\n\t Ir:hasStakeholder Ir:"+str(StakeholderList)
    if is_filled(ImpactList):
        for il in ImpactList:
            Triplets += ";\n\t Ir:hasImpact Ir:"+str(il)

    return Triplets

def InsertData(form):


    IncidentId= form.IncidentId.data
    IncidentYear= form.IncidentYear.data
    IncidentHeadline= form.IncidentHeadline.data
    AISystem= form.AISystem.data
    AIPurpose= form.AIPurpose.data
    IncidentURL= form.IncidentURL.data
    AIRegion= form.AIRegion.data
    AISector= form.AISector.data
    AIDeveloper= form.AIDeveloper.data
    AIOperator= form.AIOperator.data
    StakeholderList= form.StakeholderList.data
    ImpactList= form.ImpactList.raw_data

    SI2 = form.SI2.data
    StakeholderList2= form.StakeholderList2.data
    ImpactList2= form.ImpactList2.raw_data

    SI_arr = [True,SI2]
    StakeholderList_arr = [StakeholderList, StakeholderList2]
    ImpactList_arr = [ImpactList,ImpactList2]

    Triplets=""


    if is_filled(IncidentId):
        Triplets += "Ir:"+IncidentId+" a Ir:Incident"

        if is_filled(IncidentYear):
            Triplets += ";\n\t Ir:hasIncidentYear "+str(IncidentYear)


        if is_filled(IncidentHeadline):
            Triplets += ";\n\t Ir:hasHeadline \""+str(IncidentHeadline)+"\""
        if is_filled(AISystem):
            Triplets += ";\n\t Ir:hasSystem \""+str(AISystem)+"\""
        if is_filled(AIPurpose):
            Triplets += ";\n\t Ir:hasPurpose \""+str(AIPurpose)+"\""
        if is_filled(IncidentURL):
            Triplets += ";\n\t Ir:hasURL \""+str(IncidentURL)+"\""
        if is_filled(AIRegion):
            Triplets += ";\n\t Ir:hasIncidentRegion Ir:"+str(AIRegion)
        if is_filled(AISector):
            Triplets += ";\n\t Ir:applicationSector Ir:"+str(AISector)
        if is_filled(AIDeveloper):
            Triplets += ";\n\t Ir:developedBy Ir:"+str(AIDeveloper)
        if is_filled(AIOperator):
            Triplets += ";\n\t Ir:operatedBy Ir:"+str(AIOperator)

        for i in range(len(SI_arr)):
            if (SI_arr[i]):
                Triplets = stakeholderImpactTriplet(Triplets,StakeholderList_arr[i],ImpactList_arr[i])



    else:
        return False



    sparql_query = '''PREFIX Ir: <http://foo.example/IncidentReporting/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    INSERT DATA { ''' + Triplets +'''}  
    '''
    print("Query #",sparql_query,"#")

    res = insert(sparql_query)
    print("res: " ,str(res))

    return True


#
# PREFIX Ir: <http://foo.example/IncidentReporting/>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#
# INSERT DATA {
#     Ir:AIAAIC0870 a Ir:Incident;
# Ir:hasIncidentYear 2022;
# Ir:hasHeadline "Tesla Smart Summon";
# Ir:hasPurpose "Summon car";
# Ir:hasSystem "Smart Summon";
# Ir:hasURL "https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/tesla-smart-summon#h.4mjdwgbvxyyc";
#
# Ir:hasIncidentRegion Ir:USA;
# Ir:developedBy Ir:Tesla;
# Ir:operatedBy Ir:Tesla;
# Ir:applicationSector Ir:Automotive;
#
# Ir:hasStakeholder Ir:FairOperationsStakeholder;
# Ir:hasImpact Ir:PropertyRights;
#
# Ir:hasStakeholder Ir:Consumers;
# Ir:hasImpact Ir:Fairinformation;
# }