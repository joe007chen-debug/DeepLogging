import time

from pywinauto.findwindows import find_window

from config.config import WAIT_SHORT, AAC_SHORTTIMEOUT


def test_SA(app_operate):
    #1. 确保主窗口激活（可选，防止程序在后台）
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
    #输入曲线
    app_operate.input_text_to_edit_sendkeys(
        control_type="Edit",
        name="Channel Row 0, Not sorted.",
        input_text="ds:F1;ch:WV01"
    )
    #点击运行
    app_operate.click_control(
        control_type="Button",
        name="Run"
    )

    #断言出现进度条
    analysis_dialog = app_operate.app.window(title="SlownessAnalysis")
    assert analysis_dialog.exists()