import gradio as gr

# 非模块化的写法
def greet(name):
    return "Hello " + name + "!"
with gr.Blocks() as demo:
    #设置输入组件
    name = gr.Textbox(label="Name")
    # 设置输出组件
    output = gr.Textbox(label="Output Box")
    #设置按钮
    greet_btn = gr.Button("Greet")
    #设置按钮点击事件
    greet_btn.click(fn=greet, inputs=name, outputs=output)
demo.launch()