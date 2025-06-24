from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db  # same db instance used in app.py

contact_bp = Blueprint("contact", __name__, static_folder="static", template_folder="templates")

class Contact(db.Model):  # same database instance
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('contact.html')
