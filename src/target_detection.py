from time import sleep
import time

import cv2
import numpy as np
import operator


def get_target(cap):
    """
    Vind beweging in het zichtveld van de camera. 0 voor links en 1 voor rechts. -1 voor geen beweging.
    :return: De richting waar zich de beweging bevind,
    """
    cap.set(3, 320)
    cap.set(4, 240)


    if not cap.isOpened():
        #  sudo modprobe bcm2835-v4l2
        print("CAPTURE DEVICE NOT FOUND")
        exit(2)

    ret_cam, image = cap.read()
    resized = image  # cv2.resize(image, (100, 100), interpolation=cv2.INTER_CUBIC)

    resized_inv = cv2.bitwise_not(resized)  # red = cyan due to colorspace wraping
    resized_inv = cv2.blur(resized_inv, (10, 10))

    hsv_inv = cv2.cvtColor(resized_inv, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_cyan = np.array([80, 60, 80])
    upper_cyan = np.array([90, 255, 255])

    mask = cv2.inRange(hsv_inv, lower_cyan, upper_cyan)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(hsv_inv, hsv_inv, mask=mask)

    # cv2.imshow('mask', res)
    # cv2.waitKey(0)


    print("calculating target...")
    rows, cols, channels = hsv_inv.shape
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

    direction = index / len(sum_arr)

    return direction


if __name__ == "__main__":

    total = 0
    numMeasures = 100
    cv2.namedWindow('result')

    cap = cv2.VideoCapture(-1)
    sleep(.2)
    cap.set(3, 320)
    cap.set(4, 240)

    while (1):

        start = time.clock()
        ret_cam, resized = cap.read()


        ########################################################### MASKING

        # image = cv2.imread('/home/pi/gyrosphere/src/cola.jpg')
        # resized = cv2.resize(image, (640, 480), interpolation=cv2.INTER_CUBIC)

        resized_inv = cv2.bitwise_not(resized)  # red = cyan due to colorspace wraping


        #########  BLUR
        #resized_inv = cv2.GaussianBlur(resized_inv, (15, 15), 0)

        resized_inv = cv2.blur(resized_inv, (10, 10))

        ######### end BLUR
        # define range of blue color in HSV
        lower_cyan = np.array([80, 15, 40])
        upper_cyan = np.array([90, 255, 255])

        hsv_inv = cv2.cvtColor(resized_inv, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_inv, lower_cyan, upper_cyan)

        # Bitwise-AND mask and original image
        masked_resized_inv = cv2.bitwise_and(resized_inv, resized_inv, mask=mask)

        # again but with de-inverted colors for human viewing
        res_normal = cv2.bitwise_and(resized, resized, mask=mask)

        ############################################################## END MASKING



        # mask = cv2.GaussianBlur(mask, (15, 15), 0)
        # _, mask = cv2.threshold(mask, 124, 255, cv2.THRESH_BINARY)
        # # Show mask


        #



        params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        params.minThreshold = 10
        params.maxThreshold = 200
        params.blobColor = 255

        w, h, c = resized.shape
        # Filter by Area.
        params.filterByArea = True
        params.minArea = int(((w + h) / 40) + 1)

        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.01

        # Filter by Inertia
        params.filterByInertia = False
        params.minInertiaRatio = 0.1

        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)

        # Detect blobs.
        keypoints = detector.detect(mask)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        # the size of the circle corresponds to the size of blob

        im_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0, 0, 255),
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        end = time.clock()

        #todo
        keypoints[0].pt # position
        keypoints[0].size # size



        # Show blobs
        #cv2.imshow('result', mask)
        cv2.imshow('result', im_with_keypoints)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


    # index, value = max(enumerate(sum_arr), key=operator.itemgetter(1))



    # print(index)


    # cv2.imshow('frame', res_normal)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    # cv2.waitKey(0)
