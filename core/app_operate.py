# core/app_operate.py
import os
import time
import io


import pyautogui
from pywinauto import Application
from config.config import *
from core.app_assert import DeepLoggingAssert
from pywinauto.keyboard import send_keys
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np

class DeepLoggingOperate:
    """DeepLogging程序操作封装类"""

    def __init__(self, app):
        self.app = app
        self.main_window = self.get_main_window()
        self.assertor = DeepLoggingAssert(self.main_window)

    def get_main_window(self):
        """获取主窗口对象"""
        #main_window = self.app.window(title_re=WINDOW_TITLE_PATTERN)
        main_window = self.app.window(class_name="WindowsForms10.Window.8.app.0.2dac507_r6_ad1",title_re=WINDOW_TITLE_PATTERN)
        main_window.wait("ready", timeout=LAUNCH_TIMEOUT)
        return main_window

    def maximize_window(self):
        """最大化窗口（带验证）"""
        self.main_window.maximize()
        """
        # 验证窗口是否最大化
        assert self.main_window.rectangle().width == self.main_window.screen_width(), \
            "窗口最大化失败"
        """
        return self

    """主窗口点击"""
    def click_control(self, control_type, name, timeout=CONTROL_TIMEOUT):
        """通用控件点击方法（适配所有模块的控件点击）"""
        target_control = self.main_window.child_window(
            control_type=control_type,
            title=name
        )
        # 前置验证
        assert target_control.exists(timeout=timeout), f"控件[{name}]不存在"
        assert target_control.is_visible(), f"控件[{name}]不可见"
        assert target_control.is_enabled(), f"控件[{name}]不可点击"

        # 执行点击
        target_control.click_input()
        return self

    """主窗口录入"""
    def input_text_to_edit(self,control_type="Edit", name="", input_text="", timeout=8):
        """
        通用输入框录入方法
        :param control_type: 输入框控件类型（默认Edit，UIA后端常用）
        :param name: 输入框的title/name属性（定位标识）
        :param input_text: 要录入的文本
        :param timeout: 控件加载超时时间
        :return: self（支持链式调用）
        """
        # 1. 定位输入框控件
        edit_control = self.main_window.child_window(
            control_type=control_type,
            title=name  # 按输入框的name/title定位，也可改用automation_id
        )

        # 2. 前置验证：确保输入框存在、可见、可编辑
        try:
            edit_control.wait('visible', timeout=timeout)
            assert edit_control.exists(), f"输入框[{name}]不存在"
            assert edit_control.is_visible(), f"输入框[{name}]不可见"
            assert edit_control.is_enabled(), f"输入框[{name}]不可编辑"
        except Exception as e:
            raise RuntimeError(f"输入框[{name}]验证失败：{str(e)}")

        # 3. 激活输入框（确保焦点在输入框）
        edit_control.click_input()
        time.sleep(WAIT_SHORT)  # 等待焦点激活

        # 4. 清空原有内容（通用方案：全选+删除）
        edit_control.type_keys('^a')  # Ctrl+A 全选
        time.sleep(WAIT_SHORT)
        edit_control.type_keys('{DELETE}')  # 删除选中内容
        time.sleep(WAIT_SHORT)

        # 5. 输入目标文本（支持特殊字符，如换行、空格等）
        edit_control.type_keys(input_text, with_spaces=True, with_newlines=True)
        time.sleep(WAIT_SHORT)

        # 6. 可选：验证输入结果（确保录入正确）
        actual_text = edit_control.get_value()  # 获取输入框当前内容
        assert actual_text == input_text, f"输入验证失败！预期：{input_text}，实际：{actual_text}"

        print(f"✅ 输入框[{name}]录入成功，内容：{input_text}")
        return self  # 链式调用，如 app_operate.click_control(...).input_text_to_edit(...)



    """针对不适合type_keys方式录入数据的，采用send_keys方式录入"""
    def input_text_to_edit_sendkeys(self, control_type="Edit", name="", input_text="", timeout=8):
        """
        通用输入框录入方法
        :param control_type: 输入框控件类型（默认Edit，UIA后端常用）
        :param name: 输入框的title/name属性（定位标识）
        :param input_text: 要录入的文本
        :param timeout: 控件加载超时时间
        :return: self（支持链式调用）
        """
        # 1. 定位输入框控件
        edit_control = self.main_window.child_window(
            control_type=control_type,
            title=name  # 按输入框的name/title定位，也可改用automation_id
        )

        # 2. 前置验证：确保输入框存在、可见、可编辑
        try:
            edit_control.wait('visible', timeout=timeout)
            assert edit_control.exists(), f"输入框[{name}]不存在"
            assert edit_control.is_visible(), f"输入框[{name}]不可见"
            assert edit_control.is_enabled(), f"输入框[{name}]不可编辑"
        except Exception as e:
            raise RuntimeError(f"输入框[{name}]验证失败：{str(e)}")

        # 3. 激活输入框（确保焦点在输入框）
        edit_control.click_input()
        time.sleep(WAIT_SHORT)  # 等待焦点激活

        # 5. 输入目标文本（支持特殊字符，如换行、空格等）
        send_keys(input_text, pause=0.1)
        send_keys('{ENTER}', pause=0.2)
        send_keys('{ENTER}', pause=0.2)
        time.sleep(WAIT_SHORT)


        print(f"✅ 输入框[{name}]录入成功，内容：{input_text}")
        return self  # 链式调用，如 app_operate.click_control(...).input_text_to_edit(...)
    def is_process_running(self):
        """验证程序进程是否运行"""
        return self.app.is_process_running()

    """弹出窗界面的点击，增加了一个窗口定位"""
    def click_control_sub_window(self, sub_window,control_type, name, timeout=CONTROL_TIMEOUT):
        """通用控件点击方法（适配所有模块的控件点击）"""
        target_control = sub_window.child_window(
            control_type=control_type,
            title=name
        )
        # 前置验证
        assert target_control.exists(timeout=timeout), f"控件[{name}]不存在"
        assert target_control.is_visible(), f"控件[{name}]不可见"
        assert target_control.is_enabled(), f"控件[{name}]不可点击"

        # 执行点击
        target_control.click_input()
        return self


    """弹出窗口界面的录入，增加了一个窗口定位"""
    def input_text_to_sub_window_edit(self,sub_window,control_type="Edit", name="", input_text="", timeout=8):
        """
        通用输入框录入方法
        :subwindow:子窗口
        :param control_type: 输入框控件类型（默认Edit，UIA后端常用）
        :param name: 输入框的title/name属性（定位标识）
        :param input_text: 要录入的文本
        :param timeout: 控件加载超时时间
        :return: self（支持链式调用）
        """
        # 1. 定位输入框控件
        edit_control = sub_window.child_window(
            control_type=control_type,
            title=name  # 按输入框的name/title定位，也可改用automation_id
        )

        # 2. 前置验证：确保输入框存在、可见、可编辑
        try:
            edit_control.wait('visible', timeout=timeout)
            assert edit_control.exists(), f"输入框[{name}]不存在"
            assert edit_control.is_visible(), f"输入框[{name}]不可见"
            assert edit_control.is_enabled(), f"输入框[{name}]不可编辑"
        except Exception as e:
            raise RuntimeError(f"输入框[{name}]验证失败：{str(e)}")

        # 3. 激活输入框（确保焦点在输入框）
        edit_control.click_input()
        time.sleep(WAIT_SHORT)  # 等待焦点激活

        # 4. 清空原有内容（通用方案：全选+删除）
        edit_control.type_keys('^a')  # Ctrl+A 全选
        time.sleep(WAIT_SHORT)
        edit_control.type_keys('{DELETE}')  # 删除选中内容
        time.sleep(WAIT_SHORT)

        # 5. 输入目标文本（支持特殊字符，如换行、空格等）
        edit_control.type_keys(input_text, with_spaces=True, with_newlines=True)
        time.sleep(WAIT_SHORT)

        # 6. 可选：验证输入结果（确保录入正确）
        actual_text = edit_control.get_value()  # 获取输入框当前内容
        assert actual_text == input_text, f"输入验证失败！预期：{input_text}，实际：{actual_text}"

        print(f"✅ 输入框[{name}]录入成功，内容：{input_text}")
        return self  # 链式调用，如 app_operate.click_control(...).input_text_to_edit(...)


    """用于识别不出来特征的控件，用pyautogui识别图片找到坐标点击"""
    @staticmethod
    def click_coordinate(img_name,confidence=0.8,duration=0.3,movex=0,movey=0):
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.getcwd()
        img_path = os.path.join(base_dir,"testcases", "imgs","input",img_name)
        try:
            icon_pos = pyautogui.locateOnScreen(img_path, confidence=0.8)
            if icon_pos:
                center_x, center_y = pyautogui.center(icon_pos)
                pyautogui.moveTo(center_x+movex, center_y+movey, duration=0.3)
                pyautogui.click()
            else:
                print("定位失败，请尝试调低confidence")
        except Exception as e:
            print("发生异常:", e)

    @staticmethod
    def assert_image_match(region, img_name, threshold=0.85):
        # 1. 截图
        screenshot = pyautogui.screenshot(region=region)

        # 2. 读取基准图
        base_dir = os.getcwd()
        img_path = os.path.join(base_dir, "testcases", "imgs", "assert", img_name)
        baseline = Image.open(img_path)

        # ====================== 修复核心：统一尺寸 + 统一通道 ======================
        # 把截图缩放到和基准图一样大小
        screenshot = screenshot.resize(baseline.size, Image.Resampling.LANCZOS)

        # 统一转成 RGB（去掉透明通道）
        screenshot_rgb = screenshot.convert("RGB")
        baseline_rgb = baseline.convert("RGB")

        # 转数组
        img1 = np.array(screenshot_rgb)
        img2 = np.array(baseline_rgb)

        # 3. 计算相似度
        ssim_score = ssim(img1, img2, channel_axis=2)

        # 4. 断言
        assert ssim_score >= threshold, f"图片相似度不足：{ssim_score:.2f} < {threshold}"
        print(f"✅ 图片断言成功！相似度 = {ssim_score:.2f}")