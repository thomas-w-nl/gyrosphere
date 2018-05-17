from time import sleep

import cv2
import numpy as np
import operator




def get_target(cap):
    """
    Vind beweging in het zichtveld van de camera. 0 voor links en 1 voor rechts. -1 voor geen beweging.
    :return: De richting waar zich de beweging bevind,
    """
    #camera.resolution = (320, 240)

    #cap.open()

    if not cap.isOpened():
        # try sudo modprobe bcm2835-v4l2

        print("CAPTURE DEVICE NOT FOUND")
        exit(2)



    ret_cam, image = cap.read()
    resized = cv2.resize(image, (100, 100), interpolation=cv2.INTER_CUBIC)




    resized_inv = cv2.bitwise_not(resized)  # red = cyan due to colorspace wraping

    hsv = cv2.cvtColor(resized_inv, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_cyan = np.array([70, 50, 30])
    upper_cyan = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_cyan, upper_cyan)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(hsv, hsv, mask=mask)


    #cv2.imshow('mask', res)


    print("calculating target...")
    rows, cols, channels = hsv.shape
    sum_arr = []

    for i in range(cols):
        col_sum = 0
        for j in range(rows):
            for x in range(channels):
                col_sum += res[j, i, x]

        sum_arr.append(col_sum)

    index, value = max(enumerate(sum_arr), key=operator.itemgetter(1))
    print("done")

    if value == 0:
        return -1

    direction = index/len(sum_arr)


    return direction


# if __name__ == "__main__":
#
#
#     image = cv2.imread('/home/thomas/PycharmProjects/gyrosphere/data/vga.jpg')
#     resized = cv2.resize(image, (640, 480), interpolation=cv2.INTER_CUBIC)
#
#     resized_inv = cv2.bitwise_not(resized) # red = cyan due to colorspace wraping
#
#     hsv = cv2.cvtColor(resized_inv, cv2.COLOR_BGR2HSV)
#
#     # define range of blue color in HSV
#     lower_cyan = np.array([70,50,30])
#     upper_cyan = np.array([90,255,255])
#
#     mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
#
#     # Bitwise-AND mask and original image
#     res = cv2.bitwise_and(hsv, hsv, mask=mask)
#
#     rows, cols, channels = hsv.shape
#     sum_arr = []
#
#
#     for i in range(cols):
#         col_sum = 0
#         for j in range(rows):
#             for x in range(channels):
#                 col_sum += res[j, i, x]
#
#         sum_arr.append(col_sum)
#
#
#
#     index, value = max(enumerate(sum_arr), key=operator.itemgetter(1))
#
#     print(index)
#
#     cv2.imshow('frame', res)
#     #cv2.imshow('mask', mask)
#     #cv2.imshow('res', res)
#     cv2.waitKey(0)
#
