# conftest.py
import pytest
from pywinauto import Application
from pywinauto.findwindows import find_window
from pywinauto import findwindows

from core.app_assert import DeepLoggingAssert
from core.app_operate import DeepLoggingOperate
from config.config import *


def print_all_windows():
    windows = findwindows.find_elements(visible_only=True)
    print("===== 系统中所有可见窗口 =====")
    for win in windows:
        win_title = win.name
        print(f"窗口标题：{win_title} | 句柄：{win.handle} | 类名：{win.class_name}")
    print("=============================")

# 新增：通过窗口标题查找已有程序的句柄
def get_existing_app_handle():
    """查找已打开的DeepLogging程序窗口句柄"""
    try:
        # 按窗口标题模糊匹配（替换为你的程序实际标题特征）
        handle = find_window(class_name="WindowsForms10.Window.8.app.0.2dac507_r6_ad1",title_re=WINDOW_TITLE_PATTERN)
        return handle
    except:
        raise RuntimeError(f"未找到已打开的程序窗口（匹配规则：{WINDOW_TITLE_PATTERN}）")

@pytest.fixture(scope="session")  # 整个测试会话只启动一次程序
def deeplogging_app():
    """连接已打开的程序，而非启动新程序"""
    # 1. 获取已有程序的句柄
    handle = get_existing_app_handle()
    # 2. 连接到已有程序进程
    app = Application(backend=BACKEND).connect(handle=handle)
    # （可选）验证连接成功
    assert app.is_process_running(), "连接已打开的程序失败"
    yield app
    # 3. 测试结束后不关闭程序（关键：保留已打开的界面）
    print("\n✅ 测试完成，已打开的程序界面保留")



    """启动程序，返回app对象，会话结束后关闭"""
    """
    # 启动程序
    app = Application(backend=BACKEND).start(APP_PATH)
    yield app

    # 测试结束后关闭程序（可选，根据需求是否保留）
    try:
        app.kill()
        print("\n✅ 程序已关闭")
    except Exception as e:
        print(f"\n⚠️  程序关闭失败：{e}")
    """


@pytest.fixture(scope="function")  # 每个用例前初始化操作类
def app_operate(deeplogging_app):
    """返回封装好的操作类对象，确保窗口最大化"""
    operate = DeepLoggingOperate(deeplogging_app)
    operate.maximize_window()  # 每个用例都确保窗口最大化
    return operate

