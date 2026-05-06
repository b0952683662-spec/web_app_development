from app import db


class Ingredient(db.Model):
    """食材模型"""
    __tablename__ = 'ingredients'

    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(100), nullable=False)
    amount    = db.Column(db.String(50))               # 份量（如：2顆、100g）
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'),
                          nullable=False)

    # ── CRUD 方法 ─────────────────────────────────────────────
    @classmethod
    def create(cls, name: str, recipe_id: int, amount: str = None):
        ingredient = cls(name=name, amount=amount, recipe_id=recipe_id)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient

    @classmethod
    def bulk_create(cls, items: list, recipe_id: int):
        """
        批次新增食材
        items: [{'name': '雞蛋', 'amount': '2顆'}, ...]
        """
        ingredients = [
            cls(name=item['name'], amount=item.get('amount'), recipe_id=recipe_id)
            for item in items
        ]
        db.session.bulk_save_objects(ingredients)
        db.session.commit()
        return ingredients

    @classmethod
    def get_by_recipe(cls, recipe_id: int):
        return cls.query.filter_by(recipe_id=recipe_id).all()

    @classmethod
    def delete_by_recipe(cls, recipe_id: int):
        """刪除某食譜的所有食材（用於重新整批更新）"""
        cls.query.filter_by(recipe_id=recipe_id).delete()
        db.session.commit()

    def __repr__(self):
        return f'<Ingredient {self.name} {self.amount}>'
