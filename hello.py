from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

db = SQLAlchemy(app)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow())

def __repr__(self):
    return '<name %r>' % self.id

subscribers = []
@app.route('/friends', methods=['POST', 'GET'])
def friends():
    title = 'My friends list'

    if request.method == 'POST':
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "there was a error adding your friend"
    else:
        friends = Friends.query.order_by(Friends.date_created)

        return render_template('friends.html', title=title, friends=friends)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    title = 'Update'
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "there was a error adding your friend"
    else:
        return render_template('update.html', friend_to_update=friend_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "there was a error deleting your friend"

@app.route('/')
def home():  # put application's code here
    favorite_pizza = ["pepperoni", "Chesse", "Mushrooms", 41]
    return render_template("home.html", favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/subscribe')
def subscribe():
    error_statement = ''
    title = 'Subscribe to my email newsletter'
    return render_template("subscribe.html", title=title, error_statement=error_statement)

@app.route('/success',methods=["POST"])
def success():
    error_statement = ''
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    if not first_name or not last_name or not email:
        error_statement = "All form fields are required"
        return render_template("subscribe.html", first_name=first_name, last_name=last_name,email =email, error_statement=error_statement)



    subscribers.append(first_name + " " + last_name + " " + email)
    title = 'Thank you!'
    return render_template("success.html", first_name = first_name, last_name = last_name, email = email, subscribers = subscribers)

