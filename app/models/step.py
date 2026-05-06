from app import db


class Step(db.Model):
    """烹飪步驟模型"""
    __tablename__ = 'steps'

    id        = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.Integer, nullable=False)    # 步驟順序，從 1 開始
    content   = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'),
                          nullable=False)

    # ── CRUD 方法 ─────────────────────────────────────────────
    @classmethod
    def create(cls, order_num: int, content: str, recipe_id: int):
        step = cls(order_num=order_num, content=content, recipe_id=recipe_id)
        db.session.add(step)
        db.session.commit()
        return step

    @classmethod
    def bulk_create(cls, contents: list, recipe_id: int):
        """
        批次新增步驟
        contents: ['將水煮沸', '加入鹽巴', ...]（依序從 1 開始編號）
        """
        steps = [
            cls(order_num=i + 1, content=content, recipe_id=recipe_id)
            for i, content in enumerate(contents)
        ]
        db.session.bulk_save_objects(steps)
        db.session.commit()
        return steps

    @classmethod
    def get_by_recipe(cls, recipe_id: int):
        return cls.query.filter_by(recipe_id=recipe_id).order_by(cls.order_num).all()

    @classmethod
    def delete_by_recipe(cls, recipe_id: int):
        """刪除某食譜的所有步驟（用於重新整批更新）"""
        cls.query.filter_by(recipe_id=recipe_id).delete()
        db.session.commit()

    def __repr__(self):
        return f'<Step {self.order_num}: {self.content[:30]}>'
