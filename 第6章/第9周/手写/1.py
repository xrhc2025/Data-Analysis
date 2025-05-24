import os
import pickle
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

# 定义 SimpleDigitRecognizer 类
class SimpleDigitRecognizer:
    def __init__(self):
        self.templates = []
        self.labels = []
        self.create_templates()
    
    def create_templates(self):
        # 为每个数字创建更精确的模板
        for digit in range(10):
            grid = np.zeros((8, 8))
            
            if digit == 0:
                # 更圆的0
                grid[1:7, 1:7] = 1
                grid[2:6, 2:6] = 0
                grid[3, [2,5]] = 1  # 补全圆角
                grid[4, [2,5]] = 1
            elif digit == 1:
                # 更斜的1
                grid[1:7, 4] = 1
                grid[1, 3:5] = 1
                grid[6, 2:5] = 1
            elif digit == 2:
                # 更流畅的2
                grid[1, 2:6] = 1
                grid[2, [1,5]] = 1
                grid[3, [1,4]] = 1
                grid[4, [1,3]] = 1
                grid[5, [1,2]] = 1
                grid[6, 1:6] = 1
            elif digit == 3:
                # 双曲线的3
                grid[1, 2:6] = 1
                grid[2, [1,5]] = 1
                grid[3, 2:5] = 1
                grid[4, [1,5]] = 1
                grid[5, [1,5]] = 1
                grid[6, 2:6] = 1
            elif digit == 4:
                # 更标准的4
                grid[1:5, 4] = 1
                grid[4, 1:7] = 1
                grid[1, 2] = 1
                grid[2, 3] = 1
                grid[3, 4] = 1
                grid[5:7, 4] = 1
            elif digit == 5:
                # 更明显的5
                grid[1, 1:7] = 1
                grid[2, 1] = 1
                grid[3, 1:5] = 1
                grid[4, 5] = 1
                grid[5, [1,5]] = 1
                grid[6, 2:5] = 1
            elif digit == 6:
                # 更闭合的6
                grid[1, 2:5] = 1
                grid[2, [1,5]] = 1
                grid[3, 1] = 1
                grid[4, 2:5] = 1
                grid[5, [1,5]] = 1
                grid[6, 2:5] = 1
            elif digit == 7:
                # 带横线的7
                grid[1, 1:7] = 1
                grid[2, 6] = 1
                grid[3, 5] = 1
                grid[4, 4] = 1
                grid[5, 3] = 1
                grid[6, 2] = 1
            elif digit == 8:
                # 双圆的8
                grid[1, 2:5] = 1
                grid[2, [1,5]] = 1
                grid[3, [1,5]] = 1
                grid[4, 2:5] = 1
                grid[5, [1,5]] = 1
                grid[6, [1,5]] = 1
                grid[7, 2:5] = 1
            elif digit == 9:
                # 完整的9
                grid[1, 2:5] = 1
                grid[2, [1,5]] = 1
                grid[3, [1,5]] = 1
                grid[4, 2:5] = 1
                grid[5, 5] = 1
                grid[6, 2:5] = 1
                
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

# 初始化模型
model = SimpleDigitRecognizer()

# 保存模型
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"digit_{timestamp}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            file.seek(0)
            image_data = file.read()
            prediction = model.predict(image_data)
            
            return render_template('index.html', 
                                prediction=prediction,
                                image_file=filename)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)