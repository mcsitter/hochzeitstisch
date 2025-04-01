from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gifts.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    image_file = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    price_per_piece = db.Column(db.Float, nullable=True)
    collected_amount = db.Column(db.Float, default=0.0)

@app.route('/')
def index():
    gifts = Gift.query.all()
    return render_template('index.html', gifts=gifts)

@app.route('/add_gift', methods=['POST'])
def add_gift():
    name = request.form['name']
    image = request.form.get('image') or None
    image_file = None
    if 'image_file' in request.files:
        file = request.files['image_file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file = filename
    link = request.form.get('link') or None
    try:
        price = float(request.form['price'])
    except ValueError:
        price = 0.0
    price_per_piece = float(request.form.get('price_per_piece') or 0.0)
    new_gift = Gift(name=name, image=image, image_file=image_file, link=link, price=price, price_per_piece=price_per_piece)
    db.session.add(new_gift)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/contribute/<int:gift_id>', methods=['POST'])
def contribute(gift_id):
    gift = Gift.query.get_or_404(gift_id)
    amount = float(request.form['amount'])
    if gift.collected_amount + amount <= gift.price:
        gift.collected_amount += amount
        db.session.commit()
    return redirect(url_for('index'))

def upgrade_db():
    with app.app_context():
        # Check if the new columns exist, if not, add them
        if not hasattr(Gift, 'image'):
            db.engine.execute('ALTER TABLE gift ADD COLUMN image STRING(200)')
        if not hasattr(Gift, 'link'):
            db.engine.execute('ALTER TABLE gift ADD COLUMN link STRING(200)')
        if not hasattr(Gift, 'price'):
            db.engine.execute('ALTER TABLE gift ADD COLUMN price FLOAT')
        if not hasattr(Gift, 'price_per_piece'):
            db.engine.execute('ALTER TABLE gift ADD COLUMN price_per_piece FLOAT')
        if not hasattr(Gift, 'image_file'):
            db.engine.execute('ALTER TABLE gift ADD COLUMN image_file STRING(200)')
        if hasattr(Gift, 'total_amount'):
            db.engine.execute('ALTER TABLE gift DROP COLUMN total_amount')

if __name__ == '__main__':
    upgrade_db()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
