from app import create_app
from app.extensions import db
from app.services import auth_service

app = create_app()
with app.app_context():
    print("=== 测试注册功能 ===")
    
    # 测试发送验证码
    test_username = "newuser123"
    test_phone = "13912345678"
    test_email = "newuser123@example.com"
    test_password = "testpass123"
    
    print(f"\n1. 测试发送验证码 (phone: {test_phone}, email: {test_email})")
    success, message = auth_service.send_register_otp(phone=test_phone, email=test_email)
    print(f"   结果: {'成功' if success else '失败'}, 消息: {message}")
    
    if success:
        # 从 otp_store 中获取验证码
        import sys
        sys.path.insert(0, 'app')
        from app.services.auth_service import _otp_store
        otp_key = auth_service.get_register_otp_key(phone=test_phone, email=test_email)
        print(f"   OTP key: {otp_key}")
        otp_entry = _otp_store.get(otp_key)
        if otp_entry:
            test_otp = otp_entry['otp']
            print(f"   验证码: {test_otp}")
            
            # 测试注册
            print(f"\n2. 测试注册用户 (username: {test_username})")
            success, message, user = auth_service.register_user(
                username=test_username,
                password=test_password,
                phone=test_phone,
                email=test_email,
                nickname="新用户",
                otp=test_otp,
                role="USER"
            )
            print(f"   结果: {'成功' if success else '失败'}, 消息: {message}")
            
            if success and user:
                print(f"   用户创建成功: {user.username}, user_id: {user.user_id}")
                
                # 清理测试用户
                print(f"\n3. 清理测试用户")
                db.session.delete(user)
                db.session.commit()
                print("   测试用户已删除")
        else:
            print("   无法获取验证码，OTP store 中没有找到")
    else:
        print("   发送验证码失败，无法继续测试")
