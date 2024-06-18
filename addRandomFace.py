# First download Labelled Faces in the Wild dataset
# https://vis-www.cs.umass.edu/lfw/
import os
import tarfile
import random
import uuid


# Untar Labelled Faces in the Wild dataset
def untar(lfw_tgz_PATH):
    # Uncompress Tar GZ Labelled Faces in the Wild Dataset
    file = tarfile.open(lfw_tgz_PATH)

    # print file names
    # print(file.getnames())

    # extract files
    file.extractall('./')

    # close file
    file.close()


# create list of images PATH
def create_list_images(images_PATH):
    list_images = []
    for directory in os.listdir(images_PATH):
        for file in os.listdir(os.path.join(images_PATH, directory)):
            list_images.append(os.path.join(images_PATH, directory, file))
    return list_images


def help_move_images(list_train, list_valid, list_test, train_PATH, valid_PATH, test_PATH):
    #  Move random of LFW Images to the following repository data/{train,validation,test}/unknown
    for train in list_train:
        NEW_PATH = os.path.join(train_PATH, '{}.jpg'.format(uuid.uuid1()))
        # print(NEW_PATH)
        os.replace(train, NEW_PATH)

    for valid in list_valid:
        NEW_PATH = os.path.join(valid_PATH, '{}.jpg'.format(uuid.uuid1()))
        # print(NEW_PATH)
        os.replace(valid, NEW_PATH)

    for test in list_test:
        NEW_PATH = os.path.join(test_PATH, '{}.jpg'.format(uuid.uuid1()))
        # print(NEW_PATH)
        os.replace(test, NEW_PATH)


def move_images(list_images, number_of_images, percent_train, Percent_valid, train_PATH, valid_PATH, test_PATH):
    # Randomly select n names
    random_selection = random.sample(list_images, number_of_images)

    number_of_train = int(number_of_images*percent_train)
    number_of_valid = int(number_of_images*Percent_valid)

    list_train = random_selection[:number_of_train]
    list_valid = random_selection[number_of_train:number_of_train+number_of_valid]
    list_test = random_selection[number_of_train+number_of_valid:]

    help_move_images(list_train, list_valid, list_test,
                     train_PATH, valid_PATH, test_PATH)


if __name__ == "__main__":
    # Untar Labelled Faces in the Wild dataset
    # https://vis-www.cs.umass.edu/lfw/
    lfw_tgz_PATH = 'lfw.tgz'
    if not os.path.exists('lfw'):
        untar(lfw_tgz_PATH)
    else:
        print('Wild dataset is ready')

    # unknown_PATH = os.path.join('data','unknown')
    # if not os.path.exists(unknown_PATH):

    # create list of unknown images
    lfw_PATH = './lfw'
    list_unknown_images = create_list_images(lfw_PATH)
    # print(list_unknown_images)

    # Move random of LFW Images to the following repository data/{train,validation,test}/unknown
    number_of_unknown_images = 300
    if len(list_unknown_images) < number_of_unknown_images:
        raise ValueError(
            f"The list must contain at least {number_of_unknown_images} names.")

    percent_train = 75/100
    Percent_valid = 15/100

    train_PATH = os.path.join('data', 'train', 'unknown')
    valid_PATH = os.path.join('data', 'validation', 'unknown')
    test_PATH = os.path.join('data', 'test', 'unknown')

    # Check if the folder not exists
    if not os.path.exists(train_PATH):
        os.mkdir(train_PATH)
    if not os.path.exists(valid_PATH):
        os.mkdir(valid_PATH)
    if not os.path.exists(test_PATH):
        os.mkdir(test_PATH)

    # Check if the folder is empty
    if not os.listdir(train_PATH):
        move_images(list_unknown_images, number_of_unknown_images,
                    percent_train, Percent_valid, train_PATH, valid_PATH, test_PATH)
