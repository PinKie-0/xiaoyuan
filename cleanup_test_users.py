from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product

app = create_app()
with app.app_context():
    print("=== 清理测试用户 ===")
    
    # 获取 admin 用户
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        print("错误：找不到 admin 用户！")
        exit(1)
    
    print(f"Admin 用户: {admin_user.username}, user_id: {admin_user.user_id}")
    
    # 先把所有产品的卖家改为 admin
    products = Product.query.all()
    print(f"\n找到 {len(products)} 个产品，将卖家改为 admin")
    for product in products:
        product.seller_id = admin_user.user_id
    
    db.session.commit()
    print("产品卖家已更新")
    
    # 保留 admin，删除其他所有用户
    users_to_delete = User.query.filter(User.username != 'admin').all()
    
    print(f"\n找到 {len(users_to_delete)} 个测试用户需要删除")
    
    for user in users_to_delete:
        print(f"  - 删除用户: {user.username} (phone: {user.phone}, email: {user.email})")
        db.session.delete(user)
    
    db.session.commit()
    
    print("\n=== 清理完成 ===")
    print(f"剩余用户数: {User.query.count()}")
    
    # 显示剩余用户
    remaining_users = User.query.all()
    for user in remaining_users:
        print(f"  - {user.username} (phone: {user.phone}, email: {user.email})")
