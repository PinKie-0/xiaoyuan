"""
清理测试数据脚本
删除除管理员外的所有用户和所有商品
"""
import sys

sys.path.insert(0, 'd:\\code\\新建文件夹\\xiaoyuanershou\\xiaoyuan-main')

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.orders import Order
from app.models.favorite import Favorite
from app.models.message import Message
from app.models.notification import Notification
from app.models.review import Review
from app.models.report import Report
from app.models.product_image import ProductImage
from app.models.product_comment import ProductComment


def clean_up_data():
    """清理测试数据"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("开始清理数据...")
        print("=" * 60)
        
        # 1. 统计当前数据
        print("\n[统计] 当前数据:")
        user_count = User.query.count()
        product_count = Product.query.filter_by(deleted=False).count()
        order_count = Order.query.count()
        print(f"  用户总数: {user_count}")
        print(f"  商品总数: {product_count}")
        print(f"  订单总数: {order_count}")
        
        # 2. 删除相关数据（先删除依赖表）
        print("\n[1/8] 删除通知...")
        notif_count = db.session.query(Notification).delete()
        db.session.commit()
        print(f"  删除了 {notif_count} 条通知")
        
        print("\n[2/8] 删除消息...")
        msg_count = db.session.query(Message).delete()
        db.session.commit()
        print(f"  删除了 {msg_count} 条消息")
        
        print("\n[3/8] 删除评价...")
        review_count = db.session.query(Review).delete()
        db.session.commit()
        print(f"  删除了 {review_count} 条评价")
        
        print("\n[4/8] 删除举报...")
        report_count = db.session.query(Report).delete()
        db.session.commit()
        print(f"  删除了 {report_count} 条举报")
        
        print("\n[5/8] 删除收藏...")
        fav_count = db.session.query(Favorite).delete()
        db.session.commit()
        print(f"  删除了 {fav_count} 条收藏")
        
        print("\n[6/8] 删除商品图片...")
        img_count = db.session.query(ProductImage).delete()
        db.session.commit()
        print(f"  删除了 {img_count} 张商品图片")
        
        print("\n[7/8] 删除商品评论...")
        comment_count = db.session.query(ProductComment).delete()
        db.session.commit()
        print(f"  删除了 {comment_count} 条商品评论")
        
        print("\n[8/8] 删除订单...")
        order_count = db.session.query(Order).delete()
        db.session.commit()
        print(f"  删除了 {order_count} 个订单")
        
        # 3. 删除所有商品
        print("\n[删除商品]...")
        products = Product.query.filter_by(deleted=False).all()
        deleted_products = 0
        for product in products:
            product.deleted = True
            product.product_status = 'DELETED'
            deleted_products += 1
        db.session.commit()
        print(f"  删除了 {deleted_products} 个商品")
        
        # 4. 删除除管理员外的所有用户
        print("\n[删除用户]...")
        users = User.query.filter(User.role != 'ADMIN').all()
        deleted_users = 0
        for user in users:
            # 软删除
            user.deleted = True
            user.status = 'BANNED'
            deleted_users += 1
        db.session.commit()
        print(f"  删除了 {deleted_users} 个非管理员用户")
        
        # 5. 统计剩余数据
        print("\n" + "=" * 60)
        print("清理完成！")
        print("=" * 60)
        
        remaining_users = User.query.filter_by(deleted=False).count()
        remaining_products = Product.query.filter_by(deleted=False).count()
        
        print(f"\n[剩余数据]")
        print(f"  用户数: {remaining_users}")
        print(f"  商品数: {remaining_products}")
        
        # 显示剩余的管理员
        admins = User.query.filter_by(role='ADMIN', deleted=False).all()
        print(f"\n[保留的管理员]")
        for admin in admins:
            print(f"  - {admin.username} (ID: {admin.user_id})")


if __name__ == '__main__':
    try:
        clean_up_data()
    except Exception as e:
        print(f"\n[ERROR] 错误: {str(e)}")
        import traceback
        traceback.print_exc()
