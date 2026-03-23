# testcases/test_module1.py
"""模块1：基础操作验证（示例：程序启动、窗口最大化、目标控件点击）"""
from config.config import WAIT_SHORT, CONTROL_TIMEOUT, WAIT_LONG
import time
from pywinauto.mouse import click

from core import app_assert


def test_createproject(app_operate):
    #1. 确保主窗口激活（可选，防止程序在后台）
    app_operate.main_window.set_focus()
    time.sleep(WAIT_SHORT)

    # 点击新建项目
    app_operate.click_control(
        control_type="SplitButton",
        name="Application"
    )
    time.sleep(WAIT_SHORT)  # 点击后等待反馈

    # 点击New，还有待优化，目前是坐标定位
    click(coords=(42, 69))
    time.sleep(WAIT_SHORT)  # 点击后等待反馈
    # 点击新建项目窗口的Create
    app_operate.click_control(
        control_type="Button",
        name="Create"
    )

    # 断言项目新增成功

