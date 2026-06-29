"""
测试数据初始化脚本
用于预先创建测试用户、商品等数据，方便进行黑盒测试
"""
import sys
from decimal import Decimal

sys.path.insert(0, 'd:\\code\\新建文件夹\\xiaoyuanershou\\xiaoyuan-main')

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product


def init_test_data():
    """初始化测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("开始初始化测试数据...")
        print("=" * 60)
        
        # 1. 创建测试用户
        print("\n[1/4] 创建测试用户...")
        
        def get_or_create_user(username, email, phone, nickname, introduction):
            """获取或创建用户"""
            user = User.query.filter_by(username=username).first()
            if user:
                return user
            
            # 检查邮箱是否存在
            existing = User.query.filter_by(email=email).first()
            if existing:
                return existing
            
            # 检查手机号是否存在
            existing = User.query.filter_by(phone=phone).first()
            if existing:
                return existing
            
            # 创建新用户
            user = User(
                username=username,
                email=email,
                phone=phone,
                nickname=nickname,
                introduction=introduction,
                session_version=1
            )
            user.set_password('Test123456')
            db.session.add(user)
            db.session.commit()
            print(f"[OK] 创建用户: {username} / Test123456")
            return user
        
        # 主测试用户
        test_user = get_or_create_user(
            'testuser',
            'testuser@example.com',
            '13800138000',
            '测试用户',
            '这是一个测试用户账号'
        )
        if User.query.filter_by(username='testuser').first():
            print("[OK] 测试用户已存在: testuser")
        
        # 卖家用户1
        seller1 = get_or_create_user(
            'seller1',
            'seller1@example.com',
            '13800138001',
            '小明同学',
            '诚信交易，非诚勿扰！'
        )
        if User.query.filter_by(username='seller1').first():
            print("[OK] 卖家用户1已存在: seller1")
        
        # 卖家用户2
        seller2 = get_or_create_user(
            'seller2',
            'seller2@example.com',
            '13800138002',
            '书香门第',
            '出售各类书籍资料'
        )
        if User.query.filter_by(username='seller2').first():
            print("[OK] 卖家用户2已存在: seller2")
        
        # 重新获取用户对象
        test_user = User.query.filter_by(username='testuser').first()
        seller1 = User.query.filter_by(username='seller1').first()
        seller2 = User.query.filter_by(username='seller2').first()
        
        # 2. 确保分类存在
        print("\n[2/4] 检查商品分类...")
        categories = [
            ('数码电子', '手机、电脑、平板、耳机、相机、游戏机等'),
            ('服饰鞋包', '衣服、鞋子、包包、配饰、帽子、围巾等'),
            ('生活用品', '日用品、宿舍神器、收纳、装饰、护肤品等'),
            ('运动户外', '运动器材、健身装备、户外用品、运动鞋服等'),
            ('图书娱乐', '小说、漫画、桌游、玩具、乐器等'),
            ('美妆个护', '护肤品、化妆品、洗护用品、香水等'),
            ('家居装饰', '摆件、装饰画、收纳、台灯、软装等'),
            ('交通工具', '自行车、电动车、滑板等交通工具'),
            ('其他闲置', '不在以上分类中的物品'),
        ]
        
        category_objects = {}
        for name, desc in categories:
            cat = Category.query.filter_by(category_name=name).first()
            if not cat:
                cat = Category(
                    category_name=name,
                    description=desc,
                    status='ENABLED'
                )
                db.session.add(cat)
                db.session.commit()
                print(f"[OK] 创建分类: {name}")
            else:
                print(f"[OK] 分类已存在: {name}")
            category_objects[name] = cat
        
        # 3. 创建测试商品
        print("\n[3/4] 创建测试商品...")
        
        # seller1 的商品
        seller1_products = [
            {
                'name': '全新自行车',
                'category': '交通工具',
                'price': 299.00,
                'condition': '九成新',
                'description': '毕业出售，买了半年骑过几次，质量很好，带锁和车筐。',
                'location': '北区宿舍楼下',
                'status': 'ON_SALE'
            },
            {
                'name': '高等数学第七版',
                'category': '图书娱乐',
                'price': 15.00,
                'condition': '八成新',
                'description': '高数教材，有少量笔记，不影响使用。',
                'location': '图书馆门口',
                'status': 'ON_SALE'
            },
            {
                'name': '小米充电宝20000mAh',
                'category': '数码电子',
                'price': 50.00,
                'condition': '七成新',
                'description': '小米充电宝，容量20000mAh，使用正常，换手机了不用了。',
                'location': '南区食堂',
                'status': 'ON_SALE'
            }
        ]
        
        # seller2 的商品
        seller2_products = [
            {
                'name': '考研英语词汇书',
                'category': '图书娱乐',
                'price': 20.00,
                'condition': '九成新',
                'description': '考研英语词汇红宝书，用过几次，笔记很少。',
                'location': '教学楼A座',
                'status': 'ON_SALE'
            },
            {
                'name': '篮球斯伯丁',
                'category': '运动户外',
                'price': 80.00,
                'condition': '八成新',
                'description': '斯伯丁篮球，正品，弹性好，便宜出了。',
                'location': '体育馆门口',
                'status': 'ON_SALE'
            },
            {
                'name': '台灯LED护眼灯',
                'category': '生活用品',
                'price': 35.00,
                'condition': '全新',
                'description': '全新LED护眼台灯，三档调节，买回来没用过。',
                'location': '东区宿舍',
                'status': 'ON_SALE'
            }
        ]
        
        # 创建商品
        for product_data in seller1_products:
            existing = Product.query.filter_by(
                product_name=product_data['name'],
                seller_id=seller1.user_id
            ).first()
            
            if not existing:
                category = category_objects[product_data['category']]
                product = Product(
                    seller_id=seller1.user_id,
                    category_id=category.category_id,
                    product_name=product_data['name'],
                    price=Decimal(str(product_data['price'])),
                    condition_level=product_data['condition'],
                    description=product_data['description'],
                    trade_location=product_data['location'],
                    product_status=product_data['status'],
                    view_count=0
                )
                db.session.add(product)
                db.session.commit()
                print(f"[OK] 创建商品: {product_data['name']} (seller1)")
            else:
                print(f"[OK] 商品已存在: {product_data['name']}")
        
        for product_data in seller2_products:
            existing = Product.query.filter_by(
                product_name=product_data['name'],
                seller_id=seller2.user_id
            ).first()
            
            if not existing:
                category = category_objects[product_data['category']]
                product = Product(
                    seller_id=seller2.user_id,
                    category_id=category.category_id,
                    product_name=product_data['name'],
                    price=Decimal(str(product_data['price'])),
                    condition_level=product_data['condition'],
                    description=product_data['description'],
                    trade_location=product_data['location'],
                    product_status=product_data['status'],
                    view_count=0
                )
                db.session.add(product)
                db.session.commit()
                print(f"[OK] 创建商品: {product_data['name']} (seller2)")
            else:
                print(f"[OK] 商品已存在: {product_data['name']}")
        
        # 4. 统计信息
        print("\n[4/4] 统计信息...")
        user_count = User.query.count()
        category_count = Category.query.filter_by(status='ENABLED').count()
        product_count = Product.query.filter_by(deleted=False).count()
        
        print(f"\n[OK] 用户总数: {user_count}")
        print(f"[OK] 分类总数: {category_count}")
        print(f"[OK] 商品总数: {product_count}")
        
        print("\n" + "=" * 60)
        print("测试数据初始化完成！")
        print("=" * 60)
        print("\n测试账号信息：")
        print("-" * 60)
        print("主测试账号: testuser / Test123456")
        print("卖家账号1:   seller1 / Test123456")
        print("卖家账号2:   seller2 / Test123456")
        print("-" * 60)


if __name__ == '__main__':
    try:
        init_test_data()
    except Exception as e:
        print(f"\n[ERROR] 错误: {str(e)}")
        import traceback
        traceback.print_exc()
