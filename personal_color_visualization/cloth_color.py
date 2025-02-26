import cv2
import numpy as np

def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def remove_similar_bgr(image_path, face_lab, threshold=100):
    # 이미지 로드 및 Lab 색공간 변환
    image = cv2.imread(image_path)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    
    # 얼굴 Lab 값을 BGR로 변환
    face_bgr = np.uint8([[face_lab]])
    face_bgr = cv2.cvtColor(face_bgr, cv2.COLOR_Lab2BGR)[0][0]
    
    # BGR 색공간 변환
    diff = np.linalg.norm(image.astype(np.float32) - np.array(face_bgr, dtype=np.float32), axis=2)
    
    # 임계값(threshold) 이내인 부분을 마스크로 설정
    mask = diff < threshold
    
    # 얼굴 부분 감지
    faces = detect_face(image)
    face_mask = np.zeros_like(mask, dtype=np.uint8)
    
    for (x, y, w, h) in faces:
        face_mask[y:y+h, x:x+w] = 1
        
        # 얼굴 사각형 아래 라인 기준으로 위쪽을 삭제
        # 얼굴 사각형 아래 부분은 그대로 두고 위쪽을 삭제
        image[0:y, :] = [255, 255, 255]  # 얼굴 영역의 위쪽을 흰색으로 덮기
        image[y:y+h, :] = [255, 255, 255]  # 얼굴 영역의 위쪽을 흰색으로 덮기
    # 마스크 부분을 흰색(255, 255, 255)으로 설정하여 삭제 효과 적용
    result = image.copy()
    result[mask] = [255, 255, 255]
    
    return result

# 사용 예시
image_path = "Noukky_image/1.png"  # 전신 이미지 경로
face_lab = [121, 138, 182]  # 예제 얼굴 Lab 값
result_image = remove_similar_bgr(image_path, face_lab)

# 결과 저장 및 출력
cv2.imwrite("output.jpg", result_image)
cv2.imshow("Result", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()