import time

import pytest
from pywinauto.findwindows import find_window
from pywinauto.mouse import click

from config.config import WAIT_SHORT, AAC_PROCESSTIME

@pytest.mark.sa
@pytest.mark.order(1)
def test_initdata(app_operate):
    app_operate.main_window.set_focus()
    # 点击Open Data，还有待优化，目前是坐标定位
    click(coords=(190, 203))
    click(coords=(156, 226))
    # 选择数据集窗口
    racDialog = app_operate.main_window.child_window(title="打开", control_type="Window")
    racDialog.draw_outline()

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
    # 断言加载成功
    app_operate.assertor.assert_tree_node_exists("Demo", "data_test.xtf")

@pytest.mark.sa
@pytest.mark.order(2)
def test_SA(app_operate):
    # 1. 确保主窗口激活（可选，防止程序在后台）
    app_operate.main_window.set_focus()
    time.sleep(WAIT_SHORT)
    # 点击Acoustics模块
    app_operate.click_control(
        control_type="TabItem",
        name="Acoustics"
    )

    # 点击SA模块
    app_operate.click_control(
        control_type="Button",
        name="Slowness Analysis"
    )
    time.sleep(WAIT_SHORT)  # 点击后等待反馈
    # 输入曲线
    app_operate.input_text_to_edit_sendkeys(
        control_type="Edit",
        name="Channel Row 0, Not sorted.",
        input_text="ds:F1;ch:WV01",
        is_needenter=1
    )
    # 点击运行
    app_operate.click_control(
        control_type="Button",
        name="Run"
    )

    # 断言出现进度条
    # analysis_dialog = app_operate.app.window(title="SlownessAnalysis")
    # assert analysis_dialog.exists()

    # 等待进度条消失
    time.sleep(AAC_PROCESSTIME)

    # 断言图像比对
    app_operate.assert_image_match(img_name="sa.png",region=(885,215,815,587),threshold=0.85)

    # 切换到Parameter页签
    app_operate.click_control(control_type="TabItem",name="Parameters")

    # 输入数据
    # 频率数据
    #app_operate.input_text_to_edit(control_type="Edit",name="Value Row 16",input_text="1000")
    app_operate.input_text_to_edit_sendkeys(control_type="Edit",name="Value Row 16",input_text="1000")
    app_operate.input_text_to_edit_sendkeys(control_type="Edit",name="Value Row 17",input_text="8000")
    # 时差相关数据
    parent_scrollbar = app_operate.get_control(control_type="ScrollBar",name="Vertical Scroll Bar")
    for i in range(3):
        app_operate.click_control(control_type="Button",name="下一行",parent=parent_scrollbar)
    app_operate.input_text_to_edit_sendkeys(control_type="Edit",name="Value Row 22",input_text="35.86")
    app_operate.input_text_to_edit_sendkeys(control_type="Edit",name="Value Row 23",input_text="55.1776")
    app_operate.input_text_to_edit_sendkeys(control_type="Edit",name="Value Row 24",input_text="97.7876")
    app_operate.input_text_to_edit_sendkeys(control_type="Edit",name="Value Row 25",input_text="120.0376")




    # 再次点击运行
    app_operate.click_control(
        control_type="Button",
        name="Run"
    )

    # 等待进度条消失
    time.sleep(AAC_PROCESSTIME)

    # 断言图像比对
    app_operate.assert_image_match(img_name="sa2.png",region=(885,215,815,587),threshold=0.85)

def test_SATA(app_operate):
    # 1. 确保主窗口激活（可选，防止程序在后台）
    app_operate.main_window.set_focus()
    time.sleep(WAIT_SHORT)
    # 点击Acoustics模块
    app_operate.click_control(
        control_type="TabItem",
        name="Acoustics"
    )

    # 点击SATA模块
    app_operate.click_control(
        control_type="Button",
        name="Single Arrive Time Analysis"
    )
    time.sleep(WAIT_SHORT)  # 点击后等待反馈
    # 输入曲线TRWV
    app_operate.input_text_to_edit_sendkeys(
        control_type="Edit",
        name="Channel Row 0, Not sorted.",
        input_text="ds:F1;ch:WV01"
    )
    # 输入曲线ATOUT
    app_operate.input_text_to_edit_sendkeys(
        control_type="Edit",
        name="Channel Row 1, Not sorted.",
        input_text="ds:F3;ch:ATOUT"
    )
    # 输入曲线MAXFLAG
    app_operate.input_text_to_edit_sendkeys(
        control_type="Edit",
        name="Channel Row 3, Not sorted.",
        input_text="ds:F3;ch:MAXFLAG"
    )
    # 点击运行
    app_operate.click_control(
        control_type="Button",
        name="Run"
    )

    # 断言出现进度条
    # analysis_dialog = app_operate.app.window(title="SlownessAnalysis")
    # assert analysis_dialog.exists()

    # 等待进度条消失
    time.sleep(AAC_PROCESSTIME)

    # 断言图像比对
    app_operate.assert_image_match(img_name="sata.png", region=(610, 216, 931, 568), threshold=0.85)

    # 切换到Parameter页签
    app_operate.click_control(control_type="TabItem", name="Parameters")

    # 输入数据
    # 频率数据
    app_operate.input_text_to_edit(control_type="Edit", name="Value Row 7", input_text="8860")
    app_operate.input_text_to_edit(control_type="Edit", name="Value Row 8", input_text="13480")

    # 再次点击运行
    app_operate.click_control(
        control_type="Button",
        name="Run"
    )

    # 等待进度条消失
    time.sleep(AAC_PROCESSTIME)

    # 断言图像比对
    app_operate.assert_image_match(img_name="sata2.png", region=(610, 216, 931, 568), threshold=0.85)

def test_AATA(app_operate):
    # 1. 确保主窗口激活（可选，防止程序在后台）
    app_operate.main_window.set_focus()
    time.sleep(WAIT_SHORT)
    # 点击Acoustics模块
    app_operate.click_control(
        control_type="TabItem",
        name="Acoustics"
    )

    # 点击SATA模块
    app_operate.click_control(
        control_type="Button",
        name="Array Arrive Time Analysis"
    )
    time.sleep(WAIT_SHORT)  # 点击后等待反馈
    # 输入曲线
    app_operate.input_text_to_edit_sendkeys(
        control_type="Edit",
        name="Channel Row 0, Not sorted.",
        input_text="ds:F1;ch:WV01"
    )

    app_operate.input_text_to_edit_sendkeys(
        control_type="Edit",
        name="Channel Row 1, Not sorted.",
        input_text="ds:F2;ch:TTime_R"
    )
    # 点击运行
    app_operate.click_control(
        control_type="Button",
        name="Run"
    )

    # 断言出现进度条
    # analysis_dialog = app_operate.app.window(title="SlownessAnalysis")
    # assert analysis_dialog.exists()

    # 等待进度条消失
    time.sleep(AAC_PROCESSTIME)

    # 断言图像比对
    app_operate.assert_image_match(img_name="sata.png", region=(610, 216, 931, 568), threshold=0.85)

    # 切换到Parameter页签
    app_operate.click_control(control_type="TabItem", name="Parameters")

    # 输入数据
    # 频率数据
    app_operate.input_text_to_edit(control_type="Edit", name="Value Row 7", input_text="8860")
    app_operate.input_text_to_edit(control_type="Edit", name="Value Row 8", input_text="13480")

    # 再次点击运行
    app_operate.click_control(
        control_type="Button",
        name="Run"
    )

    # 等待进度条消失
    time.sleep(AAC_PROCESSTIME)

    # 断言图像比对
    app_operate.assert_image_match(img_name="sata2.png", region=(610, 216, 931, 568), threshold=0.85)