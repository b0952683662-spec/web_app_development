from app import db


class Category(db.Model):
    """分類標籤模型"""
    __tablename__ = 'categories'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # ── CRUD 方法 ─────────────────────────────────────────────
    @classmethod
    def create(cls, name: str):
        category = cls(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, category_id: int):
        return cls.query.get_or_404(category_id)

    @classmethod
    def get_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def update(self, name: str):
        self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Category {self.name}>'
