from flask import Flask, render_template, flash, request, url_for, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import twitter
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    username = TextField('Username:', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    #print(int form.errors)
    if request.method == 'POST':
        username=request.form['username']
        #print username
 
        if form.validate():
            # Save the comment here.
            flash('Hello ' + username)
            try:
                twitter.get_all_tweets(username)
                return redirect(url_for('twitterfeed'))
            except Exception as e:
                print(str(e))
                flash('Cannot Access Twitter feed for ' + username)
            
        else:
            flash('All the form fields are required. ')
 
    return render_template('hello.html', form=form)

@app.route('/twitterfeed')
def twitterfeed():
    with open("imagelabels.txt") as f:
        labels = f.readlines()

    return render_template('twitterfeed.html', your_list=labels, your_video='video.mp4')
 
if __name__ == "__main__":
    app.run()
