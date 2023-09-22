import argparse
import webuiapi
from PIL import Image
from datetime import datetime
import os

# 初始化输入参数
parser = argparse.ArgumentParser(description='Generate image from text using webuiapi')
parser.add_argument('--batchsize', type=int, default=4, help='Batch size for generating images')
parser.add_argument('--prompt', type=str,
                    default='A female engineer in a white coat joyfully communicating with a small humanoid robot, in a bright modern laboratory setting, white, clean lines, reflective surfaces, soft lighting, high detail, optimistic mood.',
                    help='Prompt for generating image')
parser.add_argument('--negative_prompt', type=str, default='(worst quality, low quality, letterboxed)')
parser.add_argument('--denoising_strength', type=float, default=0.5, help='Strength of denoising')
parser.add_argument('--seed', type=int, default=2080962745, help='Seed for random number generator')
parser.add_argument('--cfg_scale', type=int, default=8, help='Scale of config used for generating image')
parser.add_argument('--sampler_name', type=str, default='DPM++ SDE Karras', help='Sampler index for generating image')
parser.add_argument('--steps', type=int, default=40, help='Number of steps for generating image')
parser.add_argument('--enable_hr', type=bool, default=False, help='Enable high resolution mode for generating image')
parser.add_argument('--hr_scale', type=float, default=1., help='Scale of high resolution mode for generating image')
parser.add_argument('--outputdir', type=str, default='txt2Img.png', help='Output directory for generated image')
parser.add_argument("--width", type=int, default=512, help="the outputImg's width")
parser.add_argument("--height", type=int, default=512, help="the outputImg's height")
# 加入SD模型选择参数
parser.add_argument("--modelname", type=str, default='ToonYou', help="the model's name")
# 加入vae模型选择
parser.add_argument("--vaemodels", type=str, default='vae-ft-mse-840000-ema-pruned.ckpt', help='vae models select')
# clip数字输入
parser.add_argument("--clip", type=int, default=2, help="the num of clip")
# 加入超分模型的选择
parser.add_argument("--upscale",type=str,default='R-ESRGAN 4x+',help="selcect upscale mode")
# 加入超分放大的倍数
parser.add_argument("--scaleNum",type=float,default=2.5,help="the number of upscale")
args = parser.parse_args()

# 初始化webui的端口和IP
api = webuiapi.WebUIApi(host='192.168.71.95', port=7860)


def TXT2IMG(
        batchsize=args.batchsize,
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        denoising_strength=args.denoising_strength,
        seed=args.seed,
        cfg_scale=args.cfg_scale,
        sampler_name=args.sampler_name,
        steps=args.steps,
        enable_hr=args.enable_hr,
        hr_scale=args.hr_scale,
        width=args.width,
        height=args.height,
        modelname=args.modelname,
        vae=args.vaemodels,
        clip=args.clip,
        upscale=args.upscale,
        scalenum=args.scaleNum):
    # 设置controlNet模型
    # 设置初始化模型
    api.refresh_checkpoints()
    api.util_set_model(modelname)

    # vae = api.get_sd_vae()

    options = {}
    options['sd_vae'] = vae
    # options['sd_vae'] = 'Automatic'
    api.set_options(options)
    override = {}
    override["CLIP_stop_at_last_layers"] = clip

    # 文生图
    # with controlnet
    resultImg = api.txt2img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        seed=seed,
        denoising_strength=denoising_strength,
        cfg_scale=cfg_scale,
        sampler_name=sampler_name,
        steps=steps,
        enable_hr=enable_hr,
        hr_scale=hr_scale,
        save_images=True,
        batch_size=batchsize + 1 ,
        height=height,
        width=width)


    UpscalerDic = {'R_ERSGAN_4x_Anime6B': webuiapi.Upscaler.R_ERSGAN_4x_Anime6B,
                   "None": webuiapi.Upscaler.none,
                   "Lanczos": webuiapi.Upscaler.Lanczos,
                   "Nearest": webuiapi.Upscaler.Nearest,
                   "LDSR": webuiapi.Upscaler.LDSR,
                   "BSRGAN": webuiapi.Upscaler.BSRGAN,
                   "R-ESRGAN 4x+": webuiapi.Upscaler.ESRGAN_4x,
                   "R-ESRGAN General 4xV3": webuiapi.Upscaler.R_ESRGAN_General_4xV3,
                   "ScuNET GAN": webuiapi.Upscaler.ScuNET_GAN,
                   "ScuNET PSNR": webuiapi.Upscaler.ScuNET_PSNR,
                   "SwinIR 4x": webuiapi.Upscaler.SwinIR_4x}


    # 加入单张图片的超分逻辑
    # result1 = api.extra_single_image(image=resultImg.image,
    #                                  upscaler_1=UpscalerDic[upscale],
    #                                  upscaling_resize=scalenum)

    # 记录批量生成的图像
    results = []
    final_results = []
    for i in range(batchsize):
        results.append(resultImg.images[i])
        final_results.append(api.extra_single_image(image=results[i],
                                                    upscaler_1=UpscalerDic[upscale],
                                                    upscaling_resize=scalenum))

    test = final_results

    final_results[0].image.save("./TEST0922.png")

    # result3.image.save("TEST1.png")

    # 生成时间戳
    # 输出到当前路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


    # 获取当前路径
    cwd = os.getcwd()
    # 图片存放文件夹名称
    dir_name = 'txt2imgoutput'

    # 检测文件名是否存在
    if not os.path.exists(os.path.join(cwd, dir_name)):
        # Create the directory
        os.makedirs(os.path.join(cwd, dir_name))
        print(f"Directory '{dir_name}' created successfully.")
    else:
        print(f"Directory '{dir_name}' already exists, the outputimg is in it.")

    for i in range(1, len(final_results)):
        final_results[i].image.save("./txt2imgoutput/" + str(timestamp) + "_" + str(i) + ".png")

    print("Image generated successfully!")


if __name__ == '__main__':
    TXT2IMG()
    print(api.util_get_current_model())
