import pickle
import numpy as np

class SimpleDigitRecognizer:
    def __init__(self):
        self.templates = []
        self.labels = []
        self.create_templates()
    
    def create_templates(self):
        # 为每个数字创建简单的模板
        for digit in range(10):
            # 创建一个8x8的网格表示数字
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
        # 将输入图像调整为8x8并二值化
        img = self.preprocess(image)
        
        # 简单的模板匹配
        min_dist = float('inf')
        best_match = 0
        
        for template, label in zip(self.templates, self.labels):
            dist = np.sum((img - template) ** 2)
            if dist < min_dist:
                min_dist = dist
                best_match = label
                
        return best_match
    
    def preprocess(self, image):
        # 调整大小并二值化
        from PIL import Image
        import io
        
        img = Image.open(io.BytesIO(image))
        img = img.convert('L').resize((8, 8), Image.Resampling.LANCZOS)
        img_array = np.array(img)
        
        # 二值化
        threshold = 128
        img_array = (img_array > threshold).astype(float)
        
        return img_array.flatten()

if __name__ == '__main__':
    # 创建模型实例
    model = SimpleDigitRecognizer()
    
    # 保存模型到文件
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("模型已成功创建并保存为 model.pkl")