import sys
import os
import pickle
import numpy as np
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
                            QMessageBox, QSpinBox, QComboBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class DigitRecognizerTrainer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.current_image = None
        self.current_label = None
        self.training_data = []
        
        self.init_ui()
        self.load_model()
        
    def init_ui(self):
        self.setWindowTitle("手写数字识别模型微调工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 主部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # 顶部布局 - 图像显示
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 400)
        self.image_label.setStyleSheet("background-color: white; border: 1px solid black;")
        main_layout.addWidget(self.image_label)
        
        # 中间布局 - 控制按钮
        control_layout = QHBoxLayout()
        
        # 左侧控制
        left_control = QVBoxLayout()
        
        self.load_image_btn = QPushButton("加载图像")
        self.load_image_btn.clicked.connect(self.load_image)
        left_control.addWidget(self.load_image_btn)
        
        self.draw_btn = QPushButton("手写数字")
        self.draw_btn.clicked.connect(self.start_drawing)
        left_control.addWidget(self.draw_btn)
        
        self.clear_btn = QPushButton("清除画布")
        self.clear_btn.clicked.connect(self.clear_canvas)
        left_control.addWidget(self.clear_btn)
        
        control_layout.addLayout(left_control)
        
        # 右侧控制
        right_control = QVBoxLayout()
        
        self.label_combo = QComboBox()
        self.label_combo.addItems([str(i) for i in range(10)])
        self.label_combo.setCurrentIndex(0)
        right_control.addWidget(QLabel("选择数字标签:"))
        right_control.addWidget(self.label_combo)
        
        self.add_sample_btn = QPushButton("添加训练样本")
        self.add_sample_btn.clicked.connect(self.add_training_sample)
        right_control.addWidget(self.add_sample_btn)
        
        self.train_btn = QPushButton("训练模型")
        self.train_btn.clicked.connect(self.train_model)
        right_control.addWidget(self.train_btn)
        
        self.save_model_btn = QPushButton("保存模型")
        self.save_model_btn.clicked.connect(self.save_model)
        right_control.addWidget(self.save_model_btn)
        
        control_layout.addLayout(right_control)
        
        main_layout.addLayout(control_layout)
        
        # 底部状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")
        
        # 绘图相关
        self.drawing = False
        self.last_point = None
        
    def load_model(self):
        try:
            with open('model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            self.status_bar.showMessage("模型加载成功")
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法加载模型: {str(e)}")
            self.model = SimpleDigitRecognizer()
            self.status_bar.showMessage("创建新模型")
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.current_image = Image.open(file_path).convert('L')
            self.display_image(self.current_image)
            self.status_bar.showMessage(f"已加载图像: {os.path.basename(file_path)}")
    
    def start_drawing(self):
        self.current_image = Image.new('L', (400, 400), color=255)
        self.display_image(self.current_image)
        self.drawing = True
        self.status_bar.showMessage("请在画布上绘制数字")
    
    def clear_canvas(self):
        if self.current_image:
            self.current_image = Image.new('L', (400, 400), color=255)
            self.display_image(self.current_image)
            self.status_bar.showMessage("画布已清除")
    
    def mousePressEvent(self, event):
        if self.drawing and self.image_label.underMouse():
            self.last_point = event.pos() - self.image_label.pos()
            self.draw_point(self.last_point)
    
    def mouseMoveEvent(self, event):
        if self.drawing and self.last_point and self.image_label.underMouse():
            current_point = event.pos() - self.image_label.pos()
            self.draw_line(self.last_point, current_point)
            self.last_point = current_point
    
    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.last_point = None
    
    def draw_point(self, point):
        if not self.current_image:
            return
            
        draw = ImageDraw.Draw(self.current_image)
        x = point.x() - (self.image_label.width() - 400) // 2
        y = point.y() - (self.image_label.height() - 400) // 2
        
        if 0 <= x < 400 and 0 <= y < 400:
            draw.ellipse((x-5, y-5, x+5, y+5), fill=0)
            self.display_image(self.current_image)
    
    def draw_line(self, start, end):
        if not self.current_image:
            return
            
        draw = ImageDraw.Draw(self.current_image)
        start_x = start.x() - (self.image_label.width() - 400) // 2
        start_y = start.y() - (self.image_label.height() - 400) // 2
        end_x = end.x() - (self.image_label.width() - 400) // 2
        end_y = end.y() - (self.image_label.height() - 400) // 2
        
        if (0 <= start_x < 400 and 0 <= start_y < 400 and 
            0 <= end_x < 400 and 0 <= end_y < 400):
            draw.line((start_x, start_y, end_x, end_y), fill=0, width=10)
            self.display_image(self.current_image)
    
    def display_image(self, image):
        if image.mode == 'L':
            img = image.convert('RGBA')
        else:
            img = image.copy()
            
        qimage = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        
        # 保持宽高比缩放
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), 
                              Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
    
    def add_training_sample(self):
        if not self.current_image:
            QMessageBox.warning(self, "警告", "请先加载或绘制图像")
            return
            
        try:
            # 预处理图像
            img = self.current_image.resize((8, 8), Image.LANCZOS)
            img_array = np.array(img)
            threshold = 128
            img_array = (img_array > threshold).astype(float).flatten()
            
            # 获取标签
            label = int(self.label_combo.currentText())
            
            # 添加到训练数据
            self.training_data.append((img_array, label))
            self.status_bar.showMessage(f"已添加样本: 数字 {label} (总样本数: {len(self.training_data)})")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"添加样本失败: {str(e)}")
    
    def train_model(self):
        if not self.training_data:
            QMessageBox.warning(self, "警告", "没有训练样本")
            return
            
        try:
            # 准备数据
            X = np.array([data[0] for data in self.training_data])
            y = np.array([data[1] for data in self.training_data])
            
            # 更新模型模板
            for digit in range(10):
                digit_samples = X[y == digit]
                if len(digit_samples) > 0:
                    # 计算平均值作为新模板
                    new_template = np.mean(digit_samples, axis=0)
                    self.model.templates[digit] = new_template
            
            self.status_bar.showMessage(f"模型已更新，使用了 {len(self.training_data)} 个样本")
            self.training_data = []  # 清空训练数据
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"训练失败: {str(e)}")
    
    def save_model(self):
        try:
            with open('model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            QMessageBox.information(self, "成功", "模型已保存到 model.pkl")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存模型失败: {str(e)}")

# 定义 SimpleDigitRecognizer 类 (与原始代码相同)
class SimpleDigitRecognizer:
    def __init__(self):
        self.templates = []
        self.labels = []
        self.create_templates()
    
    def create_templates(self):
        # 为每个数字创建简单的模板
        for digit in range(10):
            grid = np.zeros((8, 8))
            
            if digit == 0:
                grid[1:-1, 1:-1] = 1
                grid[2:-2, 2:-2] = 0
            elif digit == 1:
                grid[:, 3:5] = 1
            elif digit == 2:
                grid[1, 1:-1] = 1
                grid[2:-2, -2] = 1
                grid[-2, 1:-1] = 1
                grid[2:-2, 1] = 1
                grid[-1, 1] = 1
            elif digit == 3:
                grid[1, 1:-1] = 1
                grid[2:-2, -2] = 1
                grid[-2, 1:-1] = 1
                grid[2:-2, -2] = 1
            elif digit == 4:
                grid[2:-2, -3] = 1
                grid[-2, :] = 1
                grid[:, -3] = 1
            elif digit == 5:
                grid[1, 1:-1] = 1
                grid[2:4, 1] = 1
                grid[4, 1:-1] = 1
                grid[5:-1, -2] = 1
                grid[-2, 1:-2] = 1
            elif digit == 6:
                grid[2:-2, 1] = 1
                grid[1, 1:-1] = 1
                grid[-2, 1:-1] = 1
                grid[2:-2, -2] = 1
                grid[4, 1:-2] = 1
            elif digit == 7:
                grid[1, :] = 1
                for i in range(2, 8):
                    grid[i, 7-i] = 1
            elif digit == 8:
                grid[1, 1:-1] = 1
                grid[-2, 1:-1] = 1
                grid[2:-2, 1] = 1
                grid[2:-2, -2] = 1
                grid[4, 1:-1] = 1
            elif digit == 9:
                grid[1, 1:-1] = 1
                grid[2:-2, 1] = 1
                grid[4, 1:-1] = 1
                grid[2:4, -2] = 1
                grid[-2, 1:-2] = 1
            
            self.templates.append(grid.flatten())
            self.labels.append(digit)
    
    def predict(self, image):
        img = self.preprocess(image)
        
        min_dist = float('inf')
        best_match = 0
        
        for template, label in zip(self.templates, self.labels):
            dist = np.sum((img - template) ** 2)
            if dist < min_dist:
                min_dist = dist
                best_match = label
                
        return best_match
    
    def preprocess(self, image):
        from PIL import Image
        import io
        
        img = Image.open(io.BytesIO(image))
        img = img.convert('L').resize((8, 8), Image.LANCZOS)
        img_array = np.array(img)
        
        threshold = 128
        img_array = (img_array > threshold).astype(float)
        
        return img_array.flatten()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DigitRecognizerTrainer()
    window.show()
    sys.exit(app.exec_())