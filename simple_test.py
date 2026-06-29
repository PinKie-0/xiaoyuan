from app import create_app
from app.extensions import db
from app.services import auth_service
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = create_app()
with app.app_context():
    print("=== 简单测试注册 ===")
    
    test_username = "testuser999"
    test_phone = "13999999999"
    test_email = "testuser999@example.com"
    test_password = "testpass123"
    
    # 发送验证码
    success, message = auth_service.send_register_otp(phone=test_phone, email=test_email)
    print(f"发送验证码: {'OK' if success else 'FAIL'}, {message}")
    
    if success:
        # 获取验证码
        from app.services.auth_service import _otp_store
        otp_key = auth_service.get_register_otp_key(phone=test_phone, email=test_email)
        otp_entry = _otp_store.get(otp_key)
        test_otp = otp_entry['otp'] if otp_entry else None
        print(f"验证码: {test_otp}")
        
        if test_otp:
            # 注册
            success, message, user = auth_service.register_user(
                username=test_username,
                password=test_password,
                phone=test_phone,
                email=test_email,
                nickname="测试用户",
                otp=test_otp,
                role="USER"
            )
            print(f"注册: {'OK' if success else 'FAIL'}, {message}")
            
            if success and user:
                print(f"用户创建成功: {user.username}")
                # 清理
                db.session.delete(user)
                db.session.commit()
                print("测试用户已删除")

print("\n=== 测试完成 ===")
