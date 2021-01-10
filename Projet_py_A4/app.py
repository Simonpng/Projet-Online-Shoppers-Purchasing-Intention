
from flask import Flask, render_template,request,redirect,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField,IntegerField, SelectField,SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange

app=Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"]="hard to guess string"


class enteryourinput(FlaskForm):



	Administrative=FloatField("Administrative (0 to 27)",validators=[DataRequired(),NumberRange(min=-0.001,max=28)])
	Administrative_Duration = FloatField("Administrative_Duration (0 to 4000)",validators=[DataRequired(),NumberRange(min=-0.001,max=4001)])
	Informational=FloatField("Informational(integer 0 to 24)",validators=[DataRequired(),NumberRange(min=-1,max=25)])
	ProductRelated=FloatField("Product Related (integer 0 to 705)",validators=[DataRequired(),NumberRange(min=-1,max=706)])    
	ProductRelated_Duration = FloatField("ProductRelated_Duration (0 to 63974)",validators=[DataRequired(),NumberRange(min=-0.001,max=63975)])
	ExitRates = FloatField("ExitRates (0 to 0.5)",validators=[DataRequired(),NumberRange(min=-0.001,max=0.51)])    
	PageValues=FloatField("Page Values (0 to 362)",validators=[DataRequired(),NumberRange(min=-0.001,max=363)])
	SpecialDay = FloatField("SpecialDay (0 to 2)",validators=[DataRequired(),NumberRange(min=-0.001,max=3)])
	Month = FloatField("Month",validators=[DataRequired()])
	OperatingSystems = FloatField("OperatingSystems (integer 1 to 8)",validators=[DataRequired(),NumberRange(min=0,max=9)])
	Browser = FloatField("Browser(integer 1 to 13)",validators=[DataRequired(),NumberRange(min=0,max=13)])
	VisitorType = FloatField("VisitorType (integer 0 to 2)",validators=[DataRequired(),NumberRange(min=-1,max=3)])
	#Weekend = FloatField("Weekend",validators=[DataRequired()])
	submit=SubmitField("Soumettre")




@app.route('/',methods=["GET","POST"])
def prediction():
	form=enteryourinput()
	if request.method=="POST" and form.validate_on_submit():
		import joblib
		load_model=joblib.load("./OnlineShoppersPurchasingIntention.joblib")
		prediction=load_model.predict([[ form.Administrative.data, form.Administrative_Duration.data, form.Informational.data, form.ProductRelated.data, form.ProductRelated_Duration.data, form.ExitRates.data, form.PageValues.data, form.SpecialDay.data, form.Month.data, form.OperatingSystems.data, form.Browser.data, form.VisitorType.data, form.submit.data]]).tolist()
		session["result"]=prediction
		return redirect ("/results")
	return render_template('main.html',form=form)

@app.route('/results')
def show_result():
	pred=session["result"]
	return render_template('result.html',pred=pred)


if __name__ == '__main__':
	print(app.url_map)
	app.run(host='127.0.0.1',port=5000,debug=True)