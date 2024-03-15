import os
import numpy as np
import cv2 as cv
from PIL import Image
import shutil

def gif2img(path):
    if not path.endswith('gif'):#判断是否为gif文件
        print('目标文件不是gif文件，请检查文件路径')
        return []
    img_list = []
    try:
        im = Image.open(path)#打开gif文件
        while True:
            current = im.tell()#获取当前图像的位置
            # 为了保存为jpg格式，需要转化。否则可以保存为png
            img = im.convert('RGB')#色彩模式转换为RGB
            img = np.array(img, dtype=np.uint8)#转换为numpy数组，并设置数据类型
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)#色彩空间有RGB转换为BGR
            img_list.append(img)
            im.seek(current + 1)
    except Exception as e:
        if len(img_list) == 0:
            print('get error in getting image from gif as ', str(e))
            return []
        else:
            return img_list


def video2img(path):
    if not (path.endswith('.mp4') or path.endswith('.avi')):#判断是否为视频文件
        print('目标文件不是视频文件，请检查文件路径(当前仅支持avi文件与mp4文件)')
        return []
    try:
        img_list = []
        cap = cv.VideoCapture(path)#打开视频文件
        while (cap.isOpened()):
            ret, frame = cap.read()#获取一帧文件并得到获取状态，当获取失败，ret为FALSE，代表视频已经读取完毕，获取成功，则ret为TRUE，frame为获得的图像
            if not ret:#判断视频是否读取结束
                break
            # frame = cv.resize(frame, None, fx=0.2, fy=0.2)
            img_list.append(frame)
        cap.release()#释放视频文件
        return img_list
    except Exception as e:
        print('get error in getting image from video as ', str(e))
        return []


def img2gif(img_list, path):
    try:
        if not path.endswith('.gif'):#判断保存路径是否为gif文件
            parent = str(os.path.split(path)[0])#获得路径的父路径
            if not os.path.exists(parent):#判断父路径是否存在
                os.makedirs(parent)#创建文件夹
            path = parent + '/save.gif'#重置保存路径，使用默认文件名
        img_list = img_normal(img_list)#将图像队列进行尺寸归一化
        images = []
        for img in img_list:
            img=cv.cvtColor(img, cv.COLOR_BGR2RGB)#将图像从BGR色彩空间转换为RGB色彩空间

            img = Image.fromarray(img)#格式转换，从numpy数组转换位Image对象
            images.append(img)
        img.save(path, save_all=True, append_images=images, loop=0, duration=0.5)# 保存并生成gif动图
    except Exception as e:
        print('get error in getting image from video as ', str(e))
        return []


def img2video(img_list, path):
    try:
        if not (path.endswith('.mp4') or path.endswith('.avi')):#判断是否为视频文件
            parent = str(os.path.split(path)[0])#获取路径父目录
            if not os.path.exists(parent):#判断路径是否存在
                os.makedirs(parent)#创建文件夹
            path = parent + '/save.mp4'#重置保存路径，使用默认文件名
        img_list = img_normal(img_list)#将图像队列进行尺寸归一化
        type = path.split('.')[-1]#获取文件类型
        type_dict = {'mp4': 'mp4v', 'avi': 'XVID'}#文件类型-编码格式字典
        if not (type in list(type_dict.keys())):#判断是否为支持的文件类型
            path = path.split('.')[0] + '.mp4'#转换为MP4文件类型
            type = 'mp4'
        fourcc = cv.VideoWriter_fourcc(*type_dict[type])#生成编码信息
        videoWriter = cv.VideoWriter(path, fourcc, 30, ( img_list[0].shape[1],img_list[0].shape[0]))#声明文件写入对象，用于将图像写入视频
        for img in img_list:
            videoWriter.write(img)#将图像写入视频
        videoWriter.release()#释放对象
        print('视频已保存至%s' % path)
    except Exception as e:
        print('get error in merge images to video as ', str(e))


def img_normal(img_list: list):
    heights = []
    widths = []
    for img in img_list:
        heights.append(img.shape[0])#统计图像高
        widths.append(img.shape[1])#统计图像宽
    mean_height = int(np.mean(np.array(heights)))#计算图像平均高度
    mean_width = int(np.mean(np.array(widths)))#计算图像平均宽度
    for i, img in enumerate(img_list):
        img_list[i] = cv.resize(img, ( mean_width,mean_height))#图像尺寸调整
    return img_list


def save_img_list(img_list: list, path):
    if os.path.exists(path):#判断路径是否存在
        shutil.rmtree(path)#删除路径
    os.makedirs(path)#创建对应文件夹
    for i, img in enumerate(img_list):
        cv.imwrite(os.path.join(path, ('%d' % i).zfill(5) + '.jpg'), img)#图像写入指定路径


def read_img_list(path):
    if not os.path.exists(path):#判断路径是否存在
        print('路径 %s 不存在' % path)#创建对应文件夹
        return []
    files = os.listdir(path)#获取路径下所有文件的文件名
    img_list = []
    for file in files:#遍历所有文件名
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.bmp'):#判断是否为图像文件
            try:
                img = cv.imread(os.path.join(path, file))#读取图像
                img_list.append(img)
            except Exception as e:
                print('get error as %s when reading data%s' % (str(e), file))
    return img_list


if __name__ == '__main__':
    menu_title = "*" * 10 + "Picture Process Tools" + "*" * 10 + '\n'
    function1 = ' ' * 14 + "1:gif转换为视频" + '\n'
    function2 = ' ' * 14 + "2:gif保存为图片" + '\n'
    function3 = ' ' * 14 + "3:视频转换为gif" + '\n'
    function4 = ' ' * 14 + "4:视频保存为图片" + '\n'
    function5 = ' ' * 14 + "5:图片转换为gif" + '\n'
    function6 = ' ' * 14 + "6:图片转换为视频" + '\n'
    function7 = ' ' * 14 + "7:退出" + '\n'
    menu = menu_title + function1 + function2 + function3 + function4 + function5 + function6 + function7#创建菜单
    function_dict = {1: [gif2img, img2video], 2: [gif2img, save_img_list], 3: [video2img, img2gif],
                     4: [video2img, save_img_list], 5: [read_img_list, img2gif], 6: [read_img_list, img2video]}#创建函数字典
    while True:
        print(menu)#输出菜单
        order = input('请选择对应功能 1-7:')#获取用户输入
        if not order.isdigit():#判断用户输入是否为数字
            print('请输入正确的选项 1-7')
            continue
        order = int(order)#str转int
        if order == 7:
            print('谢谢使用，再见')
            break
        if not (1 <= order <= 7):
            print('请输入正确的选项 1-7')
            continue
        if 1 <= order <= 4:
            s_path = input('请输入文件路径')
        else:
            s_path = input('请输入文件夹路径')
        d_path = input('请输入文件保存路径')
        print('处理中...')
        fun1, fun2 = function_dict[order]#根据输入的指令获取对应的两个函数，
        img_list = fun1(s_path)
        if len(img_list) == 0:
            print('从 %s 中加载图片失败，请检查文件路径' % s_path)
            continue
        fun2(img_list, d_path)
        print('转换成功')
