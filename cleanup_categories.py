"""Cleanup duplicate categories and keep only the desired ones."""
from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.product import Product

app = create_app()

with app.app_context():
    # Categories we want to keep
    keep_categories = [
        '数码电子',
        '服饰鞋包', 
        '生活用品',
        '运动户外',
        '图书娱乐',
        '美妆个护',
        '家居装饰',
        '其他闲置'
    ]
    
    print(f'Categories to keep: {keep_categories}')
    print()
    
    # Get all categories
    all_categories = Category.query.all()
    print(f'Total categories in database: {len(all_categories)}')
    
    # Find "其他闲置" category to move products to
    other_category = Category.query.filter_by(category_name='其他闲置').first()
    if not other_category:
        print('[ERROR] "其他闲置" category not found!')
    else:
        print(f'Found "其他闲置" category (id: {other_category.category_id})')
    
    print()
    
    # Process each category
    for category in all_categories:
        if category.category_name not in keep_categories:
            print(f'Processing: {category.category_name}')
            
            # Check for products
            product_count = Product.query.filter_by(category_id=category.category_id).count()
            if product_count > 0 and other_category:
                print(f'  - Has {product_count} products, moving to "其他闲置"')
                Product.query.filter_by(category_id=category.category_id).update(
                    {'category_id': other_category.category_id}
                )
            
            # Delete the category
            db.session.delete(category)
            db.session.commit()
            print(f'  - DELETED')
        else:
            print(f'Keeping: {category.category_name}')
    
    print()
    print('Final categories:')
    for cat in Category.query.order_by(Category.created_at).all():
        print(f'  - {cat.category_name}')
    
    print('\nDone!')
