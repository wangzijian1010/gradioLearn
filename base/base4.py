import gradio as gr


def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "sub":
        return num1 - num2
    elif operation == "mult":
        return num1 * num2
    elif operation == "div":
        if num2 == 0:
            # 设置报错弹窗
            raise gr.Error("divide can't be zero")
        return num1 / num2


demo = gr.Interface(
    calculator,
    # 设置输入
    [
        "number",
        gr.Radio(["add", "sub", "mult", "div"]),
        "number"
    ],
    # 设置输出
    "number",
    # 设置输入参数示例
    examples=[
        [5, "add", 3],
        [4, "div", 2],
        [-4, "mult", 2.5],
        [0, "sub", 1.2],
    ],
    # 设置网页标题
    title="Toy Calculator",
    # 左上角的描述文字
    description="Here's a sample toy calculator. Enjoy!",
    # 左下角的文字
    article = "Check out the examples",
    live=True,
)

demo.launch()