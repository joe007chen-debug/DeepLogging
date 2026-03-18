import os
import time

from pywinauto.mouse import click
import pyautogui
from config.config import WAIT_SHORT
from core.app_operate import DeepLoggingOperate


def test_createDataset(app_operate):
    # 1. 确保主窗口激活（可选，防止程序在后台）
    app_operate.main_window.set_focus()

    # 目前程序有bug，先进行注释
    #点击Demo按钮
    # app_operate.click_control(
    #     control_type="TreeItem",
    #     name="Demo"
    # )
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

    app_operate.input_text_to_sub_window_edit(sub_window=racDialog,
                                              control_type="Edit",
                                              name="Alias",
                                              input_text="ANTQ")