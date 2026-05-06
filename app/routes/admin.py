from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
def dashboard():
    """
    管理員後台首頁。僅限管理員。
    顯示系統統計資訊 (e.g. 用戶總數、食譜總數)，渲染 admin/dashboard.html
    """
    pass

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
    刪除用戶及所有的連帶食譜資料。僅限管理員。
    執行成功後重導回用戶列表
    """
    pass

@admin_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    強制刪除違規食譜。僅限管理員。
    執行成功後重導向回管理員面板或通知
    """
    pass

@admin_bp.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    """
    管理食譜分類標籤頁。僅限管理員。
    GET: 顯示現有所有分類與新增表單
    POST: 新增或刪除某個分類，重新渲染 admin/categories.html 或重導向
    """
    pass
