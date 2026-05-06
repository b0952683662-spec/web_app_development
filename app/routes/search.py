from flask import Blueprint

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/', methods=['GET'])
def search_keyword():
    """
    關鍵字搜尋執行頁面。
    依 `q` 參數搜尋食譜標題與描述，並渲染 search/results.html 顯示結果
    """
    pass

@search_bp.route('/ingredient', methods=['GET', 'POST'])
def search_ingredient():
    """
    食材組合搜尋表單與結果。
    GET: 渲染 search/ingredient.html 顯示搜尋表單
    POST: 接收多項食材輸入，計算符合度，並在原頁面顯示推薦列表
    """
    pass
