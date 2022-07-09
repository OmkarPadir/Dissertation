from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:7200/repositories/Dissertation")

def query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
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
            temp.append (i[j]['value'])
        message.append(temp)
    # print(message)
    return message

def getStakeholders():
    sparql_query='''
    PREFIX Ir: <http://foo.example/IncidentReporting/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select * where { 
        ?stakeholder rdfs:subClassOf Ir:Stakeholder .
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
    select ?stakeholder ?Issue where { 
    ?stakeholder rdfs:subClassOf Ir:Stakeholder .
	?IssueNode owl:allValuesFrom ?stakeholder.
    ?IssueClass rdfs:subClassOf	?IssueNode.
    ?Issue	rdf:type ?IssueNode
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
