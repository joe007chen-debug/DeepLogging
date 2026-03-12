# testcases/test_module1.py
"""模块1：基础操作验证（示例：程序启动、窗口最大化、目标控件点击）"""
from config.config import WAIT_SHORT, CONTROL_TIMEOUT
import time
from pywinauto.mouse import click

from core import app_assert


def test_module1_click_target_button(app_operate):
    # 1. 确保主窗口激活（可选，防止程序在后台）
    app_operate.main_window.set_focus()
    time.sleep(WAIT_SHORT)
    # 临时注释
    # 点击新建项目
    # app_operate.click_control(
    #     control_type="SplitButton",
    #     name="Application"
    # )
    # time.sleep(WAIT_SHORT)  # 点击后等待反馈
    #
    # # 点击New，还有待优化，目前是坐标定位
    # click(coords=(42, 69))
    # time.sleep(WAIT_SHORT)  # 点击后等待反馈
    # # 点击新建项目窗口的Create
    # app_operate.click_control(
    #     control_type="Button",
    #     name="Create"
    # )

    # 点击Open Data，还有待优化，目前是坐标定位
    click(coords=(190, 203))
    click(coords=(156, 226))
    # 选择数据集窗口
    app_operate.input_text_to_edit(
        control_type="Edit",
        name="文件名(N):",
        input_text=r"D:\data\data_test.xtf"
    )
    # 点击打开
    app_operate.click_control(
            control_type="Button",
            name="打开(O)"
        )

    app_operate.assertor.assert_tree_node_exists("Demo","data_test.xtf")

    print("✅ 模块1-用例3：目标控件点击验证通过")