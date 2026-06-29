"""Remove specified categories from database."""
from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.product import Product

app = create_app()

with app.app_context():
    # Categories to remove
    categories_to_remove = ['交通出行', '教材学习']
    
    print(f'Categories to remove: {categories_to_remove}')
    
    for category_name in categories_to_remove:
        category = Category.query.filter_by(category_name=category_name).first()
        if category:
            # Check if there are products in this category
            product_count = Product.query.filter_by(category_id=category.category_id).count()
            if product_count > 0:
                print(f'[WARNING] Category "{category_name}" has {product_count} products')
                # Move products to "其他闲置" category
                other_category = Category.query.filter_by(category_name='其他闲置').first()
                if other_category:
                    Product.query.filter_by(category_id=category.category_id).update(
                        {'category_id': other_category.category_id}
                    )
                    print(f'[OK] Moved {product_count} products to "其他闲置"')
            
            # Delete the category
            db.session.delete(category)
            db.session.commit()
            print(f'[OK] Removed category: {category_name}')
        else:
            print(f'[SKIP] Category "{category_name}" not found')
    
    print('\nRemaining categories:')
    for cat in Category.query.order_by(Category.created_at).all():
        print(f'  - {cat.category_name}')
    
    print('\nDone!')
