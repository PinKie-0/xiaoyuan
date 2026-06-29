from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.orders import Order
from app.models.favorite import Favorite
import pytest


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


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(
            username="test_user",
            phone="13800138000",
            email="test@example.com",
            role="USER",
            status="ACTIVE",
        )
        user.set_password("Test123456")
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def test_seller(app):
    with app.app_context():
        seller = User(
            username="test_seller",
            phone="13800138001",
            email="seller@example.com",
            role="USER",
            status="ACTIVE",
        )
        seller.set_password("Test123456")
        db.session.add(seller)
        db.session.commit()
        return seller


@pytest.fixture
def test_category(app):
    with app.app_context():
        category = Category(name="测试分类", sort_order=1)
        db.session.add(category)
        db.session.commit()
        return category


@pytest.fixture
def test_product(app, test_seller, test_category):
    with app.app_context():
        seller = User.query.get(test_seller.id)
        category = Category.query.get(test_category.id)
        product = Product(
            name="测试商品",
            price=100.00,
            condition="九成新",
            description="这是一个测试商品",
            category_id=category.id,
            seller_id=seller.id,
            status="ON_SALE",
            trade_location="学校北门",
        )
        db.session.add(product)
        db.session.commit()
        return product


class TestUserAuth:
    """用户认证测试"""
    
    def test_register_new_user(self, client, app):
        """测试正常注册新用户"""
        response = client.post(
            "/auth/register",
            data={
                "username": "new_user",
                "password": "Test123456",
                "confirm_password": "Test123456",
                "phone": "13800138002",
                "email": "new@example.com",
                "verification_code": "123456",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        
        with app.app_context():
            user = User.query.filter_by(username="new_user").first()
            assert user is not None

    def test_register_existing_username(self, client, test_user):
        """测试注册已存在的用户名"""
        response = client.post(
            "/auth/register",
            data={
                "username": "test_user",
                "password": "Test123456",
                "confirm_password": "Test123456",
                "phone": "13800138003",
                "email": "duplicate@example.com",
                "verification_code": "123456",
            },
            follow_redirects=True,
        )
        assert "用户名已被注册" in response.data.decode("utf-8")

    def test_login_success(self, client, test_user):
        """测试成功登录"""
        response = client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        
        profile_response = client.get("/user/profile")
        assert profile_response.status_code == 200

    def test_login_wrong_password(self, client, test_user):
        """测试密码错误"""
        response = client.post(
            "/auth/login",
            data={"username": "test_user", "password": "WrongPass123"},
            follow_redirects=True,
        )
        assert "账号或密码错误" in response.data.decode("utf-8")

    def test_logout(self, client, test_user):
        """测试登出"""
        client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200


class TestProductManagement:
    """商品管理测试"""
    
    def test_publish_product(self, client, test_seller, test_category):
        """测试发布商品"""
        client.post(
            "/auth/login",
            data={"username": "test_seller", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.post(
            "/product/publish",
            data={
                "name": "新测试商品",
                "category_id": test_category.id,
                "price": "200.00",
                "condition": "全新",
                "description": "这是新商品",
                "trade_location": "学校南门",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_edit_product(self, client, test_seller, test_product):
        """测试编辑商品"""
        client.post(
            "/auth/login",
            data={"username": "test_seller", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.post(
            f"/product/edit/{test_product.id}",
            data={
                "name": "修改后的商品",
                "category_id": test_product.category_id,
                "price": "150.00",
                "condition": "九成新",
                "description": "修改后的描述",
                "trade_location": "学校东门",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_view_my_products(self, client, test_seller, test_product):
        """测试查看我的商品"""
        client.post(
            "/auth/login",
            data={"username": "test_seller", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.get("/product/my")
        assert response.status_code == 200
        assert "测试商品" in response.data.decode("utf-8")


class TestBrowseAndSearch:
    """浏览和搜索测试"""
    
    def test_view_homepage(self, client):
        """测试查看首页"""
        response = client.get("/")
        assert response.status_code == 200

    def test_search_product(self, client, test_product):
        """测试搜索商品"""
        response = client.get("/browse/search?keyword=测试商品")
        assert response.status_code == 200

    def test_view_product_detail(self, client, test_product):
        """测试查看商品详情"""
        response = client.get(f"/browse/detail/{test_product.id}")
        assert response.status_code == 200
        assert "测试商品" in response.data.decode("utf-8")


class TestFavorite:
    """收藏功能测试"""
    
    def test_add_favorite(self, client, test_user, test_product):
        """测试添加收藏"""
        client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.post(f"/browse/favorite/{test_product.id}")
        assert response.status_code in [200, 302]

    def test_view_favorites(self, client, test_user, test_product):
        """测试查看收藏列表"""
        client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        
        client.post(f"/browse/favorite/{test_product.id}")
        
        response = client.get("/browse/favorites")
        assert response.status_code == 200


class TestUserProfile:
    """用户资料测试"""
    
    def test_view_profile(self, client, test_user):
        """测试查看个人资料"""
        client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.get("/user/profile")
        assert response.status_code == 200
        assert "test_user" in response.data.decode("utf-8")

    def test_edit_profile(self, client, test_user):
        """测试编辑个人资料"""
        client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.post(
            "/user/profile/edit",
            data={"nickname": "测试昵称", "bio": "这是个人介绍"},
            follow_redirects=True,
        )
        assert response.status_code == 200


class TestOrder:
    """订单测试"""
    
    def test_submit_order(self, client, test_user, test_product, test_seller):
        """测试提交订单"""
        client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.post(
            f"/order/submit/{test_product.id}",
            data={
                "trade_type": "OFFLINE",
                "buyer_message": "明天交易可以吗",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_view_buyer_orders(self, client, test_user):
        """测试查看买家订单"""
        client.post(
            "/auth/login",
            data={"username": "test_user", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.get("/order/buyer")
        assert response.status_code == 200

    def test_view_seller_orders(self, client, test_seller):
        """测试查看卖家订单"""
        client.post(
            "/auth/login",
            data={"username": "test_seller", "password": "Test123456"},
            follow_redirects=True,
        )
        
        response = client.get("/order/seller")
        assert response.status_code == 200


def run_tests():
    """运行所有测试的辅助函数"""
    import sys
    import subprocess
    
    print("=" * 50)
    print("开始运行测试...")
    print("=" * 50)
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_complete.py", "-v"],
        capture_output=True,
        text=True,
    )
    
    print("\n测试输出:")
    print(result.stdout)
    
    if result.stderr:
        print("\n错误输出:")
        print(result.stderr)
    
    print(f"\n测试结果: {'通过' if result.returncode == 0 else '失败'}")
    return result.returncode == 0


if __name__ == "__main__":
    run_tests()
