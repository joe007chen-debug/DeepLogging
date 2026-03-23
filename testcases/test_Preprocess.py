import os
import time

from pywinauto.mouse import click
import pyautogui
from config.config import WAIT_SHORT
from core.app_operate import DeepLoggingOperate

# 创建数据集
def test_createDataset(app_operate):
    # 1. 确保主窗口激活（可选，防止程序在后台）
    app_operate.main_window.set_focus()

    # 目前程序有bug，先进行注释
    #点击Demo按钮
    app_operate.click_control(
        control_type="TreeItem",
        name="Demo"
    )
    # 点击Create DataSet，还有待优化，目前是坐标定位
    click(coords=(190, 203))
    #点击创建数据集按钮
    click(coords=(180, 227))

    #点击OK按钮
    app_operate.click_control(
        control_type="Button",
        name="OK"
    )

    #断言节点新增成功
    app_operate.assertor.assert_tree_node_exists("Demo", "Dataset")

# 新增一条曲线
def test_addCurve(app_operate):
    app_operate.main_window.set_focus()
    # 收起项目树
    app_operate.click_control(
        control_type="Button",
        name="Collapse"
    )
    # 展开一级项目树
    app_operate.click_control(
        control_type="Button",
        name="Expand"
    )

    #点击Dataset按钮
    app_operate.click_control(
        control_type="TreeItem",
        name="Dataset"
    )

    # 点击Data模块
    app_operate.click_control(
        control_type="TabItem",
        name="Data"
    )

    # 点击Preprocess模块
    app_operate.click_control(
        control_type="Button",
        name="Preprocess"
    )

    # 点击Add Channel下拉菜单
    app_operate.click_control(
        control_type="MenuItem",
        name="Add Channel"
    )

    # 点击Add Channel按钮
    DeepLoggingOperate.click_coordinate("addChannel.png")

    # 选择数据集窗口
    racDialog = app_operate.main_window.child_window(title="Add New Channel",control_type="Window")
    racDialog.draw_outline()
    # 输入Alias
    app_operate.input_text_to_sub_window_edit(sub_window=racDialog,
                                              control_type="Edit",
                                              name="Alias",
                                              input_text="ANTQ")
    # 输入Name
    app_operate.input_text_to_sub_window_edit(sub_window=racDialog,
                                              control_type="Edit",
                                              name="Name",
                                              input_text="Curve1")
    # 输入Default Value
    app_operate.input_text_to_sub_window_edit(sub_window=racDialog,
                                              control_type="Edit",
                                              name="Default Value",
                                              input_text="8")
    # 点击ok
    app_operate.click_control_sub_window(sub_window=racDialog,
                                         control_type="Button",
                                         name="OK")


    #断言节点新增成功
    app_operate.assertor.assert_tree_node_exists("Dataset", "Curve1")

# 编辑曲线
def test_editCurve(app_operate):
    app_operate.main_window.set_focus()
    # 选中第一条记录
    app_operate.click_control(
        control_type="Header",
        name="Row 0"
    )

    # 定位到ribbon控件
    ribbonDialog = app_operate.main_window.child_window(title="Lower Ribbon", control_type="Pane")
    ribbonDialog.draw_outline()

    # 点击Edit Curve
    app_operate.click_control_sub_window(sub_window=ribbonDialog,
                                         control_type="Button",
                                         name="Edit Curve"
                                         )
    # 定位到Edit Curve Data弹窗
    editcurvedataDialog = app_operate.main_window.child_window(title="Edit Curve Data", control_type="Window")
    editcurvedataDialog.draw_outline()

    # 点击set Value按钮
    app_operate.click_control_sub_window(sub_window=editcurvedataDialog,
                                         control_type="Button",
                                         name="Set Value")
   # 定位到set Value弹窗
    setvalueDialog = app_operate.main_window.child_window(title="Set Value", control_type="Window")
    setvalueDialog.draw_outline()

    # 输入新的value值
    app_operate.input_text_to_sub_window_edit(sub_window=setvalueDialog,
                                              control_type="Edit",
                                              name="Value",
                                              input_text="9")

    # 点击OK
    app_operate.click_control_sub_window(sub_window=setvalueDialog,
                                         control_type="Button",
                                         name="OK")
    # 断言
    editcurvedataDialog.draw_outline()
    cell = editcurvedataDialog.child_window(control_type="Edit", title="Curve1 Row 0")
    actValue = cell.get_value()
    assert str(actValue) == "9"

    # 关闭窗口
    editcurvedataDialog.close()


def test_removeCurve(app_operate):
    app_operate.main_window.set_focus()

    # 选中第一条记录
    app_operate.click_control(
        control_type="Header",
        name="Row 0"
    )


    # 定位到ribbon控件
    ribbonDialog = app_operate.main_window.child_window(title="Lower Ribbon", control_type="Pane")
    ribbonDialog.draw_outline()

    # 点击remove Curve
    app_operate.click_control_sub_window(sub_window=ribbonDialog,
                                         control_type="Button",
                                         name="Remove"
                                         )
    # 定位到Delete Channel弹窗
    deleteDialog = app_operate.main_window.child_window(title="Delete Channel", control_type="Window")
    deleteDialog.draw_outline()

    #点击y按钮
    app_operate.click_control_sub_window(sub_window=deleteDialog,
                                         control_type="Button",
                                         name="是(Y)")

    # 断言节点删除成功
    app_operate.assertor.assert_tree_node_no_exists("Dataset", "Curve1")