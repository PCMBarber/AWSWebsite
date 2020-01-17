from application import db, login_manager
from flask_login import UserMixin

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return ''.join(['User ID: ', str(self.id), '\r\n',
            'User Name: ', self.first_name, '\r\n',
            'Name: ', self.first_name, ' ', self.last_name, '\r\n',
            'Admin? ', str(self.admin)
        ])

    @login_manager.user_loader
    def load_user(id):
        return users.query.get(int(id)) 

class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forum = db.Column(db.String(30), nullable=False)
    thread = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False, unique=True)
    content = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return ''.join(['Post ID: ', str(self.id), '\r\n',
            'Forum: ', self.forum, '\r\n',
            'Thread: ', self.thread, '\r\n',
            'Content: ', self.content, '\r\n',
            'Image: ', self.image
        ])
