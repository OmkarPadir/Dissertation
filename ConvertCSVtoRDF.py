# Import pandas
import pandas as pd
import sparql

#Create Property Datatypes
datatypes={"hasHeadline":"String",
           "hasIncidentYear":"Integer",
           "hasIncidentRegion":"Class",
           "applicationSector":"Class",
           "hasSystem":"String",
           "operatedBy":"Class",
           "developedBy":"Class",
           "hasPurpose":"String",
           "hasURL":"String",
           "hasStakeholder":"Class",
           "hasImpact":"Class",
           "Comments":"String"}

# Load the xlsx file
excel_data = pd.read_excel('AnnotationData.xlsx')
# Read the values of the file in the dataframe
data = pd.DataFrame(excel_data)
# Print the content
# print("The content of the file is:\n", data)
data = data.where(pd.notnull(data), None)
data.set_index("Incident", drop=True, inplace=True)

dictionary = data.to_dict(orient="index")


f = open("TurtleData.ttl", "w")


Turtle_headers = '''PREFIX Ir: <http://foo.example/IncidentReporting/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''
f.write(Turtle_headers)

def sp_char_replace(string_data):
    return str(string_data).replace("/","_").replace(" ","_").replace(",","_").replace("(","_").replace(")","_")

for incident in dictionary:
    # print(incident)
    # print(dictionary[incident])



    # incident="AIAAIC0864"
    IncidentData = dictionary[incident]
    # print(IncidentData)

    Triplet='''
    Ir:'''+incident+''' a Ir:Incident'''
    for property in IncidentData:
        if sparql.is_filled(IncidentData[property]):
            property_name = property.split(".")[0]
            data_to_insert = str(IncidentData[property]).split(";")
            for dti in data_to_insert:
                dti=dti.strip()
                if(datatypes[property_name]=="Class"):
                    Triplet+=''';\n\tIr:'''+property_name+''' Ir:'''+sp_char_replace(dti)
                if(datatypes[property_name]=="String"):
                    Triplet+=''';\n\tIr:'''+property_name+''' "'''+str(dti).replace("\n","")+'''"'''
                if(datatypes[property_name]=="Integer"):
                    Triplet+=''';\n\tIr:'''+property_name+''' '''+str(dti)

    Triplet+='''.\n'''

    print(Triplet)

    f.write(Triplet)

f.close()