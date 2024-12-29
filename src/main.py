import cv2
import numpy as np

img = cv2.imread('../resources/number_card.jpg')
points = []
drawing = False
POINT_COLOR = (255, 0, 0)
POINT_RADIUS = 5
LINE_COLOR = (255, 0, 0)
LINE_THICKNESS = 3
WIDTH = 480
HEIGHT = 640


def mouse_handler(event, x, y, flags, param):
    global drawing
    img_copy = img.copy()

    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 클릭 -> 점 생성
        points.append((x, y))
        drawing = True
    elif event == cv2.EVENT_RBUTTONDOWN:  # 오른쪽 클릭 -> 가장 가까운 점 제거
        if len(points) > 0: # 에러 방지를 위해, 생성한 점이 있는지 확인
            # 마우스 클릭 위치와 각 점들 간의 거리 계산
            distances = [((px - x)**2 + (py - y)**2) ** 0.5 for px, py in points]
            min_distance_idx = np.argmin(distances)  # 가장 가까운 점의 인덱스
            points.pop(min_distance_idx)  # 마우스 위치와 가장 가까운 점 제거
        else:
            drawing = False

    # 그리는 중이라면, 기존에 찍었던 점들과, 그 점들을 이은 선부터 그리기
    if drawing:
        prev_point = None
        for point in points:
            cv2.circle(img_copy, point, POINT_RADIUS, POINT_COLOR, cv2.FILLED)
            if prev_point is not None:
                cv2.line(img_copy, prev_point, point, LINE_COLOR, LINE_THICKNESS)
            prev_point = point

        next_point = (x, y)

        if len(points) == 4:
            next_point = points[0]
            show_result()

        cv2.line(img_copy, prev_point, next_point, LINE_COLOR, LINE_THICKNESS)  # 다음 그릴 선의 위치 표시

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
