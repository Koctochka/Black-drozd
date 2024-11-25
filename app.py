from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ornithology.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    observations = db.relationship('Observation', backref='observer', lazy=True)

class Bird(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    habitat = db.Column(db.String(100))
    observations = db.relationship('Observation', backref='bird', lazy=True)

class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bird_id = db.Column(db.Integer, db.ForeignKey('bird.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text)
    image_url = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    birds = Bird.query.all()
    observations = Observation.query.order_by(Observation.date.desc()).limit(3).all()
    return render_template('index.html', birds=birds, observations=observations)

@app.route('/birds')
def birds():
    birds = Bird.query.all()
    return render_template('birds.html', birds=birds)

@app.route('/observations')
@login_required
def observations():
    observations = Observation.query.order_by(Observation.date.desc()).all()
    return render_template('observations.html', observations=observations)

@app.route('/add_observation', methods=['GET', 'POST'])
@login_required
def add_observation():
    if request.method == 'POST':
        bird_id = request.form.get('bird_id')
        location = request.form.get('location')
        notes = request.form.get('notes')
        image_url = request.form.get('image_url')

        observation = Observation(
            user_id=current_user.id,
            bird_id=bird_id,
            location=location,
            notes=notes,
            image_url=image_url
        )
        db.session.add(observation)
        db.session.commit()
        flash('Наблюдение успешно добавлено!', 'success')
        return redirect(url_for('observations'))

    birds = Bird.query.all()
    return render_template('add_observation.html', birds=birds)

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Это имя пользователя уже занято', 'error')
            return render_template('register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Этот email уже зарегистрирован', 'error')
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль', 'error')
    return render_template('login.html')

@app.route('/edit_observation/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_observation(id):
    observation = Observation.query.get_or_404(id)
    if observation.user_id != current_user.id:
        flash('У вас нет прав для редактирования этого наблюдения', 'error')
        return redirect(url_for('observations'))
        
    if request.method == 'POST':
        observation.location = request.form.get('location')
        observation.notes = request.form.get('notes')
        observation.image_url = request.form.get('image_url')
        
        db.session.commit()
        flash('Наблюдение успешно обновлено', 'success')
        return redirect(url_for('observations'))
        
    return render_template('edit_observation.html', observation=observation)

@app.route('/delete_observation/<int:id>')
@login_required
def delete_observation(id):
    observation = Observation.query.get_or_404(id)
    if observation.user_id != current_user.id:
        flash('У вас нет прав для удаления этого наблюдения', 'error')
        return redirect(url_for('observations'))
        
    db.session.delete(observation)
    db.session.commit()
    flash('Наблюдение успешно удалено', 'success')
    return redirect(url_for('observations'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
