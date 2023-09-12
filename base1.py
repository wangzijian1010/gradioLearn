import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(
    fn=greet,
    # 自定义输入框
    inputs=gr.Textbox(lines=3, placeholder="Name here ...",label="my input"),
    outputs= "text"
)

demo.launch()