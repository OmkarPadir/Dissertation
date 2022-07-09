# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():
#    return 'Hello World'
# # app.add_url_rule('/', 'hello', hello_world)
#
# @app.route('/Omkar')
# def Omkar():
#     return 'Hello Omkar'
#
# @app.route('/hello/<name>')
# def hello_name(name):
#    return 'Hello '+str(name)
#
# if __name__ == '__main__':
#    app.run()

######## Template excercise ###########
# from flask import Flask, render_template
# app = Flask(__name__)
#
# @app.route('/hello/<user>')
# def hello_name(user):
#    return render_template('hello.html', name = user)
#
# @app.route("/")
# def index():
#    return render_template("index.html")
#
# if __name__ == '__main__':
#    app.run(debug = True)


#### Form Example student
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)