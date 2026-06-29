# 测试指南

本指南说明如何运行校园二手交易系统的测试。

## 快速开始

### 1. 安装依赖

确保已安装项目依赖：

```bash
pip install -r requirements.txt
```

### 2. 初始化测试数据（可选）

如果需要使用预置的测试数据：

```bash
python init_test_data.py
```

### 3. 运行测试

#### 方式一：使用测试运行脚本（推荐）

```bash
# 交互式选择测试
python run_tests.py

# 快速运行完整测试
python run_tests.py -q

# 初始化测试数据
python run_tests.py -i

# 运行所有测试
python run_tests.py -a
```

#### 方式二：直接使用 pytest

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_complete.py -v

# 运行测试并显示详细输出
python -m pytest tests/test_complete.py -v -s

# 生成测试覆盖率报告
python -m pytest tests/ --cov=app --cov-report=html
```

## 测试文件说明

| 文件 | 说明 |
|------|------|
| `test_complete.py` | ⭐ 新添加的完整测试套件 |
| `test_auth_login_logout.py` | 登录登出测试 |
| `test_auth_register.py` | 注册测试 |
| `test_browse_category.py` | 分类浏览测试 |
| `test_browse_search.py` | 搜索功能测试 |
| `test_home_diagnostic.py` | 首页诊断测试 |
| `test_homepage_queries.py` | 首页查询测试 |
| `test_notification.py` | 通知功能测试 |
| `test_password_recovery_change.py` | 密码恢复和修改测试 |
| `test_product_publish_manage.py` | 商品发布管理测试 |
| `test_user_profile.py` | 用户资料测试 |

## 测试模块说明

### test_complete.py（新增）

包含以下测试类：

#### TestUserAuth - 用户认证测试
- `test_register_new_user` - 正常注册新用户
- `test_register_existing_username` - 注册已存在的用户名
- `test_login_success` - 成功登录
- `test_login_wrong_password` - 密码错误
- `test_logout` - 登出

#### TestProductManagement - 商品管理测试
- `test_publish_product` - 发布商品
- `test_edit_product` - 编辑商品
- `test_view_my_products` - 查看我的商品

#### TestBrowseAndSearch - 浏览和搜索测试
- `test_view_homepage` - 查看首页
- `test_search_product` - 搜索商品
- `test_view_product_detail` - 查看商品详情

#### TestFavorite - 收藏功能测试
- `test_add_favorite` - 添加收藏
- `test_view_favorites` - 查看收藏列表

#### TestUserProfile - 用户资料测试
- `test_view_profile` - 查看个人资料
- `test_edit_profile` - 编辑个人资料

#### TestOrder - 订单测试
- `test_submit_order` - 提交订单
- `test_view_buyer_orders` - 查看买家订单
- `test_view_seller_orders` - 查看卖家订单

## 测试用例对照表

| 测试文档用例编号 | 对应测试函数 |
|----------------|------------|
| UC-001 | test_register_new_user |
| UC-002 | test_register_existing_username |
| UC-004 | test_login_success |
| UC-005 | test_login_wrong_password |
| UC-010 | test_logout |
| UC-011 | test_view_homepage |
| UC-012 | test_search_product |
| UC-015 | test_view_product_detail |
| UC-016 | test_add_favorite |
| UC-018 | test_view_favorites |
| UC-019 | test_view_profile |
| UC-020 | test_edit_profile |
| UC-022 | test_publish_product |
| UC-026 | test_view_my_products |
| UC-027 | test_edit_product |

## 编写新测试

### 测试结构示例

```python
import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_example_functionality(client, app):
    # 这里编写测试代码
    response = client.get("/some/url")
    assert response.status_code == 200
```

### Fixtures 说明

| Fixture | 用途 |
|---------|------|
| `app` | 测试应用实例 |
| `client` | 测试客户端 |
| `test_user` | 测试用户 |
| `test_seller` | 测试卖家 |
| `test_category` | 测试分类 |
| `test_product` | 测试商品 |

## 常见问题

### 1. 测试数据库问题

如果遇到数据库相关错误，确保测试配置正确：

```python
# app/config.py
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
```

### 2. 导入问题

确保从正确的位置导入模块：

```python
from app import create_app
from app.extensions import db
from app.models.user import User
```

### 3. 测试数据清理

每个测试后数据会自动清理，因为使用了内存数据库和 `db.drop_all()`。

## 手动测试指南

除了自动化测试外，也可以进行手动测试：

### 步骤 1：启动应用

```bash
python run.py
```

### 步骤 2：访问应用

在浏览器中访问：`http://localhost:5000`

### 步骤 3：按照测试文档执行

参考 `docs/软件测试文档-按实际功能整理.md` 中的测试用例进行手动测试。

### 步骤 4：记录测试结果

在测试文档的"测试结果分析"部分记录测试结果。
