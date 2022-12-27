#coding:utf-8
import cv2
import os
import random

label_folder = './labels/' 

raw_images_folder = './raw_images/' 

save_images_folder = './save_image/'  

name_list_path = './name_list.txt'  

classes_path = './classes.txt'


def plot_one_box(x, image, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(image, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

def draw_box_on_image(image_name, classes, colors, label_folder, raw_images_folder, save_images_folder ):
    txt_path  = os.path.join(label_folder,'%s.txt'%(image_name)) 
    print(image_name)
    if image_name == '.DS_Store':
        return 0
    image_path = os.path.join( raw_images_folder,'%s.jpg'%(image_name))  
    
    save_file_path = os.path.join(save_images_folder,'%s.jpg'%(image_name))
    
    # flag_people_or_car_data = 0  
    source_file = open(txt_path) if os.path.exists(txt_path) else []
    image = cv2.imread(image_path)
    try:
        height, width, channels = image.shape
    except:
        print('no shape info.')
        return 0

    box_number = 0
    for line in source_file: 
        staff = line.split() 
        class_idx = int(staff[0])

        x_center, y_center, w, h = float(staff[1])*width, float(staff[2])*height, float(staff[3])*width, float(staff[4])*height
        x1 = round(x_center-w/2)
        y1 = round(y_center-h/2)
        x2 = round(x_center+w/2)
        y2 = round(y_center+h/2)     
        
        # if class_idx == 0: 
        #     draw_people_tangle = cv2.rectangle(image, (x1,y1),(x2,y2),(0,0,255),2)   
        #     cv2.imwrite(save_file_path,draw_people_tangle) 
        # elif class_idx == 1:
        #     draw_car_tangle = cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)     
        #     cv2.imwrite(save_file_path,draw_car_tangle)  

        plot_one_box([x1,y1,x2,y2], image, color=colors[class_idx], label=classes[class_idx], line_thickness=None)

        cv2.imwrite(save_file_path,image) 

        box_number += 1
    return box_number
    

def make_name_list(raw_images_folder, name_list_path):

    image_file_list = os.listdir(raw_images_folder) 

    text_image_name_list_file=open(name_list_path,'w')  

    for  image_file_name in image_file_list:
        image_name,file_extend = os.path.splitext(image_file_name)  
        text_image_name_list_file.write(image_name+'\n') 
    
    text_image_name_list_file.close()


if __name__ == '__main__':           

    make_name_list(raw_images_folder, name_list_path) 

    classes = image_names = open(classes_path).read().strip().split('\n')
    random.seed(42)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))]

    image_names = open(name_list_path).read().strip().split() 

    box_total = 0
    image_total = 0
    for image_name in image_names:
        box_num = draw_box_on_image(image_name, classes, colors, label_folder, raw_images_folder, save_images_folder)
        box_total += box_num
        image_total += 1
        print('Box number:', box_total, 'Image number:',image_total)