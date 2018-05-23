from time import sleep
import time

import cv2
import numpy as np


# define range of red color in ycc
lower_red = np.array([60, 140, 121])
upper_red = np.array([115, 180, 134])

# define range of yellow color in ycc
lower_yellow = np.array([143, 128, 59])
upper_yellow = np.array([175, 165, 104])

# define range of blue color in ycc
lower_blue = np.array([23, 87, 145])
upper_blue = np.array([105, 111, 179])




def get_target(cap, color):
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

    ret_cam, resized = cap.read()



    resized = cv2.blur(resized, (10, 10))



    ycc = cv2.cvtColor(resized, cv2.COLOR_BGR2YCrCb)

    if color == "red":
        mask = cv2.inRange(ycc, lower_red, upper_red)
    if color == "blue":
        mask = cv2.inRange(ycc, lower_blue, upper_blue)
    if color == "yellow":
        mask = cv2.inRange(ycc, lower_yellow, upper_yellow)

    # Bitwise-AND mask and original image
    masked_resized = cv2.bitwise_and(resized, resized, mask=mask)


    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200
    params.blobColor = 255

    w, h, c = resized.shape
    # Filter by Area.
    params.filterByArea = True
    params.minArea = int(((w + h) / 4) + 1)

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


    # get biggest blob
    if len(keypoints) > 0:
        max = 0
        pos = 0
        max_pos = 0

        for keypoint in keypoints:

            if keypoint.size > max:
                max = keypoint.size
                max_pos = pos

            pos += 1

        biggest_target = keypoints[max_pos]

        target_position = biggest_target.pt[0] / resized.shape[1]



    else:
        target_position = -1

    # print(target_position)

    return target_position


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

        ret_cam, resized = cap.read()

        resized = cv2.blur(resized, (10, 10))



        ycc = cv2.cvtColor(resized, cv2.COLOR_BGR2YCrCb)
        mask = cv2.inRange(ycc, lower_red, upper_red)

        # Bitwise-AND mask and original image
        masked_resized = cv2.bitwise_and(resized, resized, mask=mask)

        params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        params.minThreshold = 10
        params.maxThreshold = 200
        params.blobColor = 255

        w, h, c = resized.shape
        # Filter by Area.
        params.filterByArea = True
        params.minArea = int(((w + h) / 10) + 1)

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

        # todo
        # keypoints[0].pt # position
        # keypoints[0].size # size

        if len(keypoints) > 0:
            max = 0
            pos = 0
            max_pos = 0

            for keypoint in keypoints:

                if keypoint.size > max:
                    max = keypoint.size
                    max_pos = pos


                pos += 1

            biggest_target = keypoints[max_pos]

            target_position = biggest_target.pt[0] / resized.shape[1]



        else:
            target_position = -1




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
