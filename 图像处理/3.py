import cv2
from pylab import *

# 手动选取配准点进行配准融合
srcpoint = []
destpoint = []
sourcepoint = []
targetpoint = []


# 显示图像
def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 图像1的点击事件
def click_event_srcI1gray(event, x, y, flags, params):
    global srccount
    if event == cv2.EVENT_LBUTTONDOWN:
        srcpoint.append((x, y))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(I1gray, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (255, 0, 0), 1)
        cv2.imshow('Base Image', I1gray)


# 图像2的点击事件
def click_event_dstI2gray(event, x, y, flags, params):
    global destpoint
    if event == cv2.EVENT_LBUTTONDOWN:
        destpoint.append((x, y))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(I2gray, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (255, 0, 0), 1)
        cv2.imshow('Target Image', I2gray)


def homography_manual():
    global sourcepoint, targetpoint
    sourcepoint = np.array(srcpoint)
    targetpoint = np.array(destpoint)
    # h为仿射矩阵
    h, status = cv2.findHomography(sourcepoint, targetpoint)
    print(h)
    image_output = cv2.warpPerspective(I1gray, h, (I2gray.shape[1], I2gray.shape[0]))
    viewImage(image_output)
    rate = 0.5
    # 两张图像重合显示
    overlapping = cv2.addWeighted(I2gray, rate, image_output, 1 - rate, 0)
    viewImage(overlapping)
    cv2.imwrite("result.png",overlapping)


if __name__ == "__main__":
    # 读取图像
    I1gray=cv2.imread("1.png")
    I2gray=cv2.imread("2.png")
    cv2.namedWindow('Base Image', 0)
    cv2.resizeWindow('Base Image', 519, 389)  # 自己设定窗口图片的大小
    cv2.imshow('Base Image', I1gray)
    cv2.setMouseCallback('Base Image', click_event_srcI1gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.namedWindow('Target Image', 0)
    cv2.resizeWindow('Target Image', 519, 389)  # 自己设定窗口图片的大小
    cv2.imshow('Target Image', I2gray)
    cv2.setMouseCallback('Target Image', click_event_dstI2gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    homography_manual()