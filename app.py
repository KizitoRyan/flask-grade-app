from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grades.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class GradeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score1 = db.Column(db.Float, nullable=False)
    score2 = db.Column(db.Float, nullable=False)
    score3 = db.Column(db.Float, nullable=False)
    average = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def calculate_grade(avg):
    if avg >= 80: return "A"
    elif avg >= 70: return "B"
    elif avg >= 60: return "C"
    elif avg >= 50: return "D"
    else: return "F"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    scores = [float(request.form.get(f"score{i}")) for i in range(1, 4)]
    avg = round(sum(scores) / len(scores), 1)
    grade = calculate_grade(avg)
    record = GradeRecord(name=name, score1=scores[0], score2=scores[1], score3=scores[2], average=avg, grade=grade)
    db.session.add(record)
    db.session.commit()
    return render_template("result.html", name=name, score1=scores[0], score2=scores[1], score3=scores[2], avg=avg, grade=grade)

@app.route("/history")
def history():
    records = GradeRecord.query.order_by(GradeRecord.created_at.desc()).all()
    return render_template("history.html", records=records)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
