#!/usr/bin/env python3
"""
测试脚本：验证app模块是否能被正确导入，以及app属性是否存在
"""

try:
    # 尝试导入app模块
    import app
    
    # 检查app模块是否有app属性
    if hasattr(app, 'app'):
        print("✓ 成功导入app模块")
        print("✓ app模块中存在app属性")
        print("✓ 应用实例类型：", type(app.app))
        print("✓ 应用配置名称：", app.app.config.get('ENV'))
        print("✓ 应用调试模式：", app.app.debug)
        print("\n测试结果：成功！Gunicorn应该能够找到app:app")
    else:
        print("✗ app模块中不存在app属性")
        print("可用属性：", dir(app))
        print("\n测试结果：失败！Gunicorn将无法找到app:app")

except ImportError as e:
    print(f"✗ 无法导入app模块：{e}")
    print("\n测试结果：失败！请检查app模块的导入路径和结构")
except Exception as e:
    print(f"✗ 导入过程中发生错误：{e}")
    import traceback
    traceback.print_exc()
    print("\n测试结果：失败！请检查app模块的代码")
