from flask import Blueprint

recipes_bp = Blueprint('recipes', __name__, url_prefix='/')

@recipes_bp.route('/', methods=['GET'])
def index():
    """
    首頁 / 食譜列表頁。
    處理分頁 (page)、難度篩選 (difficulty) 與分類篩選 (category_id)，
    渲染 index.html
    """
    pass

@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    食譜詳細資訊頁。
    顯示特定食譜的食材與步驟，找不到時回傳 404，渲染 recipes/detail.html
    """
    pass

@recipes_bp.route('/recipes/create', methods=['GET', 'POST'])
def create():
    """
    新增食譜頁面與執行。需登入。
    GET: 渲染 recipes/create.html
    POST: 儲存食譜、食材、步驟，並處理封面圖片上傳，成功則重導向
    """
    pass

@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit(recipe_id):
    """
    編輯食譜頁面與執行。僅限原作者或管理員。
    GET: 將食譜原資料預填於表單並渲染 recipes/edit.html
    POST: 接收表單並更新 DB，成功則重導向
    """
    pass

@recipes_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete(recipe_id):
    """
    刪除食譜。僅限原作者或管理員。
    刪除 DB 紀錄與圖片，成功後重導向至首頁
    """
    pass
