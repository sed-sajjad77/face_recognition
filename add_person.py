import cv2
import uuid
import os
import argparse


class person:
    def __init__(self, dir_train, dir_val, dir_test):
        self.dir_train = dir_train
        self.dir_val = dir_val
        self.dir_test = dir_test

    def add(self):
        # Establish a connection to the webcam
        cap = cv2.VideoCapture(0)
        i = 0
        while cap.isOpened():

            ret, frame = cap.read()

            # Cut down frame to 250x250px
            frame = frame[120:120+250, 200:200+250, :]

            if cv2.waitKey(1) & 0XFF == ord('a'):

                if i < 40:
                    # Create the unique file path
                    imgname = os.path.join(
                        self.dir_train, '{}.jpg'.format(uuid.uuid1()))
                    # Write out train image
                    cv2.imwrite(imgname, frame)

                elif i < 55:
                    # Create the unique file path
                    imgname = os.path.join(
                        self.dir_val, '{}.jpg'.format(uuid.uuid1()))
                    # Write out val images
                    cv2.imwrite(imgname, frame)

                elif i < 65:
                    # Create the unique file path
                    imgname = os.path.join(
                        self.dir_test, '{}.jpg'.format(uuid.uuid1()))
                    # Write out test image
                    cv2.imwrite(imgname, frame)

                else:
                    break

                i += 1

            # Show image back to screen
            cv2.imshow('Image Collection', frame)

            # Breaking gracefully
            if cv2.waitKey(25) & 0XFF == ord('q'):
                break

        # Release the webcam
        cap.release()
        # Close the image show frame
        cv2.destroyAllWindows()


if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--name', type=str, required=True)
    # Parse the argument
    args = parser.parse_args()

    # create files
    if not os.path.exists('data'):
        os.mkdir('data')
        os.mkdir('data/train')
        os.mkdir('data/validation')
        os.mkdir('data/test')
        f = open('data/names.txt', 'x')

    # check name in names.txt
    names_file = os.path.join('data', 'names.txt')
    with open(names_file) as f:
        names = [name.rstrip() for name in f]

    # error or append name in names.txt
    if args.name in names:
        print("error")
    else:
        file = open(names_file, 'a')
        file.writelines(f'{args.name}\n')
        file.close()

        # create dateset dir
        dir_path_train = os.path.join('data', 'train', args.name)
        dir_path_validation = os.path.join('data', 'validation', args.name)
        dir_path_test = os.path.join('data', 'test', args.name)

        if not os.path.exists(dir_path_train):
            os.mkdir(dir_path_train)
            os.mkdir(dir_path_validation)
            os.mkdir(dir_path_test)

        p = person(dir_path_train, dir_path_validation, dir_path_test)
        p.add()
