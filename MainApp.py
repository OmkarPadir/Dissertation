from flask import Flask, render_template
import sparql
app = Flask(__name__)

# query1='''select * where {
# 	?s a <http://foo.example/IncidentReporting/Incident>.
#     ?s ?o ?p.
# } limit 100'''
#
# results = sparql.query(query1)
# print(results)

@app.route('/')
def index():
    Stakeholders = sparql.getStakeholders()
    StakeholderIssues = sparql.getStakeholdersIssues()
    # print(StakeholderIssues)
    messages={"Stakeholders":Stakeholders,
              "Stake_len":len(Stakeholders)}
    print("Messages: ",messages)
    return render_template('Annotation.html', messages=messages)

if __name__ == '__main__':
   app.run()

