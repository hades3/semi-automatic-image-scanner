import cv2
import numpy as np

img = cv2.imread('../resources/number_card.jpg')
points = []
POINT_COLOR = (255, 0, 0)
POINT_RADIUS = 5
WIDTH = 480
HEIGHT = 640


def mouse_handler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 클릭 -> 점 생성
        points.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:  # 오른쪽 클릭 -> 가장 가까운 점 제거
        if len(points) > 0: # 에러 방지를 위해, 생성한 점이 있는지 확인
            # 마우스 클릭 위치와 각 점들 간의 거리 계산
            distances = [((px - x)**2 + (py - y)**2) ** 0.5 for px, py in points]
            min_distance_idx = np.argmin(distances)  # 가장 가까운 점의 인덱스
            points.pop(min_distance_idx)  # 마우스 위치와 가장 가까운 점 제거

    img_copy = img.copy()
    for point in points:
        cv2.circle(img_copy, point, POINT_RADIUS, POINT_COLOR, cv2.FILLED)

    if len(points) == 4:
        show_result()
        points.clear()
        return

    cv2.imshow('img', img_copy)


def show_result():
    src = np.float32(points)
    dst = np.float32(np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]]))

    matrix = cv2.getPerspectiveTransform(src, dst)  # 변환행렬
    result = cv2.warpPerspective(img, matrix, (WIDTH, HEIGHT))
    cv2.imshow('result', result)


cv2.namedWindow('img')
cv2.setMouseCallback('img', mouse_handler)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
