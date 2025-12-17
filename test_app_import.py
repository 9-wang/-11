# 测试app模块是否能正确导入和获取app属性
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

print("正在测试app模块导入...")

try:
    # 导入app模块
    from app import app
    print("✅ 成功导入app模块并获取app属性")
    print(f"   app类型: {type(app)}")
    print(f"   app名称: {app.name}")
    print("✅ 测试通过！Gunicorn部署应该可以正常工作。")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
