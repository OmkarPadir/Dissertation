from flask import Flask, render_template, jsonify, request
import sparql
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

Stakeholders = sparql.getStakeholders()
StakeholderIssues = sparql.getStakeholdersIssues()
IssueDescription = sparql.getIssueDescription(StakeholderIssues)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # print(StakeholderIssues)
#     messages={"Stakeholders":Stakeholders,
#               "Stake_len":len(Stakeholders),
#               "StakeholderIssues":StakeholderIssues,
#               "IssueDescription" : IssueDescription
#               }
#     print("Messages: ",messages)
#     return render_template('Annotation.html', messages=messages)

@app.route('/annotate', methods=['GET', 'POST'])
def annotate_handler():

    # print(StakeholderIssues)
    messages={"Stakeholders":Stakeholders,
              "Stake_len":len(Stakeholders),
              "StakeholderIssues":StakeholderIssues,
              "IssueDescription" : IssueDescription
              }
    print("Messages: ",messages)

    #Create Stakeholder tuple for form choices
    Stakeholderchoices= [(c[0], c[1]) for c in Stakeholders]
    Impactchoices = [(c, c) for c in StakeholderIssues['Community']]

    form = IncidentForm()
    form.StakeholderList.choices = Stakeholderchoices
    form.ImpactList.choices = Impactchoices

    form.StakeholderList2.choices = Stakeholderchoices
    form.ImpactList2.choices = Impactchoices


    if request.method=="POST":
        res = sparql.InsertData(form)
        return render_template('/Success_page.html', messages=messages)

    return render_template('/annotate_form.html', messages=messages, form = form)

app.add_url_rule('/', 'annotate', annotate_handler)


@app.route('/search', methods=['GET', 'POST'])
def search_handler():

    # print(StakeholderIssues)
    messages={"Stakeholders":Stakeholders,
              "Stake_len":len(Stakeholders),
              "StakeholderIssues":StakeholderIssues,
              "IssueDescription" : IssueDescription
              }
    print("Messages: ",messages)

    #Create Stakeholder tuple for form choices
    Stakeholderchoices= [(c[0], c[1]) for c in Stakeholders]
    Impactchoices = [(c, c) for c in StakeholderIssues['Community']]


    search_form = SearchForm()
    search_form.Search_StakeholderList.choices = Stakeholderchoices
    search_form.Search_ImpactList.choices = Impactchoices

    print("Inside Search")

    if request.method=="POST":
        # res = sparql.InsertData(form)
        return "Search SUCCESS"

    return render_template('/search.html', messages=messages, search_form=search_form)

@app.route('/impact/<stakeholder>')
def impact(stakeholder):
    Impactchoices = {c:c for c in StakeholderIssues[stakeholder]}

    ImpactArray = []
    for impact in StakeholderIssues[stakeholder]:
        impactObj = {}
        impactObj['id'] = impact
        impactObj['name'] = impact
        ImpactArray.append(impactObj)

    return jsonify(ImpactArray)

if __name__ == '__main__':
   app.run()

