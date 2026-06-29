from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.orders import Order
from app.models.favorite import Favorite
from app.models.message import Message
from app.models.review import Review
from app.models.report import Report
from app.models.notification import Notification

app = create_app()
with app.app_context():
    print("=== 清理所有测试数据 ===\n")
    
    # 获取 admin 用户
    admin_user = User.query.filter_by(username='admin').first()
    print(f"Admin 用户: {admin_user.username}, user_id: {admin_user.user_id}")
    
    # 1. 清理订单
    orders = Order.query.all()
    print(f"\n订单数: {len(orders)}")
    for order in orders:
        db.session.delete(order)
    db.session.commit()
    print("订单已清理")
    
    # 2. 清理收藏
    favorites = Favorite.query.all()
    print(f"\n收藏数: {len(favorites)}")
    for fav in favorites:
        db.session.delete(fav)
    db.session.commit()
    print("收藏已清理")
    
    # 3. 清理消息
    messages = Message.query.all()
    print(f"\n消息数: {len(messages)}")
    for msg in messages:
        db.session.delete(msg)
    db.session.commit()
    print("消息已清理")
    
    # 4. 清理评价
    reviews = Review.query.all()
    print(f"\n评价数: {len(reviews)}")
    for rev in reviews:
        db.session.delete(rev)
    db.session.commit()
    print("评价已清理")
    
    # 5. 清理举报
    reports = Report.query.all()
    print(f"\n举报数: {len(reports)}")
    for rep in reports:
        db.session.delete(rep)
    db.session.commit()
    print("举报已清理")
    
    # 6. 清理通知
    notifications = Notification.query.all()
    print(f"\n通知数: {len(notifications)}")
    for notif in notifications:
        db.session.delete(notif)
    db.session.commit()
    print("通知已清理")
    
    # 7. 把所有产品的卖家改为 admin
    products = Product.query.all()
    print(f"\n产品数: {len(products)}")
    for product in products:
        product.seller_id = admin_user.user_id
    db.session.commit()
    print("产品卖家已更新为 admin")
    
    # 8. 删除除 admin 外的所有用户
    users_to_delete = User.query.filter(User.username != 'admin').all()
    print(f"\n需删除的用户数: {len(users_to_delete)}")
    for user in users_to_delete:
        print(f"  - {user.username}")
        db.session.delete(user)
    db.session.commit()
    
    print("\n=== 清理完成 ===")
    print(f"剩余用户数: {User.query.count()}")
    print(f"剩余产品数: {Product.query.count()}")
    
    remaining_users = User.query.all()
    for user in remaining_users:
        print(f"\n  - {user.username}")
        print(f"    phone: {user.phone}")
        print(f"    email: {user.email}")
