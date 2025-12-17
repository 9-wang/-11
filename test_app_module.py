# 测试app模块是否能被正确导入，并验证app属性是否存在
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

print("=== 测试app模块导入 ===")

# 测试1：直接导入app模块
try:
    import app
    print("✅ 成功导入app模块")
    
    # 测试2：检查app模块中是否有app属性
    if hasattr(app, 'app'):
        print(f"✅ app模块中存在app属性，类型: {type(app.app)}")
    else:
        print("❌ app模块中不存在app属性")
        print("   app模块中的属性列表:", dir(app))
        
    # 测试3：尝试直接从app模块导入app
    try:
        from app import app as flask_app
        print(f"✅ 成功从app模块导入app，类型: {type(flask_app)}")
    except ImportError as e:
        print(f"❌ 从app模块导入app失败: {e}")
        
except Exception as e:
    print(f"❌ 导入app模块失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试结束 ===")
