import gradio as gr
scores = []
def track_score(score):
    scores.append(score)
    #返回分数top3
    top_scores = sorted(scores, reverse=True)[:3]
    return top_scores
demo = gr.Interface(
    track_score,
    # 输入
    gr.Number(label="Score"),
    # 输出
    gr.JSON(label="Top Scores")
)
demo.launch()
