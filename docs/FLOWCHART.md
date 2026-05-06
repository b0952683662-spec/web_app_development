# FLOWCHART — 食譜收藏夾系統

> **版本**：v1.0
> **建立日期**：2026-05-07
> **依據**：docs/PRD.md、docs/ARCHITECTURE.md

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項主要操作的完整路徑。

```mermaid
flowchart LR
    Start([🌐 使用者開啟網站]) --> Home[首頁\n食譜列表]

    Home --> IsLogin{已登入？}

    %% 未登入分支
    IsLogin -->|否| AuthChoice{選擇操作}
    AuthChoice -->|登入| Login[登入頁]
    AuthChoice -->|註冊| Register[註冊頁]
    Login --> LoginOK{驗證成功？}
    LoginOK -->|是| Home
    LoginOK -->|否| Login
    Register --> RegisterOK{資料合法？}
    RegisterOK -->|是| Home
    RegisterOK -->|否| Register

    %% 已登入分支
    IsLogin -->|是| MainMenu{要做什麼？}

    %% 瀏覽食譜
    MainMenu -->|瀏覽食譜| Browse[瀏覽頁\n分類 / 分頁]
    Browse --> RecipeDetail[食譜詳細頁\n食材 + 步驟 + 難度]

    %% 新增食譜
    MainMenu -->|新增食譜| CreateForm[填寫食譜表單\n名稱 / 食材 / 步驟 / 難度]
    CreateForm --> CreateOK{驗證通過？}
    CreateOK -->|是| RecipeDetail
    CreateOK -->|否| CreateForm

    %% 編輯 / 刪除食譜
    RecipeDetail --> IsOwner{是作者或管理員？}
    IsOwner -->|是| EditChoice{選擇操作}
    IsOwner -->|否| Browse
    EditChoice -->|編輯| EditForm[編輯食譜表單]
    EditForm --> RecipeDetail
    EditChoice -->|刪除| ConfirmDelete{確認刪除？}
    ConfirmDelete -->|是| Browse
    ConfirmDelete -->|否| RecipeDetail

    %% 搜尋食譜
    MainMenu -->|搜尋食譜| SearchBar[輸入關鍵字]
    SearchBar --> SearchResults[搜尋結果頁]
    SearchResults --> RecipeDetail

    %% 食材組合搜尋
    MainMenu -->|食材組合搜尋| IngredientSearch[輸入手邊食材]
    IngredientSearch --> MatchResults[推薦食譜\n含符合度 %]
    MatchResults --> RecipeDetail

    %% 難度篩選
    MainMenu -->|依難度篩選| DifficultyFilter[選擇難度\n新手 / 中級 / 進階]
    DifficultyFilter --> Browse

    %% 管理員後台
    IsLogin -->|管理員| AdminDash[管理員後台]
    AdminDash --> AdminRecipes[管理食譜]
    AdminDash --> AdminUsers[管理用戶]
    AdminDash --> AdminCategory[管理分類標籤]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 用戶登入流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(auth.py)
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 填寫帳號密碼並送出
    Browser->>Flask: POST /auth/login
    Flask->>Model: 查詢 User by email
    Model->>DB: SELECT * FROM users WHERE email=?
    DB-->>Model: 回傳用戶資料
    Model-->>Flask: User 物件

    alt 密碼正確
        Flask->>Flask: Flask-Login.login_user()
        Flask-->>Browser: 302 重導向 → 首頁
        Browser-->>User: 顯示首頁（已登入狀態）
    else 密碼錯誤
        Flask-->>Browser: 渲染 login.html（含錯誤訊息）
        Browser-->>User: 顯示登入失敗提示
    end
```

---

### 2.2 新增食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(recipes.py)
    participant RecipeModel as Recipe Model
    participant IngModel as Ingredient Model
    participant DB as SQLite

    User->>Browser: 填寫食譜表單（名稱/食材/步驟/難度）
    Browser->>Flask: POST /recipes/create
    Flask->>Flask: Flask-WTF 表單驗證

    alt 驗證失敗
        Flask-->>Browser: 渲染 create.html（含錯誤提示）
        Browser-->>User: 顯示驗證錯誤
    else 驗證成功
        Flask->>RecipeModel: 建立 Recipe 物件
        RecipeModel->>DB: INSERT INTO recipes
        DB-->>RecipeModel: recipe_id
        Flask->>IngModel: 建立 Ingredient 清單
        IngModel->>DB: INSERT INTO ingredients（批次）
        DB-->>IngModel: 成功
        Flask-->>Browser: 302 重導向 → 食譜詳細頁
        Browser-->>User: 顯示新建立的食譜
    end
```

---

### 2.3 食材組合搜尋流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(search.py)
    participant Helper as search_helpers.py
    participant DB as SQLite

    User->>Browser: 輸入手邊食材（如：雞蛋、番茄）
    Browser->>Flask: POST /search/ingredient
    Flask->>DB: SELECT 所有食譜及其食材
    DB-->>Flask: 食譜 + 食材清單

    Flask->>Helper: calculate_match_score(使用者食材, 各食譜食材)
    loop 每道食譜
        Helper->>Helper: 計算交集 / 食譜食材總數
        Helper->>Helper: 符合度 = 交集數 ÷ 食譜食材數 × 100%
    end
    Helper-->>Flask: 排序後的食譜清單（含符合度）

    Flask-->>Browser: 渲染 ingredient.html
    Browser-->>User: 顯示推薦食譜（依符合度高到低排序）
```

---

### 2.4 管理員刪除食譜流程

```mermaid
sequenceDiagram
    actor Admin as 管理員
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(admin.py)
    participant Decorator as admin_required\n裝飾器
    participant Model as Recipe Model
    participant DB as SQLite

    Admin->>Browser: 點擊「刪除食譜」按鈕
    Browser->>Flask: POST /admin/recipes/<id>/delete
    Flask->>Decorator: 檢查是否為管理員

    alt 非管理員
        Decorator-->>Browser: 403 Forbidden
        Browser-->>Admin: 顯示無權限頁面
    else 是管理員
        Flask->>Model: Recipe.query.get(id)
        Model->>DB: SELECT * FROM recipes WHERE id=?
        DB-->>Model: 食譜資料
        Flask->>DB: DELETE FROM recipes WHERE id=?
        DB-->>Flask: 成功
        Flask-->>Browser: 302 重導向 → 管理後台
        Browser-->>Admin: 顯示刪除成功訊息
    end
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 | 需登入 | 需管理員 |
|------|----------|-----------|------|--------|----------|
| 首頁 / 食譜列表 | `/` | GET | 顯示所有公開食譜，支援分類篩選與分頁 | ❌ | ❌ |
| 食譜詳細頁 | `/recipes/<id>` | GET | 顯示單一食譜的完整食材與步驟 | ❌ | ❌ |
| 新增食譜 | `/recipes/create` | GET / POST | GET 顯示表單；POST 儲存食譜 | ✅ | ❌ |
| 編輯食譜 | `/recipes/<id>/edit` | GET / POST | GET 顯示預填表單；POST 更新食譜 | ✅ | ❌ |
| 刪除食譜 | `/recipes/<id>/delete` | POST | 刪除食譜（只有作者或管理員可操作） | ✅ | ❌ |
| 關鍵字搜尋 | `/search` | GET | 依 `q` 參數搜尋食譜名稱 | ❌ | ❌ |
| 食材組合搜尋 | `/search/ingredient` | GET / POST | GET 顯示輸入頁；POST 回傳推薦清單 | ❌ | ❌ |
| 難度篩選 | `/recipes?difficulty=<n>` | GET | 依難度係數（1–5）篩選食譜列表 | ❌ | ❌ |
| 分類篩選 | `/recipes?category=<id>` | GET | 依分類標籤篩選食譜列表 | ❌ | ❌ |
| 用戶註冊 | `/auth/register` | GET / POST | GET 顯示表單；POST 建立帳號 | ❌ | ❌ |
| 用戶登入 | `/auth/login` | GET / POST | GET 顯示表單；POST 驗證登入 | ❌ | ❌ |
| 用戶登出 | `/auth/logout` | GET | 清除 Session，重導首頁 | ✅ | ❌ |
| 管理員後台首頁 | `/admin/` | GET | 顯示統計數據（食譜數、用戶數） | ✅ | ✅ |
| 管理員：食譜管理 | `/admin/recipes` | GET | 列出所有食譜，可操作刪除 | ✅ | ✅ |
| 管理員：用戶管理 | `/admin/users` | GET | 列出所有用戶，可封鎖或刪除 | ✅ | ✅ |
| 管理員：分類管理 | `/admin/categories` | GET / POST | 新增或刪除分類標籤 | ✅ | ✅ |

---

*此文件由 AI Agent 依據 Flowchart Skill 自動產出，Mermaid 語法可在 GitHub、Notion、Obsidian 等平台直接渲染預覽。*
