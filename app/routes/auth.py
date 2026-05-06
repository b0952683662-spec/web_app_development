from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    用戶註冊頁面與執行。
    GET: 渲染 auth/register.html
    POST: 驗證表單並建立 User，成功後重導向至登入頁或首頁
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    用戶登入頁面與執行。
    GET: 渲染 auth/login.html
    POST: 驗證 Email 與密碼，成功後記錄 Session 並重導向
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    用戶登出處理。
    清除 Session 並重導向至首頁
    """
    pass
