# core/assert_operate.py
from config.config import CONTROL_TIMEOUT, WAIT_SHORT
import time


class DeepLoggingAssert:
    def __init__(self, main_window):
        """初始化传入主窗口对象"""
        self.main_window = main_window

    def assert_tree_node_exists(self, parent_node_name, child_node_name):
        """
        断言树节点下存在指定子节点
        :param parent_node_name: 父节点名称（默认Demo）
        :param child_node_name: 子节点名称（默认data_test.xtf）
        """
        # 定位父节点
        parent_node = self.main_window.child_window(
            control_type="TreeItem",
            title=parent_node_name
        )
        parent_node.wait('exists', timeout=CONTROL_TIMEOUT)



        # 定位并断言子节点存在
        child_node = parent_node.child_window(
            control_type="TreeItem",
            title=child_node_name
        )
        assert child_node.exists(timeout=CONTROL_TIMEOUT), \
            f"❌ [{parent_node_name}]节点下未找到[{child_node_name}]子节点"
        print(f"✅ [{parent_node_name}]节点下存在[{child_node_name}]子节点")