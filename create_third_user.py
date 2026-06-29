"""
创建第三个测试用户，用于测试无权访问订单
"""
import sys

sys.path.insert(0, 'd:\\code\\新建文件夹\\xiaoyuanershou\\xiaoyuan-main')

from app import create_app
from app.extensions import db
from app.models.user import User


def create_third_user():
    """创建第三个测试用户"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("创建第三个测试用户...")
        print("=" * 60)
        
        # 检查用户是否已存在
        user = User.query.filter_by(username='testuser2').first()
        
        if user:
            print(f"\n[OK] 用户已存在: testuser2")
        else:
            # 创建新用户
            user = User(
                username='testuser2',
                email='testuser2@example.com',
                phone='13800138003',
                nickname='测试用户2',
                introduction='这是第三个测试用户，用于测试权限',
                session_version=1
            )
            user.set_password('Test123456')
            db.session.add(user)
            db.session.commit()
            print(f"\n[OK] 创建用户: testuser2 / Test123456")
        
        print("\n" + "=" * 60)
        print("创建完成！")
        print("=" * 60)
        print("\n测试账号信息：")
        print("-" * 60)
        print("主测试账号: testuser / Test123456")
        print("卖家账号1:   seller1 / Test123456")
        print("测试账号2:   testuser2 / Test123456 (新！)")
        print("-" * 60)


if __name__ == '__main__':
    try:
        create_third_user()
    except Exception as e:
        print(f"\n[ERROR] 错误: {str(e)}")
        import traceback
        traceback.print_exc()
