import pprint
import time

import pyautogui
from pywinauto.mouse import click
from config.config import WAIT_SHORT
from utils.InputMethod import InputMethod


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
        input_text=r"D:\data\GR.las"
    )
    # 点击打开
    app_operate.click_control(
        control_type="Button",
        name="打开(O)"
    )
    # 断言加载成功
    app_operate.assertor.assert_tree_node_exists("Demo", "GR.las")

def test_addDepthLog(app_operate):
    # 激活主窗口
    app_operate.main_window.set_focus()

    #点击Demo按钮
    app_operate.click_control(
        control_type="TreeItem",
        name="Demo"
    )

    # 点击Project模块
    app_operate.click_control(
        control_type="TabItem",
        name="Project"
    )

    # 定位到ribbon控件
    ribbonDialog = app_operate.main_window.child_window(title="Lower Ribbon", control_type="Pane")
    ribbonDialog.draw_outline()

    # 点击Depth Log
    app_operate.click_control_sub_window(sub_window=ribbonDialog,
                                         control_type="Button",
                                         name="Depth Log"
                                         )
    #定位到新增窗口
    newCanvasDialog = app_operate.main_window.child_window(title="Create New Canvas_WellLog Canvas", control_type="Window")
    newCanvasDialog.draw_outline()

    # 判断Use Template Canvas是否选中，选中就去掉勾选
    useTemplate = newCanvasDialog.child_window(title="Use Template Canvas", control_type="CheckBox")
    # print(useTemplate.get_properties())
    # print("选中属性", useTemplate.is_enabled())
    if useTemplate.is_enabled():
        app_operate.click_control_sub_window(sub_window=newCanvasDialog,control_type="CheckBox",name="Use Template Canvas")

    # 点击OK
    app_operate.click_control_sub_window(sub_window=newCanvasDialog,control_type="Button",name="OK")

    # 断言Demo下新增节点成功
    app_operate.assertor.assert_tree_node_exists("Demo", "LogPlot")

    # 定位到ribbon控件
    ribbonDialog = app_operate.main_window.child_window(title="Lower Ribbon", control_type="Pane")
    ribbonDialog.draw_outline()

    # 点击Basic
    app_operate.click_control_sub_window(sub_window=ribbonDialog,
                                         control_type="MenuItem",
                                         name="Basic"
                                         )
    time.sleep(WAIT_SHORT)

    # 点击Curve
    app_operate.click_coordinate(img_name="curve.png")

    time.sleep(WAIT_SHORT)

    # 点击测井图T1道
    app_operate.click_coordinate(img_name="curveT1.png")

    # 定位到属性控件
    # attDialog = app_operate.main_window.child_window(title="VoLogPrsCurve()", control_type="Pane",found_index=1)
    attDialog = app_operate.main_window.child_window(title="PropertyGrid", control_type="Pane")
    attDialog.draw_outline()

    # 滚动滚动条，让DataName可见
    app_operate.click_control_sub_window(sub_window=attDialog,control_type="Button",name="向上翻页")

    # 输入DataName ,=== 定位输入框报错，遍历DataName 项的所有子级控件也报错: Windows fatal exception: code 0x8001010d
    # dataDailog = app_operate.main_window.child_window(title="DataName", control_type="DataItem")
    # dataDailog.draw_outline()
    # app_operate.input_text_to_sub_window_edit(sub_window=dataDailog,
    #                                           control_type="Edit",
    #                                           name="DataName",
    #                                           input_text="ds:F1;ch:GR"
    #                                      )

    # 改成坐标输入
    app_operate.click_coordinate(img_name="dataname.png")
    time.sleep(WAIT_SHORT)
    pyautogui.press('shift')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.typewrite("ds:F1;ch:GR")
    print("✅ 输入成功！")

    # 点击空白位置
    app_operate.click_coordinate(img_name="curveT1.png",movex=440)
    time.sleep(WAIT_SHORT)

    # 定位到属性控件
    wellattDialog = app_operate.main_window.child_window(title="WellLogCanvas(LogPlot)", control_type="Pane",found_index=1)
    wellattDialog.draw_outline()

    #输入起始和结束值
    app_operate.click_coordinate(img_name="endindex.png")
    time.sleep(WAIT_SHORT)
    pyautogui.press('shift')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.typewrite("3200")
    print("✅ 输入截止值成功！")


    app_operate.click_coordinate(img_name="startindex.png")
    time.sleep(WAIT_SHORT)
    pyautogui.press('shift')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.typewrite("1684")
    print("✅ 输入起始值成功！")

    # 点击空白位置触发更新
    app_operate.click_coordinate(img_name="curveT1.png",movex=440)
    time.sleep(WAIT_SHORT)

    #断言图像生成
    app_operate.assert_image_match(img_name="depthlog.png",region=(530,201,162,602))