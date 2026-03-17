from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()


ADMIN_USERNAME = "prince"
ADMIN_PASSWORD = "@9998pc"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from datetime import datetime
        new_admission = Admission(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            grade=request.form['grade'],
            subject=request.form['subject'],
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        db.session.add(new_admission)
        db.session.commit()
        flash('Application Submitted Successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials!', 'error')
    
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    admissions = Admission.query.order_by(Admission.id.desc()).all()
    total = len(admissions)
    
    return render_template('dashboard.html', admissions=admissions, total=total)

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    admission = Admission.query.get(id)
    if admission:
        db.session.delete(admission)
        db.session.commit()
        flash('Application deleted successfully!', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)