from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MultiCheckboxField2(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class IncidentForm(FlaskForm):
    IncidentId = StringField('Incident Id:',validators=[DataRequired()])
    IncidentYear = IntegerField('Incident Year:')
    IncidentHeadline = StringField('Incident Headline:')
    AISystem = StringField('AI System:')
    AIPurpose = StringField('AI Purpose:')
    IncidentURL = StringField('URL:')

    AIRegion = StringField('Region:')
    AISector = StringField('Sector:')
    AIDeveloper = StringField('Developer:')
    AIOperator = StringField('Operator:')

    #Stakeholder and Impact Elements

    StakeholderList = SelectField('Stakeholder', choices = [])
    ImpactList = MultiCheckboxField('Impacts', choices = [])

    SI2 = BooleanField("SI2")
    StakeholderList2 = SelectField('Stakeholder', choices = [])
    ImpactList2 = MultiCheckboxField('Impacts', choices = [])

    submit = SubmitField('Save')
