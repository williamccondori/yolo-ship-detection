import os
import shutil
import xml.etree.ElementTree as ET

from PIL import Image


def convert_to_yolo(image_width, image_height, bounding_box):
    image_w = 1./image_width
    image_h = 1./image_height

    x_center = (bounding_box[0] + bounding_box[1])/2.0 - 1
    y_center = (bounding_box[2] + bounding_box[3])/2.0 - 1

    width = bounding_box[1] - bounding_box[0]
    height = bounding_box[3] - bounding_box[2]

    return (x_center * image_w, y_center * image_h, width * image_w, height * image_h)


def main():
    object_class = 0
    image_extension = '[jpg, png, bmp]'

    folder_image_path = '[INPUT_FOLDER]/[IMAGE_FOLDER]'
    folder_annotation_path = '[INPUT_FOLDER]/[IMAGE_FOLDER]'

    output_folder = '[OUTPUT_FOLDER]'
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder)

    for annotation_file in os.listdir(folder_annotation_path):

        file_name = annotation_file.split('.')[0]
        image_file_path = f'{folder_image_path}/{file_name}.{image_extension}'
        image_file = Image.open(image_file_path)

        if image_file:

            # Read XML file.
            tree = ET.parse(f'{folder_annotation_path}/{annotation_file}')
            root = tree.getroot()

            # Copy image to output folder.

            shutil.copy(image_file_path,
                        f'{output_folder}/{file_name}.{image_extension}')

            # Create yolo annotation file.
            yolo_annotation = open(f'{output_folder}/{file_name}.txt', 'w')

            objects = root.findall('object')

            for object in objects:

                bndbox = object.find('bndbox')
                x_min = bndbox.find('xmin')
                y_min = bndbox.find('ymin')
                x_max = bndbox.find('xmax')
                y_max = bndbox.find('ymax')

                # Convert bounding box to yolo format.
                hrsc_box = (int(x_min.text), int(x_max.text),
                            int(y_min.text), int(y_max.text))
                yolo_box = convert_to_yolo(
                    int(image_file.width), int(image_file.height), hrsc_box)

                # Save yolo coordinates.
                yolo_annotation.write(
                    f'{object_class} {yolo_box[0]} {yolo_box[1]} {yolo_box[2]} {yolo_box[3]}\n')
            yolo_annotation.close()


if __name__ == "__main__":
    main()
