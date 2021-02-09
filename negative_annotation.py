from xml.dom.minidom import Document
import os
from PIL import Image
import cv2
import shutil
#txt只有图片的绝对路径
#重新命名 我的电脑 搜索 按序排列 直接删除
#误判图片 背景图 随意选 相似物
dir_img_path = "C:/Users/User/Desktop/Asianhornet-detection/negative/"  # 存放负样本图片的文件夹绝对路径
dir_xml_path = "C:/Users/User/Desktop/Asianhornet-detection/VOCdevkit/VOC2007/4/"  # 存放负样本标注空文件的文件夹绝对路径
# 判断负样本格式是否为.jpg或.png
img_file_list = [img_file for img_file in os.listdir(dir_img_path) if img_file.endswith('.jpg') or img_file.endswith('.png')]
if os.path.exists(dir_xml_path):
    shutil.rmtree(dir_xml_path)
    os.mkdir(dir_xml_path)
else:
    os.mkdir(dir_xml_path)


# 自动生成负样本xml空标注文件
def create_negative_xml(img_file):
    doc = Document()
    # creat a root node which name is annotation
    annotation = doc.createElement('annotation')
    # add the root node to the dom document object
    doc.appendChild(annotation)

    # add the folder subnode
    folder = doc.createElement('folder')
    folder_text = doc.createTextNode('images')  # 存放图片的文件夹名称
    folder.appendChild(folder_text)
    annotation.appendChild(folder)

    # add the filename subnode
    filename = doc.createElement('filename')
    filename_text = doc.createTextNode(img_file)  # 图片名称
    filename.appendChild(filename_text)
    annotation.appendChild(filename)

    # add the path subnode
    path = doc.createElement('path')
    path_text = doc.createTextNode(dir_img_path + img_file)  # 图片绝对路径
    path.appendChild(path_text)
    annotation.appendChild(path)

    # add the source subnode
    source = doc.createElement('source')
    database = doc.createElement('database')
    database_text = doc.createTextNode('Unknown')
    source.appendChild(database)
    database.appendChild(database_text)
    annotation.appendChild(source)

    # add the size subnode
    size = doc.createElement('size')
    img = cv2.imread(dir_img_path + img_file)
    img_data = img.shape  # (576, 768, 3)—(height, width, depth)
    width = doc.createElement('width')
    width_text = doc.createTextNode(str(img_data[1]))  # 图片宽度
    height = doc.createElement('height')
    height_text = doc.createTextNode(str(img_data[0]))  # 图片高度
    depth = doc.createElement('depth')
    depth_text = doc.createTextNode(str(img_data[2]))  # 图片通道数
    size.appendChild(width)
    width.appendChild(width_text)
    size.appendChild(height)
    height.appendChild(height_text)
    size.appendChild(depth)
    depth.appendChild(depth_text)
    annotation.appendChild(size)

    # add the segmented subnode
    segmented = doc.createElement('segmented')
    segmented_text = doc.createTextNode('0')
    segmented.appendChild(segmented_text)
    annotation.appendChild(segmented)

    #write into the xml text file
    if img_file.endswith("jpg"):
        open(dir_xml_path+'%s.xml'%(img_file.split('.jpg')[0]),'w')  # 注意str.strip()函数的具体功能
        fp = open(dir_xml_path+'%s.xml'%(img_file.split('.jpg')[0]), 'w')
        doc.writexml(fp, addindent='\t', newl='\n', encoding='utf-8')  # addindent是缩排格式,去掉indent='\t'
        fp.close()
    if img_file.endswith("png"):
        os.mknod(dir_xml_path+'%s.xml'%(img_file.split('.png')[0]))
        fp = open(dir_xml_path+'%s.xml'%(img_file.split('.png')[0]), 'w')
        doc.writexml(fp, addindent='\t', newl='\n', encoding='utf-8')  # addindent是缩排格式,去掉indent='\t'
        fp.close()


if __name__ == "__main__":
    for img_file in img_file_list:
        # 判断图片是否存在
        try:
            img = Image.open(dir_img_path + img_file)
        except FileNotFoundError:
            print("Warning：%s is not found!" % (img_file))
            continue
        # 判断图片是否损坏
        try:
            img.load()
        except OSError:
            print("Warning：%s is broken!" % (img_file))
            continue
        # 生成符合要求的负样本标注文件
        create_negative_xml(img_file)
