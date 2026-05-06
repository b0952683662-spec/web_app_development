from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    """使用者模型"""
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), nullable=False, unique=True)
    email         = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role          = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    created_at    = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # 關聯：一個 User 有多個 Recipe
    recipes = db.relationship('Recipe', backref='author', lazy=True,
                              cascade='all, delete-orphan')

    # ── 密碼處理 ──────────────────────────────────────────────
    def set_password(self, password: str):
        """將明文密碼加密後存入 password_hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """驗證明文密碼是否與 hash 相符"""
        return check_password_hash(self.password_hash, password)

    # ── 屬性 ──────────────────────────────────────────────────
    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'

    # ── CRUD 方法 ─────────────────────────────────────────────
    @classmethod
    def create(cls, username: str, email: str, password: str, role: str = 'user'):
        user = cls(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, user_id: int):
        return cls.query.get_or_404(user_id)

    @classmethod
    def get_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'password':
                self.set_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
