from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index= True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(120))
    
    def set_password(self, passwd):
        self.password_hash = generate_password_hash(passwd, "sha256")
    def check_password(self, passwd):
        return check_password_hash(self.password_hash, passwd)



    def __repr__(self):
        return f'<user : {self.username}>'  