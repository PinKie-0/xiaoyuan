"""添加交通工具分类"""
from app import create_app
from app.extensions import db
from app.models.category import Category

app = create_app()

with app.app_context():
    # 检查是否已存在
    existing = Category.query.filter_by(category_name='交通工具').first()
    if existing:
        print('"交通工具"分类已存在')
    else:
        # 添加新分类
        category = Category(
            category_name='交通工具',
            description='自行车、电动车、滑板等交通工具',
            status='ENABLED'
        )
        db.session.add(category)
        db.session.commit()
        print('成功添加"交通工具"分类')
    
    # 显示所有分类
    print('\n当前所有分类：')
    for cat in Category.query.order_by(Category.created_at).all():
        print(f'  - {cat.category_name}')
