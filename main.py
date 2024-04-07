import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from skimage import io, color, filters, feature
import matplotlib.pyplot as plt

# 图像处理函数
def process_image(image_path):
    image = io.imread(image_path)
    image_gray = color.rgb2gray(image)
    otsu_threshold_value = filters.threshold_otsu(image_gray)
    manual_threshold_value = otsu_threshold_value
    binary_image = image_gray > manual_threshold_value
    edges = feature.canny(image_gray, sigma=1.0)
    binary_image[edges] = 0  # 在二值图像上叠加边缘

    # 保存处理后的图像
    processed_image_path = os.path.join(os.getcwd(), 'processed_image.png')
    plt.imsave(processed_image_path, binary_image, cmap='gray')
    return processed_image_path

# 打开文件选择对话框并处理图像
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        processed_image_path = process_image(file_path)
        show_processed_image(processed_image_path)
    else:
        messagebox.showinfo("Info", "No file selected.")

# 显示处理后的图像
def show_processed_image(image_path):
    global image_label
    processed_image = Image.open(image_path)
    processed_photo = ImageTk.PhotoImage(processed_image)
    image_label.config(image=processed_photo)
    image_label.image = processed_photo

# 返回初始状态
def reset_app():
    image_label.config(image='')
    image_label.image = ''

# 创建GUI
app = tk.Tk()
app.title('Image Processing App')

# 开始按钮
start_button = tk.Button(app, text='Start', command=open_file)
start_button.pack(side='top', pady=10)

# 显示图像的标签
image_label = tk.Label(app)
image_label.pack()

# 返回按钮
reset_button = tk.Button(app, text='Reset', command=reset_app)
reset_button.pack(side='bottom', pady=10)

app.mainloop()