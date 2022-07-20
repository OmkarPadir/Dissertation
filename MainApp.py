from flask import Flask, render_template, jsonify, request
import sparql
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

Stakeholders = sparql.getStakeholders()
StakeholderIssues = sparql.getStakeholdersIssues()
IssueDescription = sparql.getIssueDescription(StakeholderIssues)

@app.route('/', methods=['GET', 'POST'])
def index():
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
        # if form.validate_on_submit():
        #     print(form.ImpactList2.data)
            res = sparql.InsertData(form)
            return "SUCESS"

        # else:
        #     return "Incident Id required"
    return render_template('Annotation.html', messages=messages, form = form)

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

