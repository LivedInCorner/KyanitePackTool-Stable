"""
由AI生成（未审查）
"""

import sys
import os
import shutil
import json
import sys
import resource_rc

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QFrame, QGridLayout, QGroupBox, QFileDialog, QProgressBar, QComboBox, QSizePolicy, QColorDialog, QScrollArea, QDialog, QCheckBox, QMessageBox, QLineEdit, QMenu, QToolBar, QMenuBar, QTabWidget, QAction)
from PyQt5.QtCore import Qt, QSize, QRect, pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QStyle
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPainter, QBrush, QPen, QTextCharFormat, QTextCursor, QIntValidator

# 现代化提示窗口类
class ModernMessageBox(QDialog):
    """自定义现代化提示窗口"""
    
    # 按钮类型常量
    OK = 0
    YES_NO = 1
    YES_NO_CANCEL = 2
    
    # 图标类型常量
    INFO = 0
    WARNING = 1
    ERROR = 2
    QUESTION = 3
    SUCCESS = 4
    
    def __init__(self, title="提示", message="", parent=None, 
                 icon_type=INFO, button_type=OK, width=400, height=200):
        super().__init__(parent)
        
        # 设置窗口属性
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
        self.setWindowModality(Qt.ApplicationModal)
        
        # 设置窗口图标（使用资源文件中的图标）
        self.setWindowIcon(QIcon(":/resource/icon.ico"))
        
        # 存储用户选择的按钮
        self.result = None
        
        # 创建UI
        self.init_ui(message, icon_type, button_type)
        
    def init_ui(self, message, icon_type, button_type):
        """
    初始化UI组件
    """
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)
        
        # 创建内容区域布局
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # 添加图标
        icon_label = self.create_icon(icon_type)
        content_layout.addWidget(icon_label, alignment=Qt.AlignTop)
        
        # 添加消息文本
        message_label = QLabel(message)
        message_label.setObjectName("messageText")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        content_layout.addWidget(message_label, 1)
        
        main_layout.addLayout(content_layout)
        
        # 添加按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        button_layout.setSpacing(12)
        
        # 根据按钮类型添加按钮
        if button_type == self.OK:
            ok_button = self.create_button("确定", "primary")
            ok_button.clicked.connect(self.accept)
            button_layout.addWidget(ok_button)
        elif button_type == self.YES_NO:
            yes_button = self.create_button("是", "primary")
            yes_button.clicked.connect(lambda: self.set_result_and_close(True))
            
            no_button = self.create_button("否", "secondary")
            no_button.clicked.connect(lambda: self.set_result_and_close(False))
            
            button_layout.addWidget(no_button)
            button_layout.addWidget(yes_button)
        elif button_type == self.YES_NO_CANCEL:
            yes_button = self.create_button("是", "primary")
            yes_button.clicked.connect(lambda: self.set_result_and_close(True))
            
            no_button = self.create_button("否", "secondary")
            no_button.clicked.connect(lambda: self.set_result_and_close(False))
            
            cancel_button = self.create_button("取消", "secondary")
            cancel_button.clicked.connect(self.reject)
            
            button_layout.addWidget(cancel_button)
            button_layout.addWidget(no_button)
            button_layout.addWidget(yes_button)
        
        main_layout.addLayout(button_layout)
        
        # 设置样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            
            #messageText {
                color: #333;
                font-size: 16px;
                line-height: 1.6;
            }
            
            QPushButton {
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                min-width: 70px;
                max-width: 120px;
                height: 36px;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
            
            QPushButton:pressed {
                opacity: 0.8;
            }
            
            .primary-button {
                background-color: #0078d4;
                color: white;
                border: none;
            }
            
            .primary-button:hover {
                background-color: #106ebe;
            }
            
            .secondary-button {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ddd;
            }
            
            .secondary-button:hover {
                background-color: #e0e0e0;
            }
        """)
    
    def create_icon(self, icon_type):
        """
    根据图标类型创建图标标签
    """
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        
        # 根据图标类型选择样式
        if icon_type == self.INFO:
            icon_label.setStyleSheet("""
                background-color: #e3f2fd;
                border-radius: 24px;
                qproperty-alignment: AlignCenter;
                color: #1976d2;
                font-size: 24px;
                font-weight: bold;
            """)
            icon_label.setText("ℹ")
        elif icon_type == self.WARNING:
            icon_label.setStyleSheet("""
                background-color: #fff3e0;
                border-radius: 24px;
                qproperty-alignment: AlignCenter;
                color: #f57c00;
                font-size: 24px;
                font-weight: bold;
            """)
            icon_label.setText("!")
        elif icon_type == self.ERROR:
            icon_label.setStyleSheet("""
                background-color: #ffebee;
                border-radius: 24px;
                qproperty-alignment: AlignCenter;
                color: #d32f2f;
                font-size: 24px;
                font-weight: bold;
            """)
            icon_label.setText("×")
        elif icon_type == self.QUESTION:
            icon_label.setStyleSheet("""
                background-color: #e8f5e9;
                border-radius: 24px;
                qproperty-alignment: AlignCenter;
                color: #388e3c;
                font-size: 24px;
                font-weight: bold;
            """)
            icon_label.setText("?")
        elif icon_type == self.SUCCESS:
            icon_label.setStyleSheet("""
                background-color: #e8f5e9;
                border-radius: 24px;
                qproperty-alignment: AlignCenter;
                color: #388e3c;
                font-size: 24px;
                font-weight: bold;
            """)
            icon_label.setText("✓")
        
        return icon_label
    
    def create_button(self, text, button_type="secondary"):
        """
    创建按钮
    """
        button = QPushButton(text)
        if button_type == "primary":
            button.setObjectName("primaryButton")
            button.setProperty("class", "primary-button")
        else:
            button.setObjectName("secondaryButton")
            button.setProperty("class", "secondary-button")
        return button
    
    def set_result_and_close(self, result):
        """
    设置结果并关闭窗口
    """
        self.result = result
        self.accept()
    
    def exec_(self):
        """
    exec_方法，返回用户选择的结果
    """
        super().exec_()
        return self.result
    
    # 静态方法，提供简便的API
    @staticmethod
    def info(parent, title, message):
        """
    显示信息提示框
    """
        msg_box = ModernMessageBox(title, message, parent, ModernMessageBox.INFO)
        return msg_box.exec_()
    
    @staticmethod
    def warning(parent, title, message):
        """
    显示警告提示框
    """
        msg_box = ModernMessageBox(title, message, parent, ModernMessageBox.WARNING)
        return msg_box.exec_()
    
    @staticmethod
    def error(parent, title, message):
        """
    显示错误提示框
    """
        msg_box = ModernMessageBox(title, message, parent, ModernMessageBox.ERROR)
        return msg_box.exec_()
    
    @staticmethod
    def question(parent, title, message):
        """
    显示询问提示框
    """
        msg_box = ModernMessageBox(title, message, parent, ModernMessageBox.QUESTION, ModernMessageBox.YES_NO)
        return msg_box.exec_()
    
    @staticmethod
    def success(parent, title, message):
        """
    显示成功提示框
    """
        msg_box = ModernMessageBox(title, message, parent, ModernMessageBox.SUCCESS)
        return msg_box.exec_()

# 物品大小对话框类
class ItemSizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("自定义物品大小")
        self.setFixedSize(1000, 700)  # 窗口大小
        self.setWindowModality(Qt.ApplicationModal)  # 模态对话框
        
        # 设置窗口图标（使用资源文件中的图标）
        self.setWindowIcon(QIcon(":/resource/icon.ico"))
        
        # 创建物品控件字典
        self.item_widgets = {}
        
        # 设置样式
        self.setStyleSheet("""
            QDialog {
                font-family: 'Microsoft YaHei', sans-serif;
                background-color: #f0f0f0;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
            }
            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
            QScrollArea QWidget {
                background-color: #f0f0f0;
            }
            .itemRow {
                background-color: white;
                border-radius: 8px;
                margin-bottom: 10px;
                padding: 12px;
                border: 1px solid #ddd;
            }
            .itemNameLabel {
                font-size: 14px;
                font-weight: 500;
                color: #333;
                background-color: transparent;
                border: none;
                padding: 0;
            }
            .scaleComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                color: #333;
            }
            .scaleComboBox:hover {
                border-color: #0078d4;
                background-color: #f8f9fa;
            }
            .headerLabel {
                font-size: 16px;
                font-weight: bold;
                color: #0078d4;
                margin-bottom: 15px;
            }
        """)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建搜索栏
        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_label = QLabel("搜索物品：")
        search_label.setObjectName("subtitleLabel")
        self.search_input = QTextEdit()
        self.search_input.setMaximumHeight(50)
        self.search_input.setPlaceholderText("输入物品名称进行搜索...")
        self.search_input.textChanged.connect(self.filter_items)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        # 创建列表标题
        header_label = QLabel("物品列表")
        header_label.setProperty("class", "headerLabel")
        
        # 创建列表区域，使用QScrollArea实现滚动
        self.scroll_area = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_area)
        
        # 添加表头
        header_frame = QFrame()
        header_frame.setProperty("class", "itemRow")
        header_frame.setStyleSheet("background-color: #f8f9fa;")
        header_layout = QHBoxLayout(header_frame)
        
        item_name_header = QLabel("物品名")
        item_name_header.setFixedWidth(400)
        item_name_header.setProperty("class", "headerLabel")
        
        handheld_scale_header = QLabel("手持放大")
        handheld_scale_header.setFixedWidth(150)
        handheld_scale_header.setProperty("class", "headerLabel")
        
        dropped_scale_header = QLabel("凋落物放大")
        dropped_scale_header.setFixedWidth(150)
        dropped_scale_header.setProperty("class", "headerLabel")
        
        header_layout.addWidget(item_name_header)
        header_layout.addWidget(handheld_scale_header)
        header_layout.addWidget(dropped_scale_header)
        
        # 添加表头到滚动布局
        self.scroll_layout.addWidget(header_frame)
        
        # 添加示例物品数据
        self.add_sample_items()
        
        # 加载保存的设置
        self.load_saved_settings()
        
        # 将滚动区域添加到QScrollArea
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.scroll_layout)
        
        self.scroll_area_container = QScrollArea()
        self.scroll_area_container.setWidgetResizable(True)
        self.scroll_area_container.setWidget(self.scroll_area_widget)
        
        # 添加底部按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        
        save_button = QPushButton("保存")
        save_button.setObjectName("startConversionButton")
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("取消")
        cancel_button.setObjectName("startConversionButton")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        # 添加到主布局
        main_layout.addWidget(search_frame)
        main_layout.addWidget(header_label)
        main_layout.addWidget(self.scroll_area_container)
        main_layout.addLayout(button_layout)
    
    def add_sample_items(self):
        # 初始化存储物品控件的数据结构
        self.item_widgets = {}
        
        # 创建物品名称翻译映射
        self.item_translations = {
            "anvil": "铁砧",
            "book": "书",
            "chipped_anvil": "开裂的铁砧",
            "cobweb": "蜘蛛网",
            "compass": "指南针",
            "damaged_anvil": "损坏的铁砧",
            "elytra": "鞘翅",
            "enchanted_golden_apple": "附魔金苹果",
            "enchanting_table": "附魔台",
            "ender_pearl": "末影珍珠",
            "experience_bottle": "附魔之瓶",
            "firework_rocket": "烟花火箭",
            "golden_apple": "金苹果",
            "golden_axe": "金斧",
            "netherite_sword": "下界合金剑",
            "player_head": "玩家头颅",
            "shield": "盾牌",
            "shield_blocking": "格挡下的盾牌",
            "slime_ball": "粘液球",
            "splash_potion": "喷溅药水",
            "totem_of_undying": "不死图腾",
            "trident": "三叉戟",
            "water_bucket": "水桶",
            "block": "方块"
        }
        
        # 重新组织物品数据，分为放大物品和缩小物品
        
        # 添加放大物品分类标题
        zoom_in_label = QLabel("放大物品")
        zoom_in_label.setProperty("class", "headerLabel")
        zoom_in_label.setStyleSheet("margin-top: 10px;")
        self.scroll_layout.addWidget(zoom_in_label)
        
        # 放大物品列表（移除了handheld_rod，并将totem_of_undying移到缩小物品列表）
        zoom_in_items = [
            "anvil", "book", "chipped_anvil", "cobweb", "compass", 
            "damaged_anvil", "elytra", "enchanted_golden_apple",
            "enchanting_table", "ender_pearl", "experience_bottle", "firework_rocket",
            "golden_apple", "golden_axe",
            "netherite_sword", "player_head", "slime_ball",
            "splash_potion", "trident", "water_bucket"
        ]
        
        for item_name in zoom_in_items:
            # 创建物品行框架
            item_frame = QFrame()
            item_frame.setProperty("class", "itemRow")
            item_row = QHBoxLayout(item_frame)
            
            # 创建物品名称标签，显示中文名称
            display_name = self.item_translations.get(item_name, item_name)
            item_label = QLabel(display_name)
            item_label.setFixedWidth(400)
            item_label.setProperty("class", "itemNameLabel")
            # 存储英文名称以便后续保存使用
            item_label.setObjectName(item_name)
            
            # 创建手持放大倍数下拉框
            handheld_combo = QComboBox()
            handheld_combo.setFixedWidth(150)
            handheld_combo.setProperty("class", "scaleComboBox")
            handheld_combo.addItems(["1x", "2x", "3x", "4x"])
            handheld_combo.setCurrentText("1x")
            
            # 创建凋落物放大倍数下拉框
            dropped_combo = QComboBox()
            dropped_combo.setFixedWidth(150)
            dropped_combo.setProperty("class", "scaleComboBox")
            dropped_combo.addItems(["1x", "2x", "3x", "4x"])
            dropped_combo.setCurrentText("1x")
            
            # 添加到物品行布局
            item_row.addWidget(item_label)
            item_row.addWidget(handheld_combo)
            item_row.addWidget(dropped_combo)
            
            # 将物品行添加到滚动区域布局
            self.scroll_layout.addWidget(item_frame)
            
            # 存储控件引用以便后续获取设置
            self.item_widgets[item_name] = {
                "type": "zoom_in",
                "handheld_combo": handheld_combo,
                "dropped_combo": dropped_combo
            }
        
        # 添加缩小物品分类标题
        zoom_out_label = QLabel("缩小物品")
        zoom_out_label.setProperty("class", "headerLabel")
        zoom_out_label.setStyleSheet("margin-top: 20px;")
        self.scroll_layout.addWidget(zoom_out_label)
        
        # 缩小物品列表（移除了generated.json，并添加了totem_of_undying）
        zoom_out_items = ["block",  "shield", "shield_blocking", "totem_of_undying"]
        
        for item_name in zoom_out_items:
            # 创建物品行框架
            item_frame = QFrame()
            item_frame.setProperty("class", "itemRow")
            item_row = QHBoxLayout(item_frame)
            
            # 创建物品名称标签，显示中文名称
            display_name = self.item_translations.get(item_name, item_name)
            item_label = QLabel(display_name)
            item_label.setFixedWidth(400)
            item_label.setProperty("class", "itemNameLabel")
            # 存储英文名称以便后续保存使用
            item_label.setObjectName(item_name)
            
            # 创建复选框用于确认是否缩小（占据两列宽度）
            shrink_check = QCheckBox("是否缩小")
            shrink_check.setChecked(False)
            
            # 创建一个水平布局来容纳复选框，使其占据两列宽度
            checkbox_layout = QHBoxLayout()
            checkbox_layout.setAlignment(Qt.AlignLeft)
            checkbox_layout.addWidget(shrink_check)
            
            # 添加到物品行布局
            item_row.addWidget(item_label)
            item_row.addLayout(checkbox_layout, 2)  # 占据2个单位的空间
            
            # 将物品行添加到滚动区域布局
            self.scroll_layout.addWidget(item_frame)
            
            # 存储控件引用以便后续获取设置
            self.item_widgets[item_name] = {
                "type": "zoom_out",
                "shrink_check": shrink_check
            }
    
    def add_item_row(self, item_name):
        # 创建物品行
        item_frame = QFrame()
        item_frame.setObjectName("itemRowFrame")
        item_frame.setStyleSheet("""
            #itemRowFrame {
                border-bottom: 1px solid #f0f0f0;
            }
        """)
        item_layout = QHBoxLayout(item_frame)
        
        # 物品名称
        item_label = QLabel(item_name)
        item_label.setFixedWidth(400)
        
        # 放大倍数选择
        scale_combo = QComboBox()
        scale_combo.setObjectName("scaleComboBox")
        scales = ["1x", "2x", "4x", "8x", "16x"]
        scale_combo.addItems(scales)
        scale_combo.setCurrentText("2x")
        
        item_layout.addWidget(item_label)
        item_layout.addWidget(scale_combo)
        
        # 添加到滚动布局
        self.scroll_layout.addWidget(item_frame)
    
    def filter_items(self):
        # 搜索过滤逻辑
        search_text = self.search_input.toPlainText().lower()
        
        # 获取所有物品行（跳过第一个是表头）
        for i in range(1, self.scroll_layout.count()):
            item_frame = self.scroll_layout.itemAt(i).widget()
            if item_frame:
                # 获取物品名称标签
                item_layout = item_frame.layout()
                if item_layout:
                    item_label = item_layout.itemAt(0).widget()
                    if item_label and isinstance(item_label, QLabel):
                        # 检查物品名称是否包含搜索文本（中文名称或英文名称）
                        chinese_name = item_label.text().lower()
                        english_name = item_label.objectName().lower()
                        
                        if search_text in chinese_name or search_text in english_name:
                            item_frame.show()
                        else:
                            item_frame.hide()
    
    def load_saved_settings(self):
        """
    从overlay.json文件加载保存的设置到自定义物品大小窗口
    """
        import json
        import os
        
        # 始终使用同一个固定位置的overlay.json文件
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 如果文件不存在，不执行加载
        if not os.path.exists(overlay_file):
            return
        
        try:
            # 使用utf-8-sig编码读取文件，确保能正确解析BOM
            with open(overlay_file, "r", encoding="utf-8-sig") as f:
                settings = json.load(f)
            
            # 支持新键名core_item_scaling和旧键名big_item、small_item的向后兼容性
            big_items = {}
            small_items = {}
            
            # 先检查是否有新的core_item_scaling设置
            if "core_item_scaling" in settings:
                core_item_scaling = settings["core_item_scaling"]
                if "big_item" in core_item_scaling:
                    big_items = core_item_scaling["big_item"]
                if "small_item" in core_item_scaling:
                    small_items = core_item_scaling["small_item"]
            # 如果没有新设置，回退到旧的顶层设置
            elif "big_item" in settings:
                big_items = settings["big_item"]
            if "small_item" in settings:
                small_items = settings["small_item"]
            
            # 应用放大物品的设置
            for item_name, item_data in big_items.items():
                if item_name in self.item_widgets and self.item_widgets[item_name]["type"] == "zoom_in":
                    item_widget = self.item_widgets[item_name]
                    if "handheld_scale" in item_data:
                        if item_data["handheld_scale"] in ["1x", "2x", "3x", "4x"]:
                            item_widget["handheld_combo"].setCurrentText(item_data["handheld_scale"])
                    if "dropped_scale" in item_data:
                        if item_data["dropped_scale"] in ["1x", "2x", "3x", "4x"]:
                            item_widget["dropped_combo"].setCurrentText(item_data["dropped_scale"])
            
            # 应用缩小物品的设置
            for item_name, item_data in small_items.items():
                if item_name in self.item_widgets and self.item_widgets[item_name]["type"] == "zoom_out":
                    item_widget = self.item_widgets[item_name]
                    if "should_shrink" in item_data:
                        item_widget["shrink_check"].setChecked(item_data["should_shrink"])
        except Exception as e:
            ModernMessageBox.warning(self, "加载失败", f"加载设置时出错: {str(e)}")
    
    def save_settings(self):
        """
    保存用户在自定义物品大小窗口中设置的选项到overlay.json文件
    """
        import json
        import os
        
        # 收集设置
        settings = {}
        
        # 分离放大和缩小的物品设置
        big_items = {}
        small_items = {}
        
        for item_name, item_data in self.item_widgets.items():
            if item_data["type"] == "zoom_in":
                big_items[item_name] = {
                    "type": "zoom_in",
                    "handheld_scale": item_data["handheld_combo"].currentText(),
                    "dropped_scale": item_data["dropped_combo"].currentText()
                }
            elif item_data["type"] == "zoom_out" and item_data["shrink_check"].isChecked():
                small_items[item_name] = {
                    "type": "zoom_out",
                    "should_shrink": True
                }
        
        # 如果有放大的物品，添加到big_item名称下
        if big_items:
            settings["big_item"] = big_items
        
        # 如果有缩小的物品，添加到small_item名称下
        if small_items:
            settings["small_item"] = small_items
        
        # 检查父窗口是否有color_disc属性，获取背景颜色的RGBA分量
        if hasattr(self.parent(), 'color_disc'):
            color_disc = self.parent().color_disc
            # 获取颜色的RGBA分量（0.0-1.0范围）
            settings["nametag"] = {
                "color": color_disc.get_rgba(),
                "enabled": True
            }
        
        # 创建temp_overlay文件夹
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        os.makedirs(temp_overlay_dir, exist_ok=True)
        
        # 始终使用同一个固定位置的overlay.json文件
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 如果文件已存在，先读取现有内容
        if os.path.exists(overlay_file):
            try:
                with open(overlay_file, "r", encoding="utf-8-sig") as f:
                    existing_settings = json.load(f)
                # 合并新的设置
                existing_settings.update(settings)
                settings = existing_settings
            except json.JSONDecodeError:
                # 如果文件格式错误，则创建新的设置对象
                existing_settings = {}
                settings = existing_settings
        
        # 写入文件，确保中文字符正确编码
        with open(overlay_file, "w", encoding="utf-8-sig") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        
        # 提示保存成功
        ModernMessageBox.success(self, "保存成功", f"设置已成功保存到 {overlay_file}")
        
        # 关闭对话框
        self.accept()

class CustomNameDialog(QDialog):
    # Minecraft 颜色和格式代码映射
    COLOR_CODES = {
        "黑色": "§0",
        "深蓝色": "§1",
        "深绿色": "§2",
        "深青色": "§3",
        "深红色": "§4",
        "紫色": "§5",
        "金色": "§6",
        "灰色": "§7",
        "深灰色": "§8",
        "蓝色": "§9",
        "绿色": "§a",
        "青色": "§b",
        "红色": "§c",
        "粉红色": "§d",
        "黄色": "§e",
        "白色": "§f"
    }
    
    # 颜色代码到实际颜色的映射
    CODE_TO_COLOR = {
        "§0": "#000000",  # 黑色
        "§1": "#0000AA",  # 深蓝色
        "§2": "#00AA00",  # 深绿色
        "§3": "#00AAAA",  # 深青色
        "§4": "#AA0000",  # 深红色
        "§5": "#AA00AA",  # 紫色
        "§6": "#FFAA00",  # 金色
        "§7": "#AAAAAA",  # 灰色
        "§8": "#555555",  # 深灰色
        "§9": "#5555FF",  # 蓝色
        "§a": "#55FF55",  # 绿色
        "§b": "#55FFFF",  # 青色
        "§c": "#FF5555",  # 红色
        "§d": "#FF55FF",  # 粉红色
        "§e": "#FFFF55",  # 黄色
        "§f": "#FFFFFF"   # 白色
    }
    
    FORMAT_CODES = {
        "随机": "§k",
        "粗体": "§l",
        "删除线": "§m",
        "下划线": "§n",
        "斜体": "§o",
        "重置": "§r"
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("自定义物品名称")
        # 设置最小尺寸但不固定最大尺寸，允许窗口适当扩展
        self.resize(600, 550)  # 初始尺寸
        self.setMinimumSize(600, 550)
        
        # 设置窗口图标（使用资源文件中的图标）
        self.setWindowIcon(QIcon(":/resource/icon.ico"))
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # 标题
        title = QLabel("自定义物品名称")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # 语言选择区域
        language_frame = QFrame()
        language_layout = QHBoxLayout(language_frame)
        language_layout.setContentsMargins(0, 0, 0, 0)
        language_layout.setSpacing(30)
        
        language_label = QLabel("选择语言：")
        language_label.setObjectName("dragDropLabel")
        
        # 创建中英文复选框
        self.english_checkbox = QCheckBox("英文")
        self.chinese_checkbox = QCheckBox("中文")
        
        # 默认选择中文
        self.chinese_checkbox.setChecked(True)
        
        # 连接信号，确保只有一个被选中
        self.english_checkbox.toggled.connect(lambda: self.on_language_checkbox_toggled(self.english_checkbox))
        self.chinese_checkbox.toggled.connect(lambda: self.on_language_checkbox_toggled(self.chinese_checkbox))
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.english_checkbox)
        language_layout.addWidget(self.chinese_checkbox)
        language_layout.addStretch()
        
        main_layout.addWidget(language_frame)
        
        # 创建滚动区域并保存为实例变量
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 滚动区域的内容
        self.scroll_content = QWidget()
        scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_layout.setSpacing(10)
        
        # 创建物品名称映射字典和格式化代码映射字典
        self.name_mappings = {}  # 存储QTextEdit引用
        self.format_codes = {}  # 存储包含格式化代码的原始文本
        
        # 添加滚动内容到滚动区域
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)
        
        # 底部按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        
        save_button = QPushButton("保存")
        save_button.setObjectName("startConversionButton")
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("取消")
        cancel_button.setObjectName("startConversionButton")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        main_layout.addLayout(button_layout)
        
        # 初始化物品名称列表
        self.initialize_item_list()
        
        # 加载已保存的设置
        self.load_saved_settings()
    
    def initialize_item_list(self):
        """
    根据选择的语言初始化物品名称列表，按类别组织显示
    """
        # 导入必要的模块
        import os
        import json
        
        # 重置映射字典
        self.name_mappings = {}
        self.format_codes = {}
        self.item_id_map = {}
        
        # 清空现有的内容
        scroll_layout = self.scroll_content.layout()
        while scroll_layout.count() > 0:
            item = scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()
                widget.deleteLater()
        
        # 确定使用的语言文件
        use_chinese = self.chinese_checkbox.isChecked()
        lang_file = "zh_cn.json" if use_chinese else "en_us.json"
        lang_file_path = os.path.join(os.getcwd(), "lang", lang_file)
        
        # 按类别组织物品ID列表
        item_categories = {
            "工具与武器": [
                "item.minecraft.diamond_sword", "item.minecraft.diamond_axe", "item.minecraft.diamond_pickaxe",
                "item.minecraft.diamond_shovel", "item.minecraft.diamond_hoe",
                "item.minecraft.iron_sword", "item.minecraft.iron_axe", "item.minecraft.iron_pickaxe",
                "item.minecraft.iron_shovel", "item.minecraft.iron_hoe",
                "item.minecraft.netherite_sword", "item.minecraft.netherite_axe", "item.minecraft.netherite_pickaxe",
                "item.minecraft.netherite_shovel", "item.minecraft.netherite_hoe",
                "item.minecraft.golden_sword", "item.minecraft.golden_axe", "item.minecraft.golden_pickaxe",
                "item.minecraft.golden_shovel", "item.minecraft.golden_hoe",
                "item.minecraft.stone_sword", "item.minecraft.stone_axe", "item.minecraft.stone_pickaxe",
                "item.minecraft.stone_shovel", "item.minecraft.stone_hoe",
                "item.minecraft.wooden_sword", "item.minecraft.wooden_axe", "item.minecraft.wooden_pickaxe",
                "item.minecraft.wooden_shovel", "item.minecraft.wooden_hoe",
                "item.minecraft.bow", "item.minecraft.crossbow", "item.minecraft.trident",
                "item.minecraft.fishing_rod", "item.minecraft.shears"
            ],
            "盔甲": [
                "item.minecraft.diamond_helmet", "item.minecraft.diamond_chestplate", "item.minecraft.diamond_leggings", "item.minecraft.diamond_boots",
                "item.minecraft.iron_helmet", "item.minecraft.iron_chestplate", "item.minecraft.iron_leggings", "item.minecraft.iron_boots",
                "item.minecraft.netherite_helmet", "item.minecraft.netherite_chestplate", "item.minecraft.netherite_leggings", "item.minecraft.netherite_boots",
                "item.minecraft.golden_helmet", "item.minecraft.golden_chestplate", "item.minecraft.golden_leggings", "item.minecraft.golden_boots",
                "item.minecraft.chainmail_helmet", "item.minecraft.chainmail_chestplate", "item.minecraft.chainmail_leggings", "item.minecraft.chainmail_boots",
                "item.minecraft.shield", "item.minecraft.elytra"
            ],
            "材料": [
                "item.minecraft.diamond", "item.minecraft.netherite_ingot", "item.minecraft.emerald",
                "item.minecraft.iron_ingot", "item.minecraft.gold_ingot",
                "item.minecraft.raw_iron", "item.minecraft.raw_gold", "item.minecraft.raw_copper",
                "item.minecraft.stick"
            ],
            "消耗品与其他": [
                "item.minecraft.apple", "item.minecraft.golden_apple", "item.minecraft.enchanted_golden_apple",
                "item.minecraft.bread", "item.minecraft.egg", "item.minecraft.feather",
                "item.minecraft.ender_pearl", "item.minecraft.experience_bottle", "item.minecraft.slime_ball",
                "item.minecraft.snowball", "item.minecraft.book", "item.minecraft.blaze_rod",
                "item.minecraft.end_crystal", "item.minecraft.bucket", "item.minecraft.water_bucket", "item.minecraft.lava_bucket",
                "item.minecraft.clock", "item.minecraft.compass", "item.minecraft.bowl"
            ]
        }
        
        # 加载语言文件
        lang_data = {}
        try:
            with open(lang_file_path, "r", encoding="utf-8-sig") as f:
                lang_data = json.load(f)
        except Exception as e:
            print(f"加载语言文件失败: {e}")
        
        # 处理每个类别的物品
        for category, item_ids in item_categories.items():
            # 添加类别标题
            category_label = QLabel(category)
            category_label.setObjectName("categoryTitle")
            category_label.setStyleSheet(
                "font-weight: bold; font-size: 14px; margin-top: 15px; margin-bottom: 5px; color: #333;")
            scroll_layout.addWidget(category_label)
            
            # 创建类别框架，为每个类别添加背景色以区分
            category_frame = QFrame()
            category_frame.setStyleSheet("background-color: #f9f9f9; border-radius: 5px; padding: 5px;")
            category_layout = QVBoxLayout(category_frame)
            category_layout.setContentsMargins(5, 5, 5, 5)
            category_layout.setSpacing(5)
            
            # 添加类别内的物品
            for item_id in item_ids:
                # 获取物品名称
                item_name = ""  
                if item_id in lang_data:
                    item_name = lang_data[item_id]
                    self.item_id_map[item_name] = item_id
                else:
                    # 从物品ID中提取名称作为备选
                    item_name = item_id.replace("item.minecraft.", "").replace("_", " ").title()
                    self.item_id_map[item_name] = item_id
                
                if item_name:
                    # 创建行容器
                    row_widget = QWidget()
                    row_widget.setMinimumHeight(38)
                    row_widget.setMaximumHeight(48)
                    row_widget.setStyleSheet("background-color: white; border: 1px solid #e0e0e0; border-radius: 3px;")
                    
                    # 创建行布局
                    row_layout = QHBoxLayout(row_widget)
                    row_layout.setContentsMargins(10, 5, 10, 5)
                    row_layout.setSpacing(15)
                    
                    # 原名称标签
                    original_name_label = QLabel(item_name)
                    original_name_label.setMinimumWidth(150)
                    original_name_label.setMaximumWidth(150)
                    original_name_label.setStyleSheet("color: #555;")
                    
                    # 使用QTextEdit以支持富文本
                    custom_name_edit = QTextEdit()
                    # 允许水平滚动以显示长文本
                    custom_name_edit.setLineWrapMode(QTextEdit.NoWrap)
                    custom_name_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    custom_name_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                    custom_name_edit.setStyleSheet("border: 1px solid #ddd; padding: 3px;")
                    
                    # 连接右键菜单信号
                    custom_name_edit.setContextMenuPolicy(Qt.CustomContextMenu)
                    custom_name_edit.customContextMenuRequested.connect(
                        lambda pos, edit=custom_name_edit, item=item_name: self.show_context_menu(pos, edit, item)
                    )
                    
                    # 连接文本变化信号
                    custom_name_edit.textChanged.connect(
                        lambda edit=custom_name_edit, item=item_name: self.update_format_codes(edit, item)
                    )
                    
                    # 存储引用
                    self.name_mappings[item_name] = custom_name_edit
                    self.format_codes[item_name] = ""
                    
                    # 添加到行布局
                    row_layout.addWidget(original_name_label)
                    row_layout.addWidget(custom_name_edit)
                    
                    # 添加到类别布局
                    category_layout.addWidget(row_widget)
            
            # 添加类别框架到滚动布局
            scroll_layout.addWidget(category_frame)
        
        # 添加一个占位符来确保滚动区域正常工作
        spacer = QWidget()
        spacer.setMinimumHeight(30)
        scroll_layout.addWidget(spacer)
        
        # 强制更新和调整大小
        self.scroll_content.update()
        scroll_layout.update()
        self.scroll_content.adjustSize()
        self.scroll_area.updateGeometry()
    
    def on_language_checkbox_toggled(self, checkbox):
        """
    处理语言复选框切换事件，确保只有一个复选框被选中
    """
        # 确保只有一个复选框被选中
        if checkbox.isChecked():
            if checkbox == self.english_checkbox:
                self.chinese_checkbox.setChecked(False)
            else:
                self.english_checkbox.setChecked(False)
            # 切换语言后重新初始化物品列表
            self.initialize_item_list()
            # 重新加载已保存的设置
            self.load_saved_settings()

    def load_saved_settings(self):
        """
    加载已保存的设置，包括语言偏好和自定义名称
    """
        import json
        import os
        
        # 从固定位置的overlay.json文件中加载设置
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        if os.path.exists(overlay_file):
            try:
                # 使用utf-8-sig编码读取，以支持带BOM的UTF-8文件
                with open(overlay_file, "r", encoding="utf-8-sig") as f:
                    settings = json.load(f)
                
                # 加载保存的语言偏好
                if "selected_language" in settings:
                    selected_language = settings["selected_language"]
                    if selected_language == "zh_cn":
                        self.chinese_checkbox.setChecked(True)
                        self.english_checkbox.setChecked(False)
                    else:
                        self.chinese_checkbox.setChecked(False)
                        self.english_checkbox.setChecked(True)
                
                # 加载自定义物品名称设置（支持新格式'lang_itemname'和旧格式'custom_item_names'）
                if "lang_itemname" in settings:
                    custom_names = settings["lang_itemname"]
                    # 创建一个反向映射，从物品ID映射到显示名称
                    reverse_id_map = {v: k for k, v in self.item_id_map.items()}
                    
                    for key, custom_name in custom_names.items():
                        # 检查key是否是物品ID（以"item.minecraft."开头）
                        if key.startswith("item.minecraft."):
                            # 查找对应的显示名称
                            if key in reverse_id_map and reverse_id_map[key] in self.name_mappings:
                                display_name = reverse_id_map[key]
                                self.format_codes[display_name] = custom_name
                                self.name_mappings[display_name].setPlainText(custom_name)
                        elif key in self.name_mappings:
                            # 如果key不是物品ID，可能是旧格式的显示名称
                            self.format_codes[key] = custom_name
                            self.name_mappings[key].setPlainText(custom_name)
                elif "custom_item_names" in settings:
                    # 向后兼容旧格式
                    custom_names = settings["custom_item_names"]
                    for original_name, custom_name in custom_names.items():
                        if original_name in self.name_mappings:
                            # 保存格式化代码
                            self.format_codes[original_name] = custom_name
                            # 显示到QTextEdit
                            self.name_mappings[original_name].setPlainText(custom_name)
            except Exception as e:
                print(f"加载自定义名称设置失败: {e}")
        
    def show_context_menu(self, position, edit_widget, item_name):
        """
    显示右键菜单，用于选择文本颜色和格式
    """
        # 获取QTextEdit的光标
        cursor = edit_widget.textCursor()
        selected_text = cursor.selectedText()
        
        if not selected_text:
            # 如果没有选中文本，就选中光标位置的整个单词
            cursor.select(QTextCursor.WordUnderCursor)
            selected_text = cursor.selectedText()
            edit_widget.setTextCursor(cursor)
            
        # 创建右键菜单
        menu = QMenu()
        
        # 添加文本选择状态显示
        if selected_text:
            menu.addAction(f"当前选择: '{selected_text}'").setEnabled(False)
        else:
            menu.addAction("未选择任何文本").setEnabled(False)
        
        menu.addSeparator()
        
        # 添加格式化选项组
        
        # 粗体
        bold_action = menu.addAction("粗体 (&B)")
        bold_action.triggered.connect(lambda checked, edit=edit_widget, item=item_name: 
                                      self.apply_formatting("§l", edit, item))
        
        # 斜体
        italic_action = menu.addAction("斜体 (&I)")
        italic_action.triggered.connect(lambda checked, edit=edit_widget, item=item_name: 
                                        self.apply_formatting("§o", edit, item))
        
        # 下划线
        underline_action = menu.addAction("下划线 (&U)")
        underline_action.triggered.connect(lambda checked, edit=edit_widget, item=item_name: 
                                           self.apply_formatting("§n", edit, item))
        
        # 删除线
        strikethrough_action = menu.addAction("删除线 (&S)")
        strikethrough_action.triggered.connect(lambda checked, edit=edit_widget, item=item_name: 
                                               self.apply_formatting("§m", edit, item))
        
        menu.addSeparator()
        
        # 添加颜色选择
        color_menu = menu.addMenu("文本颜色 (&C)")
        
        # 创建颜色菜单项
        for color_name, color_code in self.COLOR_CODES.items():
            color_action = color_menu.addAction(color_name)
            color_action.triggered.connect(lambda checked, code=color_code, edit=edit_widget, item=item_name: 
                                          self.apply_formatting(code, edit, item))
        
        menu.addSeparator()
        
        # 添加快捷操作
        action_menu = menu.addMenu("快捷操作 (&A)")
        
        # 复制原始名称
        copy_original_action = action_menu.addAction("复制原始名称 (&O)")
        copy_original_action.triggered.connect(lambda: self.copy_original_name(item_name))
        
        # 清空内容
        clear_action = action_menu.addAction("清空内容 (&L)")
        clear_action.triggered.connect(lambda: edit_widget.clear())
        
        # 应用默认格式到全部
        apply_default_to_all_action = action_menu.addAction("应用默认格式到全部 (&D)")
        apply_default_to_all_action.triggered.connect(lambda: self.apply_default_format_to_all())
        
        # 在鼠标位置显示菜单
        menu.exec_(edit_widget.mapToGlobal(position))
        

    def copy_original_name(self, item_name):
        """
    复制物品的原始名称到剪贴板
    """
        clipboard = QApplication.clipboard()
        clipboard.setText(item_name)
        
    def apply_default_format_to_all(self):
        """
    为所有物品应用默认的格式化样式
    """
        default_format = "§7"  # 默认使用灰色
        
        # 遍历所有物品并应用默认格式
        for item_name, edit_widget in self.name_mappings.items():
            current_text = edit_widget.toPlainText()
            if current_text:
                # 移除所有格式代码
                clean_text = ""
                skip_next = False
                for char in current_text:
                    if skip_next:
                        skip_next = False
                        continue
                    if char == "§":
                        skip_next = True
                        continue
                    clean_text += char
                
                # 应用默认格式
                edit_widget.setPlainText(default_format + clean_text)
                
                # 更新格式化代码
                self.format_codes[item_name] = default_format + clean_text
            
    def apply_formatting(self, format_code, edit_widget, item_name):
        """
    应用文本格式化代码到选中的文本，并在界面上显示实际颜色效果
    """
        # 获取QTextEdit的光标
        cursor = edit_widget.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            # 保留原始格式化代码
            original_text = self.format_codes.get(item_name, "")
            cursor_pos = cursor.position()
            anchor_pos = cursor.anchor()
            start = min(cursor_pos, anchor_pos)
            end = max(cursor_pos, anchor_pos)
            
            # 提取纯文本内容（不包含格式代码）
            plain_text = ""
            skip_next = False
            for char in original_text:
                if skip_next:
                    skip_next = False
                    continue
                if char == "§":
                    skip_next = True
                    continue
                plain_text += char
            
            # 判断是颜色代码还是格式代码
            color_codes = set(self.COLOR_CODES.values())
            format_codes = set(self.FORMAT_CODES.values()) - {"§r"}  # 排除重置代码
            
            # 判断是否选择了整个字符串
            is_full_string = (start == 0 and end == len(plain_text))
            
            # 构建新的格式化文本
            new_formatted_text = ""
            
            # 计算选中的文本在原始格式化文本中的位置
            # 由于格式代码的存在，需要更精确地计算位置
            current_plain_pos = 0
            i = 0
            
            # 用于标记是否已经处理了选中区域
            processed_selection = False
            
            while i < len(original_text):
                if original_text[i] == "§" and i + 1 < len(original_text):
                    # 处理格式代码
                    new_formatted_text += original_text[i:i+2]
                    i += 2
                else:
                    # 处理普通字符
                    if current_plain_pos >= start and current_plain_pos < end:
                        if not processed_selection:
                            # 开始处理选中区域
                            if format_code in format_codes:
                                # 格式代码：在选中区域前面添加§r
                                new_formatted_text += "§r"
                            
                            # 添加新的格式代码和选中的文本
                            new_formatted_text += format_code
                            
                            # 找出选中区域在原始格式化文本中的实际位置
                            selection_start = i
                            selection_end = i + (end - start)
                            
                            # 复制选中的文本（包括其中的格式代码）
                            j = i
                            temp_plain_pos = current_plain_pos
                            while j < len(original_text) and temp_plain_pos < end:
                                if original_text[j] == "§" and j + 1 < len(original_text):
                                    new_formatted_text += original_text[j:j+2]
                                    j += 2
                                else:
                                    new_formatted_text += original_text[j]
                                    j += 1
                                    temp_plain_pos += 1
                            
                            # 根据代码类型添加重置代码
                            if format_code in format_codes:
                                # 格式代码：在选中区域末尾添加§r
                                new_formatted_text += "§r"
                            elif format_code in color_codes and not is_full_string:
                                # 颜色代码且不是选择整个字符串：仅在尾部添加一个§r
                                new_formatted_text += "§r"
                            
                            # 更新索引
                            i = j
                            current_plain_pos = temp_plain_pos
                            processed_selection = True
                    else:
                        # 处理非选中区域的字符
                        new_formatted_text += original_text[i]
                        i += 1
                        current_plain_pos += 1
            
            # 如果原始文本为空或无法正确处理，则使用简化的处理方式
            if not new_formatted_text or not processed_selection:
                # 根据代码类型添加重置代码
                if format_code in format_codes:
                    # 格式代码：在选中区域前后都添加§r
                    new_formatted_text = original_text[:start] + "§r" + format_code + selected_text + "§r" + original_text[end:]
                elif format_code in color_codes and not is_full_string:
                    # 颜色代码且不是选择整个字符串：仅在尾部添加一个§r
                    new_formatted_text = original_text[:start] + format_code + selected_text + "§r" + original_text[end:]
                else:
                    # 其他情况：正常添加格式代码
                    new_formatted_text = original_text[:start] + format_code + selected_text + original_text[end:]
            
            self.format_codes[item_name] = new_formatted_text
            
            # 应用富文本格式到QTextEdit
            self.apply_rich_text_formatting(format_code, edit_widget)
    
    def apply_rich_text_formatting(self, format_code, edit_widget):
        """
    将格式化代码转换为实际的富文本格式应用到QTextEdit
    """
        cursor = edit_widget.textCursor()
        
        # 创建文本格式
        char_format = QTextCharFormat()
        
        # 应用颜色
        if format_code in self.CODE_TO_COLOR:
            char_format.setForeground(QBrush(QColor(self.CODE_TO_COLOR[format_code])))
        
        # 应用格式
        if format_code == "§l":  # 粗体
            char_format.setFontWeight(QFont.Bold)
        elif format_code == "§o":  # 斜体
            char_format.setFontItalic(True)
        elif format_code == "§n":  # 下划线
            char_format.setFontUnderline(True)
        elif format_code == "§m":  # 删除线
            char_format.setFontStrikeOut(True)
        elif format_code == "§r":  # 重置
            char_format = QTextCharFormat()  # 使用默认格式
        
        # 应用格式到选中的文本
        cursor.mergeCharFormat(char_format)
        edit_widget.setTextCursor(cursor)
            
    def update_format_codes(self, edit_widget, item_name):
        """
    当文本变化时，更新格式化代码存储
    """
        # 获取QTextEdit的纯文本
        plain_text = edit_widget.toPlainText()
        
        # 检查是否已有格式化代码存储
        if item_name in self.format_codes:
            stored_text = self.format_codes[item_name]
            
            # 如果存储的文本包含格式化代码
            has_color_codes = any(code in stored_text for code in self.COLOR_CODES.values())
            has_format_codes = any(code in stored_text for code in self.FORMAT_CODES.values())
            
            if has_color_codes or has_format_codes: 
                # 从存储的文本中提取纯文本（不包含格式代码）
                plain_stored_text = ""
                skip_next = False
                for char in stored_text:
                    if skip_next:
                        skip_next = False
                        continue
                    if char == "§":
                        skip_next = True
                        continue
                    plain_stored_text += char
                
                # 如果纯文本内容相同，仅保留存储的格式化代码文本
                if plain_stored_text.strip() == plain_text.strip():
                    # 内容没有变化，保留格式化代码
                    return
                
                # 内容有变化，但我们仍尝试保留所有格式代码
                # 提取所有格式代码
                all_format_codes = []
                i = 0
                while i < len(stored_text):
                    if stored_text[i] == "§" and i + 1 < len(stored_text):
                        all_format_codes.append(stored_text[i:i+2])
                        i += 2
                    else:
                        i += 1
                
                # 创建新的格式化文本，将所有格式代码应用到新文本
                # 为了简化，我们将所有格式代码应用到整个文本
                if all_format_codes:
                    new_formatted_text = "".join(all_format_codes) + plain_text
                    self.format_codes[item_name] = new_formatted_text
                    return
        
        # 如果没有格式化代码或无法保留格式，则更新为纯文本
        self.format_codes[item_name] = plain_text
        
    def save_settings(self):
        """
    保存用户在自定义名字窗口中设置的选项
    """
        import json
        import os
        
        # 收集设置
        settings = {}
        custom_names = {}
        
        # 收集所有非空的自定义名称（使用存储的格式化代码）
        for original_name in self.name_mappings.keys():
            # 优先使用格式化代码文本
            custom_name = self.format_codes.get(original_name, "").strip()
            
            # 如果格式化代码文本为空，尝试从文本框获取
            if not custom_name:
                edit_widget = self.name_mappings[original_name]
                custom_name = edit_widget.toPlainText().strip()
                
            if custom_name:
                # 使用物品ID作为键保存自定义名称
                if original_name in self.item_id_map:
                    item_id = self.item_id_map[original_name]
                    custom_names[item_id] = custom_name
                else:
                    # 如果找不到对应的物品ID，使用原始名称（向后兼容）
                    custom_names[original_name] = custom_name
        
        # 如果有自定义名称，则添加到设置中
        if custom_names:
            settings["lang_itemname"] = custom_names
            
        # 保存选择的语言
        settings["selected_language"] = "zh_cn" if self.chinese_checkbox.isChecked() else "en_us"
        
        # 创建temp_overlay文件夹
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        os.makedirs(temp_overlay_dir, exist_ok=True)
        
        # 始终使用同一个固定位置的overlay.json文件
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 如果文件已存在，先读取现有内容
        if os.path.exists(overlay_file):
            try:
                with open(overlay_file, "r", encoding="utf-8-sig") as f:
                    existing_settings = json.load(f)
                # 合并新的自定义名称设置
                existing_settings.update(settings)
                settings = existing_settings
            except json.JSONDecodeError:
                # 如果文件格式错误，则创建新的设置对象
                existing_settings = {}
                settings = existing_settings
        
        # 写入文件
        with open(overlay_file, "w", encoding="utf-8-sig") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        
        # 提示保存成功
        ModernMessageBox.success(self, "保存成功", f"自定义名称设置已成功保存到 {overlay_file}")
        self.accept()

# 彩色圆盘选择器类
class ColorDisc(QPushButton):
    def __init__(self):
        super().__init__()
        self.setObjectName("colorDisc")
        self.setFixedSize(48, 48)
        # 美化样式，使用PyQt5兼容的样式
        self.setStyleSheet("""
            #colorDisc {
                border-radius: 24px;
                background-color: #f0f0f0;
                border: 2px solid #d0d0d0;
            }
            #colorDisc:hover {
                border-color: #0078d4;
                background-color: #f8f9fa;
            }
        """)
        self.current_color = "浅灰色"
        self.color_object = QColor(240, 240, 240)  # 存储实际的颜色对象，默认为浅灰色
        # 扩展颜色映射，增加更多常用颜色
        self.color_map = {
            "透明": "transparent",
            "白色": "#ffffff",
            "黑色": "#000000",
            "灰色": "#808080",
            "红色": "#ff0000",
            "绿色": "#00ff00",
            "蓝色": "#0000ff",
            "黄色": "#ffff00",
            "紫色": "#800080",
            "青色": "#00ffff",
            "橙色": "#ff8000"
        }
        self.clicked.connect(self.show_color_dialog)
        # 添加颜色名称标签
        self.color_label = QLabel(self.current_color, self)
        self.color_label.setStyleSheet("color: #333333; font-size: 8px; font-weight: bold;")
        self.color_label.setAlignment(Qt.AlignCenter)
        self.color_label.setGeometry(0, 30, 48, 15)
    
    def show_color_dialog(self):
        color_dialog = QColorDialog()
        color_dialog.setWindowTitle("选择背景颜色")
        
        # 设置预定义颜色为中文
        color_dialog.setCustomColor(0, QColor(255, 255, 255))  # 白色
        color_dialog.setCustomColor(1, QColor(0, 0, 0))       # 黑色
        color_dialog.setCustomColor(2, QColor(128, 128, 128)) # 灰色
        color_dialog.setCustomColor(3, QColor(255, 0, 0))     # 红色
        color_dialog.setCustomColor(4, QColor(0, 255, 0))     # 绿色
        color_dialog.setCustomColor(5, QColor(0, 0, 255))     # 蓝色
        color_dialog.setCustomColor(6, QColor(255, 255, 0))   # 黄色
        color_dialog.setCustomColor(7, QColor(255, 0, 255))   # 紫色
        color_dialog.setCustomColor(8, QColor(0, 255, 255))   # 青色
        color_dialog.setCustomColor(9, QColor(255, 128, 0))   # 橙色
        
        if color_dialog.exec_():
            color = color_dialog.currentColor()
            self.color_object = color  # 保存实际的颜色对象
            # 更新按钮背景色
            if color.alpha() == 0:
                self.current_color = "透明"
                self.setStyleSheet("""
                    #colorDisc {
                        border-radius: 24px;
                        background-color: transparent;
                        border: 2px dashed #e0e0e0;
                    }
                    #colorDisc:hover {
                        border-color: #0078d4;
                        background-color: #f8f9fa;
                    }
                """)
            else:
                # 检查是否是预定义颜色
                color_name = "自定义"
                for name, hex_color in self.color_map.items():
                    if name != "透明" and QColor(hex_color) == color:
                        color_name = name
                        break
                
                self.current_color = color_name
                style = "#colorDisc {{border-radius: 24px; background-color: {0}; border: 2px solid #e0e0e0;}} #colorDisc:hover {{border-color: #0078d4; background-color: #f8f9fa;}}"
                style = style.format(color.name())
                self.setStyleSheet(style)
            # 更新颜色标签文本
            self.color_label.setText(self.current_color)
    
    def get_rgba(self):
        """
    获取当前颜色的RGBA分量，每个分量的范围是0.0-1.0
    """
        if self.color_object.isValid():
            return {
                "r": self.color_object.redF(),   # 红色分量 (0.0-1.0)
                "g": self.color_object.greenF(), # 绿色分量 (0.0-1.0)
                "b": self.color_object.blueF(),  # 蓝色分量 (0.0-1.0)
                "a": self.color_object.alphaF()  # 透明度 (0.0-1.0)
            }
        else:
            # 如果颜色无效，返回默认的白色RGBA值
            return {
                "r": 1.0,
                "g": 1.0,
                "b": 1.0,
                "a": 1.0
            }

# 其他选项对话框
class OtherOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("其他选项")
        self.setFixedSize(500, 350)
        
        # 设置窗口图标（使用资源文件中的图标）
        self.setWindowIcon(QIcon(":/resource/icon.ico"))
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # 标题
        title = QLabel("其他渲染选项")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # 背包无阴影复选框
        self.no_shadow_checkbox = QCheckBox("背包无阴影")
        self.no_shadow_checkbox.setObjectName("dragDropLabel")
        main_layout.addWidget(self.no_shadow_checkbox)
        
        # 添加垂直间距使界面更美观
        main_layout.addSpacing(40)
        
        # 底部按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        
        save_button = QPushButton("保存")
        save_button.setObjectName("startConversionButton")
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("取消")
        cancel_button.setObjectName("startConversionButton")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        main_layout.addLayout(button_layout)
        
        # 尝试加载已保存的设置
        self.load_saved_settings()
        
    def load_saved_settings(self):
        import json
        import os
        
        # 始终使用同一个固定位置的overlay.json文件
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 如果文件不存在，不执行加载
        if not os.path.exists(overlay_file):
            return
        
        try:
            # 使用utf-8-sig编码读取文件，确保能正确解析BOM
            with open(overlay_file, "r", encoding="utf-8-sig") as f:
                settings = json.load(f)
            
            # 加载背包无阴影设置（支持旧格式'no_shadow'和新格式'core_shadow'）
            if "core_shadow" in settings:
                # 不需要取反，直接设置
                self.no_shadow_checkbox.setChecked(settings["core_shadow"].get("enabled", False))
            elif "no_shadow" in settings:
                # 向后兼容旧格式
                self.no_shadow_checkbox.setChecked(settings["no_shadow"].get("enabled", False))
        except Exception as e:
            ModernMessageBox.warning(self, "加载失败", f"加载设置时出错: {str(e)}")
        
    def save_settings(self):
        """
    保存用户在其他选项窗口中设置的选项
    """
        import json
        import os
        import datetime
        
        # 收集设置
        settings = {}
        
        # 背包无阴影设置
        settings["core_shadow"] = {
            "enabled": self.no_shadow_checkbox.isChecked()  # 不需要取反，勾选表示需要启用无阴影功能
        }
        
        # 创建temp_overlay文件夹
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        os.makedirs(temp_overlay_dir, exist_ok=True)
        
        # 始终使用同一个固定位置的overlay.json文件
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 如果文件已存在，先读取现有内容
        if os.path.exists(overlay_file):
            try:
                with open(overlay_file, "r", encoding="utf-8-sig") as f:
                    existing_settings = json.load(f)
                # 合并新的设置
                existing_settings.update(settings)
                settings = existing_settings
            except json.JSONDecodeError:
                # 如果文件格式错误，则创建新的设置对象
                existing_settings = {}
                settings = existing_settings
        
        # 写入文件
        with open(overlay_file, "w", encoding="utf-8-sig") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        
        # 提示保存成功
        ModernMessageBox.success(self, "保存成功", f"其他选项已成功保存到 {overlay_file}")
        
        # 关闭对话框
        self.accept()

# 自定义物品边框颜色对话框
class BorderColorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("自定义物品边框")
        self.setFixedSize(600, 300)
        
        # 设置窗口图标（使用资源文件中的图标）
        self.setWindowIcon(QIcon(":/resource/icon.ico"))
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # 标题
        title = QLabel("设置方块边框")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # 说明文字
        notice_label = QLabel("因为一些不知名的问题，边框颜色暂时无法使用，请等待后续开发完善")
        notice_label.setObjectName("dragDropLabel")
        notice_label.setAlignment(Qt.AlignCenter)
        notice_label.setWordWrap(True)
        main_layout.addWidget(notice_label)
        
        # 炫彩边框复选框
        self.rgb_border_checkbox = QCheckBox("炫彩边框（需显卡支持）")
        self.rgb_border_checkbox.setObjectName("dragDropLabel")
        main_layout.addWidget(self.rgb_border_checkbox, alignment=Qt.AlignCenter)
        
        # 底部按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        
        save_button = QPushButton("保存")
        save_button.setObjectName("startConversionButton")
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("取消")
        cancel_button.setObjectName("startConversionButton")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        main_layout.addLayout(button_layout)
        
        # 加载已保存的设置
        self.load_saved_settings()
        
    # toggle_color_disc方法已移除，因为不再需要颜色选择器
        
    def load_saved_settings(self):
        """
    加载已保存的设置
    """
        import json
        import os
        
        # 从固定位置的overlay.json文件中加载设置
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        if os.path.exists(overlay_file):
            try:
                # 使用utf-8-sig编码读取，以支持带BOM的UTF-8文件
                with open(overlay_file, "r", encoding="utf-8-sig") as f:
                    settings = json.load(f)
                
                # 加载边框设置（支持新格式'core_outline'和'core_outline_rainbow'）
                if "core_outline_rainbow" in settings and settings["core_outline_rainbow"].get("enabled", False):
                    # 炫彩边框已启用
                    self.rgb_border_checkbox.setChecked(True)
                elif "core_outline" in settings and settings["core_outline"].get("enabled", False):
                    # 自定义颜色边框已启用 - 但我们只保留炫彩边框选项
                    self.rgb_border_checkbox.setChecked(False)
                elif "item_border" in settings:
                    # 向后兼容旧格式
                    border_settings = settings["item_border"]
                    # 检查是否选择了炫彩边框
                    if border_settings.get("type") == "rgb_border":
                        self.rgb_border_checkbox.setChecked(True)
                    else:
                        self.rgb_border_checkbox.setChecked(False)
            except Exception as e:
                print(f"加载边框设置失败: {e}")
    
    def save_settings(self):
        """
    保存用户在自定义物品边框窗口中设置的选项
    """
        import json
        import os
        
        # 收集设置
        settings = {}
        
        # 使用默认边框粗细值1
        thickness = 1
        
        # 检查是否选择了炫彩边框
        if self.rgb_border_checkbox.isChecked():
            # 炫彩边框设置为core_outline_rainbow
            settings["core_outline_rainbow"] = {
                "type": "rgb_border",
                "enabled": True,
                "name": "Rainbow Border",
                "description": "Enable GPU-accelerated colorful gradient border",
                "thickness": thickness
            }
            # 确保自定义颜色边框被禁用
            settings["core_outline"] = {
                "enabled": False
            }
        else:
            # 未选择炫彩边框时，禁用所有边框
            settings["core_outline"] = {
                "enabled": False
            }
            settings["core_outline_rainbow"] = {
                "enabled": False
            }
        
        # 创建temp_overlay文件夹
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        os.makedirs(temp_overlay_dir, exist_ok=True)
        
        # 始终使用同一个固定位置的overlay.json文件
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 如果文件已存在，先读取现有内容
        if os.path.exists(overlay_file):
            try:
                with open(overlay_file, "r", encoding="utf-8-sig") as f:
                    existing_settings = json.load(f)
                # 合并新的边框设置
                existing_settings.update(settings)
                settings = existing_settings
            except json.JSONDecodeError:
                # 如果文件格式错误，则创建新的设置对象
                existing_settings = {}
                settings = existing_settings
        
        # 写入文件
        with open(overlay_file, "w", encoding="utf-8-sig") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        
        # 提示保存成功
        ModernMessageBox.success(self, "保存成功", f"边框设置已成功保存到 {overlay_file}")
        
        # 关闭对话框
        self.accept()

class KPTMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("KyanitePackTool")
        self.setGeometry(100, 100, 1000, 600)
        
        # 设置窗口图标（使用资源文件中的图标）
        self.setWindowIcon(QIcon(":/resource/icon.ico"))
        
        # 设置窗口最小/最大尺寸，确保尺寸转换稳定性
        self.setMinimumSize(900, 500)  # 设置最小尺寸，防止窗口过小
        self.setMaximumSize(1200, 900)  # 增加最大高度，以容纳覆盖包页面的完整内容
        
        # 使窗口居中显示
        self.center_window()
        
        # 设置窗口尺寸策略，水平方向固定，垂直方向允许自由调整以完整显示所有内容
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        
        # 设置全局字体支持中文
        font = QFont("Microsoft YaHei", 10)
        self.setFont(font)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 设置样式
        self.setup_styles()
        
        # 初始化后延迟加载已保存的主题色
        from PyQt5.QtCore import QTimer
        # 移除主题色功能
        
        # 中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建内容区域容器，用于页面切换
        self.content_area = QWidget()
        self.content_area_layout = QVBoxLayout(self.content_area)
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area_layout.setSpacing(0)
        main_layout.addWidget(self.content_area)
        
        # 底部功能区域 - 独立于内容区域，不会在页面切换时被删除
        bottom_frame = QWidget()
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setSpacing(20)
        bottom_layout.setContentsMargins(40, 20, 40, 40)  # 左右边距40，上下边距20和40
        
        # 材质包转换按钮
        self.convert_button = QPushButton("材质包版本转换")
        self.convert_button.setObjectName("functionButton")
        self.convert_button.setFixedHeight(60)
        bottom_layout.addWidget(self.convert_button)
        
        # 覆盖包制作按钮
        self.overlay_button = QPushButton("覆盖包制作")
        self.overlay_button.setObjectName("functionButton")
        self.overlay_button.setFixedHeight(60)
        bottom_layout.addWidget(self.overlay_button)
        
        # 设置按钮
        self.settings_button = QPushButton("设置")
        self.settings_button.setObjectName("functionButton")
        self.settings_button.setFixedHeight(60)
        bottom_layout.addWidget(self.settings_button)
        
        # 主页按钮
        self.home_button = QPushButton("主页")
        self.home_button.setObjectName("homeButton")
        self.home_button.setFixedHeight(60)
        bottom_layout.addWidget(self.home_button)
        
        main_layout.addWidget(bottom_frame)
        
        # 连接按钮信号
        self.convert_button.clicked.connect(self.open_conversion_page)
        self.overlay_button.clicked.connect(self.open_overlay_page)
        self.settings_button.clicked.connect(self.open_settings_page)
        self.home_button.clicked.connect(self.show_home_page)
        
        # 初始显示主页
        self.start_application()
    
    def center_window(self):
        # 获取屏幕几何信息
        screen_geometry = QApplication.desktop().screenGeometry()
        # 获取窗口几何信息
        window_geometry = self.frameGeometry()
        # 计算窗口居中位置
        window_geometry.moveCenter(screen_geometry.center())
        # 设置窗口位置
        self.move(window_geometry.topLeft())
        
    def create_menu_bar(self):
        """
    创建菜单栏
    """
    
    # 登录对话框功能已移除
    
    # 注册对话框功能已移除
    
    def show_about_dialog(self):
        """
    显示关于对话框
    """
        ModernMessageBox.info(self, '关于KyanitePackTool', \
                            'KyanitePackTool v0.0.2\n\n' \
                            '一个强大的材质包转换工具，支持多版本转换和覆盖包制作。\n\n' \
                            '© 2024 KyanitePackTool团队')
    
    # 用户状态更新功能已移除
    
    def setup_styles(self):
        # 设置应用程序的样式表
        style_sheet = """
/* 全局字体设置 */
* {
    font-family: 'Microsoft YaHei', sans-serif;
}

/* 主窗口背景 */
QMainWindow {
    background-color: #f0f0f0;
}

/* 主内容区域 */
#mainContent {
    background-color: #f0f0f0;
}

/* 欢迎区域 */
#welcomeFrame {
    background-color: white;
    border-radius: 10px;
    border: 1px solid #ddd;
}

/* 欢迎标题 */
#welcomeTitle {
    color: #333;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: center;
}

/* 副标题 */
#subtitleLabel {
    color: #555;
    font-size: 18px;
    font-weight: bold;
    line-height: 1.5;
    margin-bottom: 10px;
    max-width: 600px;
    text-align: center;
}



/* 功能按钮 */
#functionButton {
    background-color: white;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 500;
}

#functionButton:hover {
    background-color: #f5f5f5;
    border-color: #0078d4;
}

#functionButton:pressed {
    background-color: #e0e0e0;
}

#functionButton:checked {
    border-color: #0078d4;
    border-width: 2px;
}

/* 主页按钮 */
#homeButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 500;
}

#homeButton:hover {
    background-color: #106ebe;
}

#homeButton:pressed {
    background-color: #005a9e;
}

/* 转换页面样式 */
#conversionFrame {
    background-color: white;
    border-radius: 10px;
    border: 1px solid #ddd;
    padding: 30px;
}

/* 拖拽框样式 */
#dragDropFrame {
    background-color: #f5f5f5;
    border: 2px dashed #0078d4;
    border-radius: 10px;
    padding: 40px;
    text-align: center;
}

#dragDropFrame:hover {
    background-color: #e8f0fe;
}

#dragDropLabel {
    color: #666;
    font-size: 16px;
    font-weight: 500;
    line-height: 1.5;
    text-align: center;
}

/* 选择文件按钮 */
#selectFileButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 15px 30px;
    font-size: 16px;
    min-width: 200px;
    height: 60px;
}

#selectFileButton:hover {
    background-color: #106ebe;
}

/* 选择文件夹按钮 */
#selectFolderButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 15px 30px;
    font-size: 16px;
    min-width: 200px;
    height: 60px;
}

#selectFolderButton:hover {
    background-color: #106ebe;
}

/* 版本选择下拉框 */
#versionComboBox {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 16px;
    font-weight: 500;
    background-color: white;
    color: #333;
    min-width: 150px;
    height: 40px;
}

#versionComboBox:hover {
    border-color: #0078d4;
    background-color: #f8f9fa;
}

#versionComboBox:focus {
    border-color: #0078d4;
    outline: none;
    box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.1);
}

#versionComboBox QAbstractItemView {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: white;
    padding: 5px;
}

#versionComboBox QAbstractItemView::item {
    padding: 12px 16px;
    font-size: 14px;
    color: #333;
}

#versionComboBox QAbstractItemView::item:hover {
    background-color: #e8f0fe;
    color: #0078d4;
}

#versionComboBox QAbstractItemView::item:selected {
    background-color: #0078d4;
    color: white;
}

/* 进度条样式 */
QProgressBar {
    border: 1px solid #ddd;
    border-radius: 5px;
    text-align: center;
    background-color: #f0f0f0;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 4px;
}

/* 开始转换按钮 */
#startConversionButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    padding: 12px 24px;
}

#startConversionButton:hover {
    background-color: #106ebe;
}

#startConversionButton:pressed {
    background-color: #005a9e;
}

#startConversionButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

/* 选项按钮样式 */
#optionButton {
    background-color: white;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 500;
}

#optionButton:hover {
    background-color: #f5f5f5;
    border-color: #0078d4;
}

#optionButton:pressed {
    background-color: #e0e0e0;
}
        """
        
        self.setStyleSheet(style_sheet)
    

    
    def start_application(self):
        # 应用启动时显示主页
        home_page = self.create_home_page()
        self.content_area_layout.addWidget(home_page)
        
    def switch_page(self, new_page_creator, button_states):
        # 简单的页面切换方法，不使用动画
        # 移除内容区域中的当前页面
        for i in reversed(range(self.content_area_layout.count())):
            self.content_area_layout.itemAt(i).widget().setParent(None)
        
        # 创建新页面
        new_page = new_page_creator()
        
        # 添加新页面到内容区域
        self.content_area_layout.addWidget(new_page)
        
        # 更新按钮状态
        if button_states:
            for button, state in button_states.items():
                button.setCheckable(True)
                button.setChecked(state)
                # 设置按钮的选中状态，QSS中已定义选中状态的样式（蓝色边框）
                # 不需要手动设置样式表，避免覆盖原有样式定义
    
    def create_home_page(self):
        # 创建主页内容
        main_content = QWidget()
        main_content.setObjectName("mainContent")
        content_layout = QVBoxLayout(main_content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)  # 减小间距
        
        # 欢迎区域
        welcome_frame = QFrame()
        welcome_frame.setObjectName("welcomeFrame")
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setAlignment(Qt.AlignCenter)
        welcome_layout.setContentsMargins(30, 30, 30, 30)  # 减小边距
        
        # 欢迎标题
        welcome_title = QLabel("WELCOME")
        welcome_title.setObjectName("welcomeTitle")
        welcome_title.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_title)
        
        # 合并的副标题
        subtitle_label = QLabel("KyanitePackTool，自由地转换多个版本的材质包，快速，便捷")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        welcome_layout.addWidget(subtitle_label)
        
        content_layout.addWidget(welcome_frame)
        
        # 创建按钮容器
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(20)
        
        # 底部功能区域
        bottom_frame = QWidget()
        # 不要在页面方法中重复添加底部按钮，按钮已经在主窗口初始化时添加
        
        return main_content
    
    def show_home_page(self):
        # 显示主页，保持当前位置，设置尺寸为1000x600
        current_geometry = self.geometry()
        self.setGeometry(current_geometry.x(), current_geometry.y(), 1000, 600)
        
        # 切换页面
        button_states = {
            self.convert_button: False,
            self.overlay_button: False,
            self.home_button: True
        }
        self.switch_page(self.create_home_page, button_states)
    
    def open_conversion_page(self):
        # 打开材质包转换页面，保持当前位置，增加高度以完全显示所有内容
        current_geometry = self.geometry()
        self.setGeometry(current_geometry.x(), current_geometry.y(), 1000, 900)
        
        # 切换页面
        button_states = {
            self.convert_button: True,
            self.overlay_button: False,
            self.settings_button: False,
            self.home_button: False
        }
        self.switch_page(self.create_conversion_page, button_states)
    
    def create_overlay_page(self):
        # 创建覆盖包制作页面
        overlay_page = QWidget()
        overlay_layout = QVBoxLayout(overlay_page)
        overlay_layout.setContentsMargins(40, 40, 40, 40)
        overlay_layout.setSpacing(20)
        
        # 页面标题
        title = QLabel("覆盖包制作")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        overlay_layout.addWidget(title)
        
        # 主框架
        main_frame = QFrame()
        main_frame.setObjectName("conversionFrame")
        main_frame_layout = QVBoxLayout(main_frame)
        main_frame_layout.setSpacing(25)
        
        # 1. 母材质包选择（最大的控件，可选）
        parent_pack_frame = QFrame()
        parent_pack_frame.setObjectName("dragDropFrame")
        parent_pack_frame.setMinimumHeight(200)
        
        parent_pack_layout = QVBoxLayout(parent_pack_frame)
        parent_pack_layout.setAlignment(Qt.AlignCenter)
        
        parent_pack_label = QLabel("母材质包 (可选)")
        parent_pack_label.setObjectName("dragDropLabel")
        parent_pack_label.setAlignment(Qt.AlignCenter)
        
        self.parent_pack_button = QPushButton("选择母材质包文件")
        self.parent_pack_button.setObjectName("selectFileButton")
        self.parent_pack_button.clicked.connect(self.select_parent_pack)
        
        self.parent_pack_file_label = QLabel("（如果不选择，将使用默认设置）")
        self.parent_pack_file_label.setObjectName("dragDropLabel")
        self.parent_pack_file_label.setAlignment(Qt.AlignCenter)
        self.parent_pack_file_label.setWordWrap(True)
        
        parent_pack_layout.addWidget(parent_pack_label)
        parent_pack_layout.addWidget(self.parent_pack_button)
        parent_pack_layout.addWidget(self.parent_pack_file_label)
        
        # 创建自定义设置面板
        self.custom_settings_panel = QFrame()
        self.custom_settings_panel_layout = QVBoxLayout(self.custom_settings_panel)
        self.custom_settings_panel.setVisible(False)  # 默认隐藏
        
       
        # 自定义物品边框下拉框
        self.border_combo = QComboBox()
        self.border_combo.setObjectName("versionComboBox")
        borders = ["无", "细边框", "粗边框", "虚线边框", "自定义..."]
        self.border_combo.addItems(borders)
        self.custom_settings_panel_layout.addWidget(QLabel("自定义物品边框："))
        self.custom_settings_panel_layout.addWidget(self.border_combo)
        
        # 三个自定义按钮（自定义名字、自定义物品大小、自定义物品边框）- 去掉边框，改为水平排列
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(20)
        
        # 自定义名字按钮
        self.name_button = QPushButton("自定义名字")
        self.name_button.setObjectName("optionButton")
        self.name_button.setFixedHeight(50)
        
        # 自定义物品大小按钮
        self.size_button = QPushButton("自定义物品大小")
        self.size_button.setObjectName("optionButton")
        self.size_button.setFixedHeight(50)
        
        # 自定义物品边框按钮
        self.border_button = QPushButton("自定义物品边框")
        self.border_button.setObjectName("optionButton")
        self.border_button.setFixedHeight(50)
        
        # 其他选项按钮
        self.other_options_button = QPushButton("其他选项")
        self.other_options_button.setObjectName("optionButton")
        self.other_options_button.setFixedHeight(50)
        
        buttons_layout.addWidget(self.name_button)
        buttons_layout.addWidget(self.size_button)
        buttons_layout.addWidget(self.border_button)
        buttons_layout.addWidget(self.other_options_button)
        
        # 连接按钮点击事件
        self.name_button.clicked.connect(self.open_custom_name_dialog)
        self.size_button.clicked.connect(self.open_item_size_dialog)
        self.border_button.clicked.connect(self.open_border_color_dialog)
        self.other_options_button.clicked.connect(self.open_other_options_dialog)
        
        # 生成覆盖包按钮
        self.generate_overlay_button = QPushButton("生成覆盖包")
        self.generate_overlay_button.setObjectName("startConversionButton")
        self.generate_overlay_button.setFixedHeight(60)
        self.generate_overlay_button.clicked.connect(self.generate_overlay_pack)
        
        # 添加所有组件到框架
        main_frame_layout.addWidget(parent_pack_frame)
        main_frame_layout.addWidget(buttons_frame)  # 三个自定义按钮：自定义名字、自定义物品大小、自定义物品边框
        # 添加垂直间隔，使页面更宽敞
        main_frame_layout.addSpacing(40)
        main_frame_layout.addWidget(self.generate_overlay_button, alignment=Qt.AlignCenter)
        
        # 添加框架到页面
        overlay_layout.addWidget(main_frame)
        
        return overlay_page
    
    def toggle_setting(self, widget):
        """
    切换设置项的显示状态
    """
        if widget.isVisible():
            widget.hide()
        else:
            widget.show()
            
    def open_item_size_dialog(self):
        """
    打开自定义物品大小对话框
    """
        # 创建并显示物品大小对话框
        self.item_size_dialog = ItemSizeDialog(self)
        # 居中显示对话框
        self.item_size_dialog.setGeometry(
            self.x() + (self.width() - self.item_size_dialog.width()) // 2,
            self.y() + (self.height() - self.item_size_dialog.height()) // 2,
            self.item_size_dialog.width(),
            self.item_size_dialog.height()
        )
        self.item_size_dialog.show()
        
    def open_border_color_dialog(self):
        """
    打开自定义物品边框对话框
    """
        # 创建并显示边框颜色对话框
        self.border_color_dialog = BorderColorDialog(self)
        # 居中显示对话框
        self.border_color_dialog.setGeometry(
            self.x() + (self.width() - self.border_color_dialog.width()) // 2,
            self.y() + (self.height() - self.border_color_dialog.height()) // 2,
            self.border_color_dialog.width(),
            self.border_color_dialog.height()
        )
        self.border_color_dialog.show()
        
    def open_other_options_dialog(self):
        """
    打开其他选项对话框
    """
        # 创建并显示其他选项对话框
        self.other_options_dialog = OtherOptionsDialog(self)
        # 居中显示对话框
        self.other_options_dialog.setGeometry(
            self.x() + (self.width() - self.other_options_dialog.width()) // 2,
            self.y() + (self.height() - self.other_options_dialog.height()) // 2,
            self.other_options_dialog.width(),
            self.other_options_dialog.height()
        )
        self.other_options_dialog.show()
        
    def open_custom_name_dialog(self):
        """
    打开自定义物品名称对话框
    """
        # 创建并显示自定义名称对话框
        self.custom_name_dialog = CustomNameDialog(self)
        # 居中显示对话框
        self.custom_name_dialog.setGeometry(
            self.x() + (self.width() - self.custom_name_dialog.width()) // 2,
            self.y() + (self.height() - self.custom_name_dialog.height()) // 2,
            self.custom_name_dialog.width(),
            self.custom_name_dialog.height()
        )
        self.custom_name_dialog.show()
            
    def open_overlay_page(self):
        import json
        import os
        
        # 打开覆盖包制作页面，保持当前位置，进一步增加高度以完全显示所有内容
        current_geometry = self.geometry()
        self.setGeometry(current_geometry.x(), current_geometry.y(), 1200, 1200)
        
        # 清空overlay.json文件内容
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 如果文件存在，清空其内容
        if os.path.exists(overlay_file):
            try:
                # 清空文件内容，但保留空对象
                with open(overlay_file, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"清空overlay.json文件失败：{str(e)}")
        
        # 切换页面 - 只将当前页面按钮设置为选中状态
        button_states = {
            self.convert_button: False,
            self.overlay_button: True,
            self.home_button: False
        }
        self.switch_page(self.create_overlay_page, button_states)
    
    def create_settings_page(self):
        # 创建设置页面，包含滚动功能
        settings_page = QWidget()
        settings_main_layout = QVBoxLayout(settings_page)
        settings_main_layout.setContentsMargins(0, 0, 0, 0)
        settings_main_layout.setSpacing(0)
        
        # 创建标题区域 - 更现代的设计
        title_frame = QFrame()
        title_frame.setObjectName("welcomeFrame")
        title_frame.setStyleSheet("""
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            border-bottom: 1px solid #ddd;
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(40, 20, 40, 15)
        title_layout.setSpacing(8)
        
        # 软件名称 - 使用渐变背景使其更突出
        app_name_label = QLabel("KyanitePackTool")
        app_name_label.setObjectName("welcomeTitle")
        app_name_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(app_name_label)
        
        settings_main_layout.addWidget(title_frame)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { background-color: #f0f0f0; }")
        
        # 创建滚动内容容器
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(40, 20, 40, 30)
        scroll_layout.setSpacing(20)
        
        # 主题色功能已移除
        
        # 添加用户设置区域 - 使用现代化卡片设计
        user_group = QFrame()
        user_group.setObjectName("welcomeFrame")
        user_group.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        """)
        user_layout = QVBoxLayout(user_group)
        user_layout.setContentsMargins(20, 10, 20, 15)
        user_layout.setSpacing(15)
        
        # 用户设置标题
        user_title = QLabel("用户设置")
        user_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        user_layout.addWidget(user_title)
        
        # 显示欢迎信息
        user_status_frame = QFrame()
        user_status_layout = QVBoxLayout(user_status_frame)
        user_status_layout.setContentsMargins(10, 0, 10, 10)
        
        user_status_label = QLabel("欢迎使用资源包转换工具")
        user_status_label.setStyleSheet("font-size: 16px; color: #333;")
        user_status_label.setAlignment(Qt.AlignCenter)
        user_status_layout.addWidget(user_status_label)
        
        user_layout.addWidget(user_status_frame)
        
        # 创建空白布局以保持界面一致性
        auth_button_layout = QHBoxLayout()
        auth_button_layout.setSpacing(20)
        auth_button_layout.setAlignment(Qt.AlignCenter)
        
        # 添加占位符
        spacer = QWidget()
        spacer.setFixedSize(260, 44)  # 与原来的两个按钮宽度相当
        auth_button_layout.addWidget(spacer)
        
        user_layout.addLayout(auth_button_layout)
        scroll_layout.addWidget(user_group)
        
        # 添加版本信息区域 - 使用现代化卡片设计
        version_group = QFrame()
        version_group.setObjectName("welcomeFrame")
        version_group.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        """)
        version_layout = QVBoxLayout(version_group)
        version_layout.setContentsMargins(20, 10, 20, 15)
        version_layout.setSpacing(15)
        
        # 版本信息标题
        version_title = QLabel("关于软件")
        version_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        version_layout.addWidget(version_title)
        
        # 显示当前版本 - 改进样式
        current_version = self.read_app_version()
        version_info_frame = QFrame()
        version_info_layout = QVBoxLayout(version_info_frame)
        version_info_layout.setContentsMargins(10, 0, 10, 10)
        
        version_label = QLabel(f"当前版本：{current_version}")
        version_label.setStyleSheet("font-size: 18px; color: #333; font-weight: bold;")
        version_info_layout.addWidget(version_label, alignment=Qt.AlignCenter)
        
        version_layout.addWidget(version_info_frame)
        
        # 联系方式已移至单独的卡片区域
        
        # 添加版权信息
        copyright_label = QLabel("©2025 KyanitePackStudio 保留所有权利")
        copyright_label.setStyleSheet("color: #666; font-size: 16px; font-weight: bold;")
        copyright_label.setAlignment(Qt.AlignCenter)
        version_layout.addWidget(copyright_label, alignment=Qt.AlignBottom | Qt.AlignCenter)
        
        scroll_layout.addWidget(version_group)
        
        # 创建单独的联系方式卡片
        contact_group = QFrame()
        contact_group.setObjectName("welcomeFrame")
        contact_group.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        """)
        contact_layout_main = QVBoxLayout(contact_group)
        contact_layout_main.setContentsMargins(20, 10, 20, 15)
        contact_layout_main.setSpacing(15)
        
        # 联系方式标题
        contact_title = QLabel("联系方式")
        contact_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        contact_layout_main.addWidget(contact_title)
        
        # 联系方式图标按钮布局
        contact_layout = QHBoxLayout()
        contact_layout.setSpacing(20)
        contact_layout.setAlignment(Qt.AlignCenter)
        
        # 创建各平台图标按钮（增大尺寸）
        platforms = ["bilibili", "youtube", "afdian", "email"]
        labels = ["B站", "YouTube", "爱发电", "邮箱"]
        colors = {"bilibili": "#FB7299", "youtube": "#FF0000", "afdian": "#FF6B6B", "email": "#4285F4"}
        
        for platform, label in zip(platforms, labels):
            button = QPushButton(label)
            button.setObjectName("functionButton")
            # 增大按钮尺寸到120x44
            button.setFixedSize(120, 44)
            # 使用字符串格式化设置按钮样式
            button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
                color: #333;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
            """ % colors[platform]
            button.setStyleSheet(button_style)
            button.clicked.connect(lambda checked, p=platform: self.show_contact_info(p))
            contact_layout.addWidget(button)
        
        contact_layout_main.addLayout(contact_layout)
        
        scroll_layout.addWidget(contact_group)
        

        
        # 添加一些空白区域使页面更美观
        scroll_layout.addStretch(1)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(scroll_content)
        
        # 添加滚动区域到主布局
        settings_main_layout.addWidget(scroll_area)
        
        return settings_page
        
    def read_app_version(self):
        # 直接返回硬编码的应用版本
        return "1.0.0"  # 当前应用版本
        

            

    
    def show_contact_info(self, platform):
        # 显示不同平台的联系方式
        contacts = {
            "bilibili": "B站主页：https://space.bilibili.com/3493094785812897",
            "youtube": "YouTube频道：https://www.youtube.com/@Unknown_JiaoLuo",
            "afdian": "爱发电支持：https://afdian.net/a/KyanitePack",
            "email": "邮箱联系：nufk_tlm@163.com"
        }
        
        if platform in contacts:
            ModernMessageBox.info(self, "联系方式", contacts[platform])
    
    def open_settings_page(self):
        # 打开设置页面，保持当前位置，设置尺寸为1000x600
        current_geometry = self.geometry()
        self.setGeometry(current_geometry.x(), current_geometry.y(), 1000, 600)
        
        # 切换页面
        button_states = {
            self.convert_button: False,
            self.overlay_button: False,
            self.settings_button: True,
            self.home_button: False
        }
        self.switch_page(self.create_settings_page, button_states)
    
    def create_conversion_page(self):
        # 创建转换页面
        conversion_page = QWidget()
        conversion_layout = QVBoxLayout(conversion_page)
        conversion_layout.setContentsMargins(40, 40, 40, 40)
        conversion_layout.setSpacing(20)
        
        # 页面标题
        title = QLabel("材质包版本转换")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        conversion_layout.addWidget(title)
        
        # 转换框架
        conversion_frame = QFrame()
        conversion_frame.setObjectName("conversionFrame")
        conversion_frame_layout = QVBoxLayout(conversion_frame)
        conversion_frame_layout.setSpacing(25)
        
        # 拖拽框
        drag_drop_frame = QFrame()
        drag_drop_frame.setObjectName("dragDropFrame")
        drag_drop_frame.setAcceptDrops(True)
        drag_drop_frame.setMinimumHeight(200)
        
        drag_drop_layout = QVBoxLayout(drag_drop_frame)
        drag_drop_layout.setAlignment(Qt.AlignCenter)
        
        # 按钮布局
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        self.select_file_button = QPushButton("选择材质包文件")
        self.select_file_button.setObjectName("selectFileButton")
        self.select_file_button.clicked.connect(self.select_resource_pack)
        
        self.select_folder_button = QPushButton("选择材质包文件夹")
        self.select_folder_button.setObjectName("selectFolderButton")
        self.select_folder_button.clicked.connect(self.select_resource_folder)
        
        buttons_layout.addWidget(self.select_file_button)
        buttons_layout.addWidget(self.select_folder_button)
        
        # 只添加按钮布局，不再显示选中的文件/文件夹路径
        drag_drop_layout.addLayout(buttons_layout)
        
        # 连接拖拽事件
        drag_drop_frame.dragEnterEvent = self.drag_enter_event
        drag_drop_frame.dropEvent = self.drop_event
        
        # 目标版本选择和转换进度
        version_layout = QHBoxLayout()
        version_label = QLabel("目标版本：")
        version_label.setObjectName("dragDropLabel")
        version_label.setMinimumWidth(80)
        
        self.version_combo_box = QComboBox()
        self.version_combo_box.setObjectName("versionComboBox")
        # 添加完整的Minecraft版本列表
        versions = [
            "1.6-1.8", "1.9-1.10", "1.11-1.12", "1.13-1.14", "1.15-1.16.1", "1.16.2-1.16.5",
            "1.17", "1.18", "1.19-1.19.2", "1.19.3", "1.19.4", "1.20-1.20.1",
            "1.20.2", "1.20.3-1.20.4", "1.20.5-1.20.6", "1.21-1.21.1",
            "1.21.2-1.21.3", "1.21.4", "1.21.5", "1.21.6", "1.21.7-1.21.8", 
            "1.21.9-1.21.10", "1.21.11"
        ]
        self.version_combo_box.addItems(versions)
        
        # 转换进度组件
        progress_label = QLabel("转换进度：")
        progress_label.setObjectName("dragDropLabel")
        progress_label.setMinimumWidth(80)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumWidth(200)
        
        self.progress_text = QLabel("准备就绪")
        self.progress_text.setObjectName("dragDropLabel")
        self.progress_text.setMaximumWidth(400)  
        
        # 将所有组件添加到水平布局
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_combo_box)
        version_layout.addSpacing(20)
        version_layout.addWidget(progress_label)
        version_layout.addWidget(self.progress_bar)
        version_layout.addWidget(self.progress_text)
        version_layout.addStretch()
        
        # 开始转换按钮
        self.start_conversion_button = QPushButton("开始转换")
        self.start_conversion_button.setObjectName("startConversionButton")
        self.start_conversion_button.setFixedHeight(60)
        self.start_conversion_button.clicked.connect(self.start_conversion)
        self.start_conversion_button.setEnabled(False)
        
        # 添加所有组件到框架
        conversion_frame_layout.addWidget(drag_drop_frame)
        conversion_frame_layout.addLayout(version_layout)
        conversion_frame_layout.addWidget(self.start_conversion_button, alignment=Qt.AlignCenter)
        
        # 添加框架到页面
        conversion_layout.addWidget(conversion_frame)
        
        # 添加底部按钮
        # 不要在页面方法中重复添加底部按钮，按钮已经在主窗口初始化时添加
        
        return conversion_page
    
    def select_resource_pack(self):
        # 打开文件选择对话框，支持多选
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择材质包", "", "压缩文件 (*.zip);;材质包 (*.mcpack);;所有文件 (*.*)"
        )
        
        if file_paths:
            self.selected_file_paths = file_paths  # 使用复数形式存储多个文件路径
            # 只显示文件名而不是完整路径
            if len(file_paths) == 1:
                file_name = os.path.basename(file_paths[0])
                self.select_file_button.setText(f"已选择：{file_name}")
            else:
                self.select_file_button.setText(f"已选择 {len(file_paths)} 个文件")
            
            # 重置文件夹按钮文本
            self.select_folder_button.setText("选择材质包文件夹")
            
            # 不再显示选中的文件列表
            self.start_conversion_button.setEnabled(True)
    
    def select_resource_folder(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择材质包文件夹", ""
        )
        
        if folder_path:
            # 将文件夹路径作为单个项目存储在selected_file_paths中
            self.selected_file_paths = [folder_path]
            
            # 显示选中的文件夹名称
            folder_name = os.path.basename(folder_path)
            self.select_folder_button.setText(f"已选择：{folder_name}")
            
            # 重置文件按钮文本
            self.select_file_button.setText("选择材质包文件")
            
        # 不再显示选中的文件夹路径
            self.start_conversion_button.setEnabled(True)
            
    def select_parent_pack(self):
        # 导入必要的模块
        import os
        import json
        import shutil
        
        # 打开文件选择对话框选择母材质包
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择母材质包", "", "压缩文件 (*.zip);;材质包 (*.mcpack);;所有文件 (*.*)"
        )
        
        if file_path:
            self.parent_pack_path = file_path
            # 只显示文件名而不是完整路径
            file_name = os.path.basename(file_path)
            self.parent_pack_button.setText(f"已选择：{file_name}")
            self.parent_pack_file_label.setText(f"当前选择：{file_name}")
            
            # 创建temp_overlay目录（如果不存在）
            temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
            os.makedirs(temp_overlay_dir, exist_ok=True)
            
            # 将母材质包复制到temp_overlay目录
            dest_path = os.path.join(temp_overlay_dir, file_name)
            try:
                shutil.copy2(file_path, dest_path)
                
                # 写入overlay.json文件
                overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
                settings = {}
                
                # 如果文件已存在，先读取现有内容
                if os.path.exists(overlay_file):
                    try:
                        with open(overlay_file, "r", encoding="utf-8-sig") as f:
                            settings = json.load(f)
                    except json.JSONDecodeError:
                        settings = {}
                
                # 添加母材质包信息到settings
                settings["parent_pack"] = {
                    "path": dest_path,
                    "filename": file_name,
                    "enabled": True
                }
                
                # 写入文件
                with open(overlay_file, "w", encoding="utf-8-sig") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=4)
                
            except Exception as e:
                ModernMessageBox.error(self, "错误", f"复制母材质包或写入overlay.json失败：{str(e)}")
    
    def generate_overlay_pack(self):
        import json
        import os
        import overlay  # 导入overlay模块
        
        # 检查temp_overlay目录和overlay.json文件是否存在
        temp_overlay_dir = os.path.join(os.getcwd(), "temp_overlay")
        overlay_file = os.path.join(temp_overlay_dir, "overlay.json")
        
        # 确保temp_overlay目录存在
        os.makedirs(temp_overlay_dir, exist_ok=True)
        
        # 检查是否存在已有设置
        settings_info = ""
        if os.path.exists(overlay_file):
            try:
                with open(overlay_file, "r", encoding="utf-8") as f:
                    settings_data = json.load(f)
                # 统计设置项数量
                settings_count = len(settings_data)
                settings_info = f"已加载 {settings_count} 项保存的设置\n\n"
                
                # 询问用户是否要清除之前的设置
                # 创建包含Yes/No/Cancel选项的确认对话框
                confirm_dialog = ModernMessageBox(
                    "确认操作",
                    f"检测到已保存的设置，是否清除之前的设置重新开始？\n\n" \
                    f"选择'是'：将清除所有已保存的设置，重新开始\n" \
                    f"选择'否'：将保留现有设置，继续使用\n" \
                    f"选择'取消'：取消当前操作",
                    self,
                    ModernMessageBox.QUESTION,
                    ModernMessageBox.YES_NO_CANCEL
                )
                reply = confirm_dialog.exec_()
                
                if reply is True:
                    # 清除现有设置
                    with open(overlay_file, "w", encoding="utf-8") as f:
                        json.dump({}, f, ensure_ascii=False, indent=4)
                    settings_info = "已清除之前的设置，重新开始\n\n"
                elif reply is None:
                    # 取消操作
                    return
                # else: 选择No，继续使用现有设置
            except Exception as e:
                settings_info = f"加载已有设置时出错：{str(e)}\n\n"
        
        # 准备显示信息
        overlay_name = "自定义覆盖包"
        has_custom_names = False
        has_size_settings = False
        
        # 检查是否有自定义名称设置
        if os.path.exists(overlay_file):
            try:
                with open(overlay_file, "r", encoding="utf-8") as f:
                    settings_data = json.load(f)
                # 检查是否有自定义名称设置
                if "custom_item_names" in settings_data:
                    has_custom_names = True
                # 检查是否有物品大小设置
                for key in settings_data:
                    if key not in ["custom_item_names", "background_color"]:
                        has_size_settings = True
                        break
            except:
                pass
        
        # 调用overlay模块中的start_overlay函数开始制作覆盖包
        try:
            overlay.start_overlay()
            
            # 封装覆盖包为资源包
            zip_file_path = overlay.package_overlay_resource_pack()
            
            if zip_file_path and os.path.exists(zip_file_path):
                # 让用户选择保存位置
                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "保存覆盖包",
                    os.path.basename(zip_file_path),
                    "ZIP文件 (*.zip)"
                )
                
                if save_path:
                    # 复制文件到用户选择的位置
                    shutil.copy2(zip_file_path, save_path)
                    
                    # 显示导出成功提示
                    ModernMessageBox.success(
                    self,
                    "导出成功",
                    f"覆盖包已成功导出到：\n{save_path}\n\n" \
                    "你可以将此ZIP文件添加到Minecraft的资源包文件夹中使用。"
                )
        except Exception as e:
            ModernMessageBox.error(
                self,
                "制作失败",
                f"覆盖包制作过程中出错：{str(e)}\n\n" \
                "请检查日志信息以获取详细错误。"
            )
    
    def drag_enter_event(self, event):
        # 处理拖拽进入事件
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def drop_event(self, event):
        # 处理拖拽释放事件，支持多个文件
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            self.selected_file_paths = file_paths  # 使用复数形式存储多个文件路径
            
            # 只显示文件名而不是完整路径
            if len(file_paths) == 1:
                file_name = os.path.basename(file_paths[0])
                self.select_file_button.setText(f"已选择：{file_name}")
            else:
                self.select_file_button.setText(f"已选择 {len(file_paths)} 个文件")
            
            self.start_conversion_button.setEnabled(True)
    
    def start_conversion(self):
        # 开始转换逻辑
        if hasattr(self, 'selected_file_paths'):
            target_version = self.version_combo_box.currentText()
            
            # 禁用开始转换按钮
            self.start_conversion_button.setEnabled(False)
            
            # 显示转换进度
            self.progress_text.setText(f"正在转换到版本 {target_version}...")
            
            # 创建转换线程来调用pack.py中的start_conversion函数
            from PyQt5.QtCore import QThread, pyqtSignal
            import os
            import sys
            
            class ConversionThread(QThread):
                # 定义信号
                progress_updated = pyqtSignal(int)
                conversion_completed = pyqtSignal(str)
                
                def __init__(self, file_paths, target_version):
                    super().__init__()
                    self.file_paths = file_paths
                    self.target_version = target_version
                
                def run(self):
                    # 为pack.py设置必要的环境
                    try:
                        # 导入pack模块
                        import pack
                           
                        # 创建一个简单的类来模拟tk.Variable类型的selected_files对象
                        class MockSelectedFiles:
                            def __init__(self, file_paths):
                                self.file_paths = file_paths
                            def get(self):
                                # 直接返回文件路径列表
                                return self.file_paths
                           
                        # 设置pack模块中的全局变量，传入已选择的文件路径
                        # 每次都更新，确保使用最新选择的文件
                        pack.selected_files = MockSelectedFiles(self.file_paths)
                        
                        # 为了防止pack.py中的初始化错误，设置必要的全局变量
                        if not hasattr(pack, 'frame'):
                            # 创建一个简单的模拟对象来替代UI框架
                            class MockFrame:
                                pass
                            pack.frame = MockFrame()
                            pack.root = None
                        
                        # 创建进度回调函数
                        def progress_callback(value):
                            # 确保进度值在0-100范围内
                            value = max(0, min(100, value))
                            # 发出进度更新信号
                            self.progress_updated.emit(value)
                        
                        # 初始进度
                        self.progress_updated.emit(0)
                        # 调用pack.py中的start_conversion函数并传入进度回调
                        pack.start_conversion(self.target_version, progress_callback)
                    except Exception as e:
                        # 捕获所有异常
                        error_message = f"转换过程中出错: {str(e)}"
                        print(error_message)
                        # 发出错误信号，不更新进度条到100%
                        self.conversion_completed.emit(f"ERROR:{error_message}")
                    else:
                        # 转换成功，更新进度条到100%
                        self.progress_updated.emit(100)
                        self.conversion_completed.emit(self.target_version)
            
            # 创建并启动线程
            self.conversion_thread = ConversionThread(self.selected_file_paths, target_version)
            # 连接信号和槽
            self.conversion_thread.progress_updated.connect(self.update_progress)
            self.conversion_thread.conversion_completed.connect(self.conversion_finished)
            # 启动线程
            self.conversion_thread.start()
            
    def update_progress(self, value):
        # 在主线程中更新进度条
        self.progress_bar.setValue(value)
        
    def reset_conversion_page(self):
        # 重置转换页面
        self.progress_bar.setValue(0)
        self.progress_text.setText("请选择材质包文件或文件夹")
        self.select_file_button.setText("选择材质包文件")
        self.select_folder_button.setText("选择材质包文件夹")
        # 不再需要重置selected_file_label，因为它不再被使用
        if hasattr(self, 'selected_file_paths'):
            delattr(self, 'selected_file_paths')
        self.start_conversion_button.setEnabled(False)
    
    def conversion_finished(self, result):
        # 初始化has_processed_files变量，避免作用域错误
        has_processed_files = False
        
        # 在主线程中处理转换完成
        if result.startswith("ERROR:"):
            # 转换失败
            error_message = result[6:]  # 去掉"ERROR:"前缀
            self.progress_text.setText("转换失败！")
            # 错误时不启用转换按钮，而是在重置页面时处理
            
            # 显示错误消息框
            message_box = ModernMessageBox(
                title="转换失败",
                message=f"无法完成材质包转换：\n{error_message}",
                parent=self,
                icon_type=ModernMessageBox.ERROR,
                button_type=ModernMessageBox.OK
            )
            # 连接信号，当消息框关闭时重置页面
            message_box.finished.connect(self.reset_conversion_page)
            # 使用show而不是exec_，允许非阻塞显示
            message_box.show()
        else:
            # 转换成功
            target_version = result
            self.progress_text.setText(f"转换完成！已成功转换到版本 {target_version}")
            self.start_conversion_button.setEnabled(True)
            
            # 导入pack模块，获取最后一次转换的文件路径
            import pack
            
            # 检查转换是否成功（是否有处理后的文件）
            has_processed_files = hasattr(pack, 'global_last_processed_files') and pack.global_last_processed_files
            
            if has_processed_files:
                # 播放转换成功的声音提示
                try:
                    import platform
                    system_type = platform.system()
                    
                    if system_type == 'Windows':
                        import winsound
                        # 使用Windows默认的声音
                        try:
                            winsound.MessageBeep(0x40)  # MB_ICONINFORMATION的数字代码
                        except Exception:
                            # 如果仍失败，使用简单的蜂鸣
                            winsound.Beep(1000, 200)
                    else:  # Linux和其他平台
                        # 在Linux上使用ASCII响铃字符
                        print('\a')  # ASCII响铃字符
                except Exception as e:
                    print(f"播放声音失败: {str(e)}")
            
            # 检查应用是否是焦点应用，如果不是则发送桌面通知
            is_active_window = self.isActiveWindow()
            if not is_active_window:
                try:
                    from plyer import notification
                    # 发送跨平台桌面通知
                    notification.notify(
                        title='材质包转换成功',
                        message=f'已成功转换到版本 {target_version}',
                        app_name='ResourcePackConverter',
                        timeout=10
                    )
                except Exception as e:
                    print(f"发送通知失败: {str(e)}")
        
        # 只有在转换成功时才显示成功窗口
        if has_processed_files:
            # 创建成功提示对话框
            success_dialog = QDialog(self)
            success_dialog.setWindowTitle("转换成功")
            success_dialog.setGeometry(300, 300, 500, 350)
            success_dialog.setWindowIcon(self.windowIcon())
            
            # 设置对话框样式
            success_dialog.setStyleSheet("""
                QDialog {
                    background-color: #f0f0f0;
                    border-radius: 5px;
                }
                QLabel {
                    color: #333333;
                    font-family: 'Microsoft YaHei';
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 20px;
                    font-family: 'Microsoft YaHei';
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton#closeButton {
                    background-color: #f44336;
                }
                QPushButton#closeButton:hover {
                    background-color: #d32f2f;
                }
            """)
            
            # 创建对话框布局
            layout = QVBoxLayout(success_dialog)
            layout.setContentsMargins(30, 30, 30, 20)
            layout.setSpacing(20)
            
            # 添加成功图标和标题
            success_icon = QLabel()
            success_icon.setPixmap(QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation).pixmap(48, 48))
            success_icon.setAlignment(Qt.AlignCenter)
            layout.addWidget(success_icon)
            
            # 添加成功消息
            success_message = QLabel(f"材质包已成功转换到版本 {target_version}！")
            success_message.setAlignment(Qt.AlignCenter)
            success_message.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(success_message)
            
            # 添加文件列表区域
            file_list_frame = QFrame()
            file_list_frame.setStyleSheet("background-color: white; border-radius: 4px; padding: 10px;")
            file_list_layout = QVBoxLayout(file_list_frame)
            
            file_label = QLabel("转换后的文件:")
            file_label.setStyleSheet("font-weight: bold;")
            file_list_layout.addWidget(file_label)
            
            # 检查是否有转换后的文件路径
            if hasattr(pack, 'global_last_processed_files') and pack.global_last_processed_files:
                for file_path in pack.global_last_processed_files:
                    file_name = os.path.basename(file_path)
                    file_item = QLabel(f"• {file_name}")
                    file_item.setWordWrap(True)
                    file_list_layout.addWidget(file_item)
            else:
                no_files_label = QLabel("未找到转换后的文件信息")
                no_files_label.setStyleSheet("color: #999999;")
                file_list_layout.addWidget(no_files_label)
            
            layout.addWidget(file_list_frame)
            
            # 添加按钮区域
            buttons_frame = QFrame()
            buttons_layout = QHBoxLayout(buttons_frame)
            buttons_layout.setSpacing(10)
            buttons_layout.setContentsMargins(0, 0, 0, 0)
            
            # 添加查看文件按钮
            def open_file_location():
                if hasattr(pack, 'global_last_processed_files') and pack.global_last_processed_files:
                    # 获取第一个文件的目录
                    first_file_path = pack.global_last_processed_files[0]
                    directory = os.path.dirname(first_file_path)
                    
                    # 跨平台打开文件夹
                    import platform, subprocess
                    system_type = platform.system()
                    
                    try:
                        if system_type == 'Windows':
                            os.startfile(directory)
                        elif system_type == 'Darwin':  # macOS
                            subprocess.run(['open', directory], check=True)
                        else:  # Linux和其他Unix-like系统
                            subprocess.run(['xdg-open', directory], check=True)
                    except Exception as e:
                        print(f"打开文件夹失败: {str(e)}")
            
            open_button = QPushButton("查看文件")
            open_button.clicked.connect(open_file_location)
            buttons_layout.addWidget(open_button)
            
            # 添加关闭按钮
            close_button = QPushButton("关闭")
            close_button.setObjectName("closeButton")
            # 连接关闭按钮信号，先关闭对话框再重置页面
            close_button.clicked.connect(lambda: (success_dialog.close(), self.reset_conversion_page()))
            buttons_layout.addWidget(close_button)
            
            layout.addWidget(buttons_frame)
            
            # 居中显示对话框
            success_dialog.move(self.geometry().center() - success_dialog.rect().center())
            
            # 显示对话框
            success_dialog.exec_()
    


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle("Fusion")  # 使用Fusion样式，看起来更现代
    
    # 设置全局调色板
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(51, 51, 51))
    app.setPalette(palette)
    
    window = KPTMainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
