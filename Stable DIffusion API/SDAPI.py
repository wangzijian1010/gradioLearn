import webuiapi
from PIL import Image, PngImagePlugin,ImageDraw

# api = webuiapi.WebUIApi()
api = webuiapi.WebUIApi(host='127.0.0.1',
                        port=7861,
                        sampler='Euler a',
                        steps=20)

result1 = api.txt2img(prompt="cute squirrel",
                    negative_prompt="ugly, out of frame",
                    seed=1003,
                    styles=["anime"],
                    cfg_scale=7,
                     sampler_index='DDIM',
                     steps=30,
                      # 开启超分
                      enable_hr=False,
                      hr_scale=1.
                    )


result1.image.save('testwebui3.png')

# 完成图生图功能
result2 = api.img2img(
    images=[result1.image],
    prompt="cute cat",
    seed= 5555,
    cfg_scale=6.5,
    denoising_strength=0.5,
    batch_size=1,
)

# 图生图批量保存图片代码
# i = 0
# for saveImg in result2.images:
#     saveImg.save("testweb4" + str(i) + ".png")
#     i = i + 1


result2.image.save("testwebui4.png")

# img2img inpainting? 有什么用
# extra-single-image
result3 = api.extra_single_image(image=result2.image,
                                 upscaler_1=webuiapi.Upscaler.ESRGAN_4x,
                                 upscaling_resize=1.5)

result3.image.save("testwebui5.png")


result4 = api.extra_batch_images(images=[result1.image, result2.image],
                                 upscaler_1=webuiapi.Upscaler.ESRGAN_4x,
                                 upscaling_resize=1.5)
result4.images[0].save("testwebui6.png")
result4.images[1].save("testwebui7.png")



# 实现换SD模型
# 获取当前所有的sdmodels
test = api.get_sd_models()

# 获取当前使用的sd模型
old_model = api.util_get_current_model()

# get list of available models
# 获取当前可用的model
models = api.util_get_model_names()

# refresh list of models
# 刷新模型列表
api.refresh_checkpoints()

# 选择模型
# 这里选择的是models数组的第0个
api.util_set_model(models[1])

current_model = api.util_get_current_model()

# set model (find closest match)
# 这种是按照最接近的名称來設置模型
api.util_set_model('photon')
current_model = api.util_get_current_model()


controlnet = api.controlnet_model_list()

# 在文生图上使用controlNet
r = api.txt2img(
    prompt="photo of a beautiful girl with blonde hair",
    height=512,
    seed=100,
)

img = r.image
img.save("testwebui8.png")



# txt2img with ControlNet (used 1.0 but also supports 1.1)
unit1 = webuiapi.ControlNetUnit(input_image=img, module='canny', model='control_v11p_sd15_canny [d14c016b]')
r = api.txt2img(prompt="photo of a beautiful girl with black hair", controlnet_units=[unit1])
r.image.save("testwebui9.png")


unit1 = webuiapi.ControlNetUnit(input_image=img, module='canny', model='control_v11p_sd15_canny [d14c016b]')
unit2 = webuiapi.ControlNetUnit(input_image=img, module='depth', model='control_v11f1p_sd15_depth [cfd03158]', weight=0.5)

r2 = api.img2img(prompt="a Asian girl",
            images=[img],
            width=512,
            height=512,
            controlnet_units=[unit1, unit2],
            sampler_name="Euler a",
            cfg_scale=7,
           )

r2.images[0].save("testwebui10.png")
r2.images[1].save("testwebui11.png")
r2.images[2].save("testwebui12.png")


# 实现移除背景的功能
rembg = webuiapi.RemBGInterface(api)
r3 = rembg.rembg(input_image=img, model='u2net', return_mask=False)
r3.image.save("testwebui13.png")


print("hello SD")

