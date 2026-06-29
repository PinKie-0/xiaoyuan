import subprocess
import sys
import os


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("校园二手交易系统 - 测试运行器")
    print("=" * 60)
    
    test_files = [
        "test_auth_login_logout.py",
        "test_auth_register.py",
        "test_browse_category.py",
        "test_browse_search.py",
        "test_home_diagnostic.py",
        "test_homepage_queries.py",
        "test_notification.py",
        "test_password_recovery_change.py",
        "test_product_publish_manage.py",
        "test_user_profile.py",
        "test_complete.py",
    ]
    
    print("\n可用的测试文件:")
    for i, file in enumerate(test_files, 1):
        print(f"  {i}. {file}")
    
    print("\n请选择要运行的测试:")
    print("  a - 运行所有测试")
    print("  n - 运行新添加的完整测试 (test_complete.py)")
    print("  1~{n} - 运行指定的测试文件".format(n=len(test_files)))
    
    choice = input("\n请输入选择 (a/n/1~{}): ".format(len(test_files))).strip()
    
    if choice.lower() == 'a':
        print("\n正在运行所有测试...")
        run_pytest(["tests/"])
    elif choice.lower() == 'n':
        print("\n正在运行新添加的完整测试...")
        run_pytest(["tests/test_complete.py", "-v"])
    elif choice.isdigit() and 1 <= int(choice) <= len(test_files):
        test_file = test_files[int(choice) - 1]
        print(f"\n正在运行测试: {test_file}")
        run_pytest([f"tests/{test_file}", "-v"])
    else:
        print("无效的选择！")


def run_pytest(args):
    """运行 pytest 命令"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest"] + args,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        return result.returncode == 0
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return False


def init_test_data():
    """初始化测试数据"""
    print("\n正在初始化测试数据...")
    try:
        result = subprocess.run(
            [sys.executable, "init_test_data.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        if result.returncode == 0:
            print("测试数据初始化成功！")
        else:
            print("测试数据初始化失败！")
    except Exception as e:
        print(f"初始化测试数据时出错: {e}")


def quick_test():
    """快速测试 - 运行完整测试套件"""
    print("\n快速测试模式 - 运行完整测试套件...")
    run_pytest(["tests/test_complete.py", "-v", "--tb=short"])


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="校园二手交易系统测试运行器")
    parser.add_argument(
        "-q", "--quick",
        action="store_true",
        help="快速运行完整测试"
    )
    parser.add_argument(
        "-i", "--init",
        action="store_true",
        help="初始化测试数据"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="运行所有测试"
    )
    
    args = parser.parse_args()
    
    if args.quick:
        quick_test()
    elif args.init:
        init_test_data()
    elif args.all:
        run_pytest(["tests/", "-v"])
    else:
        run_all_tests()
