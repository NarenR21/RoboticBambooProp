import cv2
import numpy as np
import os
import math

image_path = "photos"
def load_image(path, numImages = -1):
    images = []
    j = 0
    if os.path.exists(path):
        for i in os.listdir(path):
            if(j == numImages):
                break
            image_loc = os.path.join(path, i)
            image = cv2.imread(image_loc)
            if image is not None:
                image = cv2.resize(image, (300,400), interpolation=cv2.INTER_LINEAR)
                images.append(image)
                j+=1
    return images
def determine_masks(images):
    #BGR values
    #lower_red = np.array([156, 7, 254], dtype = "uint8")
    #upper_red= np.array([175, 27, 254], dtype = "uint8")
    #lower_red = np.array([0, 0, 0], dtype = "uint8")
    #upper_red= np.array([72, 60, 254], dtype = "uint8") 
    #
    masks = []
    for image in images:
        mask = np.ndarray(image.shape, np.uint8)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                mask[i,j] = getMagentaDistace(image[i,j])
        masks.append(mask)
    return masks

def getMagentaDistace(pixel):
    r = np.int64(pixel[2])
    g = np.int64(pixel[1])
    b = np.int64(pixel[0])
    r2, g2, b2, = 195, 63, 113
    red = (r-r2) **2 
    green = (g-g2) **2
    blue = (b-b2) **2
    # print(red)
    # print(blue)
    # print(green)

    # print(math.sqrt(red + green + blue))
    dist = math.sqrt(red + green + blue)
    if dist > 50:
        return 0
    else:
        return 1

def update_flightControls():
    pass

if __name__ == "__main__":
    images = load_image(image_path)
    print("images loaded")
    masks = determine_masks(images)
    print("masks found")
    for i in range(len(images)):
        if not np.all(np.where(masks[i] >= 1)):
            center = [np.average(indices).astype(np.uint32) for indices in np.where(masks[i] >= 1)]
        else:
            center = [150, 200]
        masks[i] = (masks[i] * 255).astype(np.uint8)
        print(center)
        cv2.circle(masks[i], (center[1], center[0]), 1, (0, 0, 255), 2)
        cv2.imshow("image", images[i])
        cv2.imshow("mask", cv2.bitwise_and(images[i], masks[i]))
        cv2.waitKey(0)