import os
import random


def main():
    dataset_name = '[DATASET_NAME]'
    folder_image_path = '[INPUT_FOLDER]/[IMAGE_FOLDER]'

    images = os.listdir(folder_image_path)

    valid_percent = 0.20

    group_divider = int(round(valid_percent * len(images)))
    groups = images[:]
    random.shuffle(groups)

    if len(groups[group_divider:]) + len(groups[:group_divider]) == len(images):
        train_txt = open(f'data/{dataset_name}_train.txt', 'w')
        train_txt.writelines([f'{line}\n' for line in groups[group_divider:]])
        train_txt.close()

        valid_txt = open(f'data/{dataset_name}_valid.txt', 'w')
        valid_txt.writelines([f'{line}\n' for line in groups[:group_divider]])
        valid_txt.close()


if __name__ == "__main__":
    main()
