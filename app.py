from flask import Flask, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///feedback.db"
app.config['SQLALCHEMY_TRACK_MIDIFIACTION'] = False
db = SQLAlchemy(app)


class Feedback(db.Model):
    # __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text())

    def __init__(self, student, location, rating, comment):
        self.student = student
        self.location = location
        self.rating = rating
        self.comment = comment


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        student = request.form["st_name"]
        location = request.form["loc"]
        rating = request.form["rating"]
        comments = request.form["comments"]

        if db.session.query(Feedback).filter(Feedback.student == student).count() == 0:
            feedback = Feedback(student=student, location=location,
                                rating=rating, comment=comments)
            db.session.add(feedback)
            db.session.commit()
            return render_template("success.html")
        return render_template("index.html", message="You have already submitted Feedback!!")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
