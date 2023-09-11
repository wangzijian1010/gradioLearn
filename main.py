import gradio
import numpy as np
from transformers import pipeline



def greet(name):
    return "Hello" + name + "!"

def sepia(input_img):
    #处理图像
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

#接口创建函数
#fn设置处理函数，inputs设置输入接口组件，outputs设置输出接口组件
#fn,inputs,outputs都是必填函数

demo = gradio.Interface(fn = sepia,inputs = gradio.Image(shape=(300,300)),outputs="image")
demo.launch()