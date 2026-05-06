# ROUTES — 路由與頁面設計

> **版本**：v1.0
> **建立日期**：2026-05-07
> **依據**：docs/PRD.md、docs/ARCHITECTURE.md、docs/DB_DESIGN.md

---

## 1. 路由總覽表格

| 模組 | 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|------|-----------|----------|----------|------|
| **Recipes** | 首頁 / 食譜列表 | GET | `/` | `templates/index.html` | 顯示所有公開食譜，支援分頁與分類/難度篩選 |
| | 食譜詳細頁 | GET | `/recipes/<int:recipe_id>` | `templates/recipes/detail.html` | 顯示單一食譜的食材、步驟與詳細資訊 |
| | 新增食譜頁面 | GET | `/recipes/create` | `templates/recipes/create.html` | 顯示新增表單（需登入） |
| | 儲存食譜 | POST | `/recipes/create` | — | 接收表單，存入 DB，成功後重導向至詳細頁 |
| | 編輯食譜頁面 | GET | `/recipes/<int:recipe_id>/edit` | `templates/recipes/edit.html` | 顯示編輯表單（需為作者或管理員） |
| | 更新食譜 | POST | `/recipes/<int:recipe_id>/edit` | — | 接收表單，更新 DB，成功後重導向至詳細頁 |
| | 刪除食譜 | POST | `/recipes/<int:recipe_id>/delete` | — | 刪除 DB 資料，成功後重導向至首頁 |
| **Search** | 關鍵字搜尋 | GET | `/search` | `templates/search/results.html` | 依 `q` 參數搜尋食譜名稱與描述 |
| | 食材搜尋頁面 | GET | `/search/ingredient` | `templates/search/ingredient.html` | 顯示輸入手邊食材的表單 |
| | 執行食材搜尋 | POST | `/search/ingredient` | `templates/search/ingredient.html` | 回傳推薦食譜（含符合度） |
| **Auth** | 用戶註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| | 執行用戶註冊 | POST | `/auth/register` | — | 建立帳號，成功後重導向至首頁或登入頁 |
| | 用戶登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| | 執行用戶登入 | POST | `/auth/login` | — | 驗證帳密，成功後重導向至首頁 |
| | 用戶登出 | GET | `/auth/logout` | — | 清除 Session，重導向至首頁 |
| **Admin** | 管理員首頁 | GET | `/admin/` | `templates/admin/dashboard.html` | 顯示統計數據（需管理員權限） |
| | 封鎖/刪除用戶 | POST | `/admin/users/<int:user_id>/delete` | — | 刪除使用者及其建立的食譜 |
| | 刪除食譜（管理員） | POST | `/admin/recipes/<int:recipe_id>/delete` | — | 管理員強制刪除違規食譜 |
| | 分類標籤管理 | GET / POST | `/admin/categories` | `templates/admin/categories.html` | 顯示、新增、刪除分類標籤 |

---

## 2. 每個路由的詳細說明

### 2.1 模組：Recipes (`recipes.py`)

- **`GET /`**
  - **輸入**：URL 參數 `page`（分頁，預設 1）、`difficulty`（難度篩選，選填）、`category_id`（分類篩選，選填）。
  - **處理邏輯**：呼叫 `Recipe.get_all()` 取得分頁結果與過濾資料。
  - **輸出**：渲染 `index.html`。
  - **錯誤處理**：若頁數超過範圍，回傳 404 或重導向第 1 頁。

- **`GET /recipes/<int:recipe_id>`**
  - **處理邏輯**：呼叫 `Recipe.get_by_id(recipe_id)`。
  - **輸出**：渲染 `recipes/detail.html`。
  - **錯誤處理**：找不到食譜時回傳 404 頁面。

- **`GET/POST /recipes/create`**
  - **輸入**：(POST) `title`, `description`, `difficulty`, `cook_time`, 圖片檔案, 食材清單, 步驟清單。
  - **處理邏輯**：驗證表單。如成功，呼叫 `Recipe.create()`、`Ingredient.bulk_create()`、`Step.bulk_create()`，並儲存圖片。需要 `@login_required`。
  - **輸出**：渲染 `recipes/create.html` (GET 或 失敗)，成功則重導向 `/recipes/<id>`。

- **`GET/POST /recipes/<int:recipe_id>/edit`**
  - **處理邏輯**：驗證當前使用者是否為作者或管理員。查出原有資料預填至表單。POST 時更新 `Recipe` 及關聯表。
  - **輸出**：渲染 `recipes/edit.html` (GET 或 失敗)，成功則重導向 `/recipes/<id>`。
  - **錯誤處理**：非作者/管理員回傳 403。

- **`POST /recipes/<int:recipe_id>/delete`**
  - **處理邏輯**：驗證權限。刪除相關的食譜資料與圖片檔案。
  - **輸出**：重導向至 `/`。
  - **錯誤處理**：非作者/管理員回傳 403。

### 2.2 模組：Search (`search.py`)

- **`GET /search`**
  - **輸入**：URL 參數 `q`。
  - **處理邏輯**：呼叫 `Recipe.search_by_keyword(q)`。
  - **輸出**：渲染 `search/results.html`。

- **`GET/POST /search/ingredient`**
  - **輸入**：(POST) 使用者輸入的食材名稱陣列。
  - **處理邏輯**：處理輸入陣列，呼叫 `Recipe.search_by_ingredients()`，計算符合度並排序。
  - **輸出**：GET 或 POST 都渲染 `search/ingredient.html`，並顯示推薦列表。

### 2.3 模組：Auth (`auth.py`)

- **`GET/POST /auth/register`**
  - **輸入**：`username`, `email`, `password`, `confirm_password`。
  - **處理邏輯**：檢查 `email` 或 `username` 是否已存在。如果沒有，呼叫 `User.create()`。
  - **輸出**：渲染 `auth/register.html` 或重導向 `/auth/login`。

- **`GET/POST /auth/login`**
  - **輸入**：`email`, `password`。
  - **處理邏輯**：呼叫 `User.get_by_email()` 並驗證密碼 (`check_password()`)。成功則 `login_user()`。
  - **輸出**：渲染 `auth/login.html` 或重導向 `/` 或 next URL。

- **`GET /auth/logout`**
  - **處理邏輯**：`logout_user()`。
  - **輸出**：重導向 `/`。

### 2.4 模組：Admin (`admin.py`) (全需 `@admin_required`)

- **`GET /admin/`**
  - **輸出**：渲染 `admin/dashboard.html`，提供系統統計。

- **`POST /admin/users/<int:user_id>/delete`**
  - **處理邏輯**：從資料庫中刪除使用者及其連帶資源。
  - **輸出**：重導向 `/admin/users` 列表。

- **`GET/POST /admin/categories`**
  - **處理邏輯**：列出現有分類、允許新增與刪除分類。
  - **輸出**：渲染 `admin/categories.html`。

---

## 3. Jinja2 模板清單

所有的視圖模板都會繼承基礎版面（例如 `base.html`）。

| 檔案路徑 | 說明 | 繼承 |
|----------|------|------|
| `templates/base.html` | 基礎版型，包含導覽列 (Navbar)、全域 CSS/JS、Footer 等。 | (無) |
| `templates/index.html` | 首頁，顯示食譜列表。 | `base.html` |
| `templates/recipes/detail.html` | 單一食譜詳細畫面。 | `base.html` |
| `templates/recipes/create.html` | 新增食譜表單。 | `base.html` |
| `templates/recipes/edit.html` | 編輯食譜表單。 | `base.html` |
| `templates/search/results.html` | 關鍵字搜尋結果。 | `base.html` |
| `templates/search/ingredient.html` | 食材組合搜尋表單與結果。 | `base.html` |
| `templates/auth/login.html` | 登入表單。 | `base.html` |
| `templates/auth/register.html` | 註冊表單。 | `base.html` |
| `templates/admin/dashboard.html` | 管理員後台首頁與統計。 | `base.html` |
| `templates/admin/categories.html` | 分類標籤管理頁。 | `base.html` |

