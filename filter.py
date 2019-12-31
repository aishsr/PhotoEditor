import cv2

#Get On Change position on the track bar
def trackerSet(hue=0, sat=0):
    hue = cv2.getTrackbarPos('Hue', 'Settings')
    sat = cv2.getTrackbarPos('Sat', 'Settings')
    bright = cv2.getTrackbarPos('Brightness', 'Settings')
    contrast = cv2.getTrackbarPos('Contrast', 'Settings')

    #apply effect
    effect = applySetting(hsv, hue, sat,img, bright, contrast)

    #show effect
    cv2.imshow('Settings', effect)
    cv2.resizeWindow('Settings', 900, 600)

#Apply Filters
def applySetting(input_img, hue=179, sat=255, brightness=255, contrast=127):
    originalPosH = 179
    originalPosS = 255

    #Get position change on trackbar
    hue = cv2.getTrackbarPos('Hue', 'Settings')
    sat = cv2.getTrackbarPos('Sat', 'Settings')
    brightness = map(brightness, 0, 510, -255, 255)
    contrast = map(contrast, 0, 254, -127, 127)

    #Transfer to HSV format
    h, s, v = cv2.split(input_img)

    #Hue
    if ((hue - originalPosH) >= 0):
        h = h + (hue - originalPosH)
    else:
        h = h - (originalPosH - hue)
    print (h)

    #Saturation
    if ((sat - originalPosS) >= 0):
        s = s + (sat - originalPosS)
    else:
        s = s - (originalPosS - sat)
    #print (s[0][0])

    # for i in range(len(s)):
    #     for j in range(len(s[i])):
    #         if s[i][j] != 0 or s[i][j] != 255:
    #             s = s + (sat - originalPosS)

    #Merge HSV channels -> RGB
    hsv = cv2.merge([h, s, v])
    rgbimg = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    #Brightness
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        newImg = cv2.addWeighted(rgbimg, alpha_b, rgbimg, 0, gamma_b)
    else:
        newImg = rgbimg.copy()

    if contrast != 0:
        f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        newImg = cv2.addWeighted(newImg, alpha_c, newImg, 0, gamma_c)

    return newImg

#to get the offset
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


#Main
if __name__ == '__main__':
    original = cv2.imread("flower.jpg", 1)
    hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('Settings')
    img = original.copy()


    #constants
    hue = 179
    sat = 255
    bri = 255
    con = 127

    #Create trackbars
    cv2.createTrackbar('Hue', 'Settings', hue, 2 * 179, trackerSet)
    cv2.createTrackbar('Sat', 'Settings', sat, 2*255, trackerSet)
    cv2.createTrackbar('Brightness', 'Settings', bri, 2 * 255, trackerSet)
    cv2.createTrackbar('Contrast', 'Settings', con, 2 * 127, trackerSet)

    trackerSet(0)
    cv2.imshow('Settings', original)
    cv2.resizeWindow('Settings', 900, 600)

cv2.waitKey(0)
