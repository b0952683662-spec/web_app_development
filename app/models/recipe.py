from app import db
from datetime import datetime

# ── 多對多中間表 ─────────────────────────────────────────────
recipe_category = db.Table(
    'recipe_category',
    db.Column('recipe_id',   db.Integer, db.ForeignKey('recipes.id',    ondelete='CASCADE'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)


class Recipe(db.Model):
    """食譜模型"""
    __tablename__ = 'recipes'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty  = db.Column(db.Integer, nullable=False)   # 1（新手）~ 5（進階）
    cook_time   = db.Column(db.Integer)                   # 分鐘
    image_path  = db.Column(db.String(300))               # 相對於 static/uploads/
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                            onupdate=datetime.utcnow)

    # 關聯
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True,
                                  cascade='all, delete-orphan')
    steps       = db.relationship('Step', backref='recipe', lazy=True,
                                  order_by='Step.order_num',
                                  cascade='all, delete-orphan')
    categories  = db.relationship('Category', secondary=recipe_category,
                                  backref=db.backref('recipes', lazy='dynamic'))

    # ── 難度文字標籤 ───────────────────────────────────────────
    DIFFICULTY_LABELS = {1: '新手', 2: '初級', 3: '中級', 4: '高級', 5: '進階'}

    @property
    def difficulty_label(self) -> str:
        return self.DIFFICULTY_LABELS.get(self.difficulty, '未知')

    # ── CRUD 方法 ─────────────────────────────────────────────
    @classmethod
    def create(cls, title, difficulty, user_id, description=None,
               cook_time=None, image_path=None):
        recipe = cls(
            title=title,
            description=description,
            difficulty=difficulty,
            cook_time=cook_time,
            image_path=image_path,
            user_id=user_id
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @classmethod
    def get_all(cls, difficulty=None, category_id=None, page=1, per_page=12):
        """取得食譜列表，支援難度與分類篩選及分頁"""
        query = cls.query
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        if category_id:
            query = query.filter(cls.categories.any(id=category_id))
        return query.order_by(cls.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @classmethod
    def get_by_id(cls, recipe_id: int):
        return cls.query.get_or_404(recipe_id)

    @classmethod
    def search_by_keyword(cls, keyword: str, page=1, per_page=12):
        """依關鍵字搜尋食譜名稱或描述"""
        return cls.query.filter(
            db.or_(
                cls.title.ilike(f'%{keyword}%'),
                cls.description.ilike(f'%{keyword}%')
            )
        ).order_by(cls.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @classmethod
    def search_by_ingredients(cls, ingredient_names: list):
        """
        依食材組合搜尋食譜，回傳 list of (Recipe, match_score)
        match_score = 符合食材數 / 食譜食材總數
        """
        ingredient_names_lower = [n.lower().strip() for n in ingredient_names]
        all_recipes = cls.query.all()
        results = []
        for recipe in all_recipes:
            recipe_ingr = [i.name.lower().strip() for i in recipe.ingredients]
            if not recipe_ingr:
                continue
            matched = sum(1 for name in recipe_ingr if name in ingredient_names_lower)
            if matched > 0:
                score = matched / len(recipe_ingr)
                results.append((recipe, matched, len(recipe_ingr), round(score * 100)))
        # 依符合度由高到低排序
        results.sort(key=lambda x: x[3], reverse=True)
        return results

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Recipe {self.title} (difficulty={self.difficulty})>'
