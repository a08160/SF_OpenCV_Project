import cv2
import numpy as np
import pandas as pd

def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def remove_similar_bgr(image_path, face_lab, threshold=100):
    # 이미지 로드 및 Lab 색공간 변환
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # BGRA 지원
    if image is None:
        return None

    if image.shape[2] == 3:  # Alpha 채널이 없는 경우 추가
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    lab_image = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2Lab)  # BGR만 변환
    
    # 얼굴 Lab 값을 BGR로 변환
    face_bgr = np.uint8([[face_lab]])
    face_bgr = cv2.cvtColor(face_bgr, cv2.COLOR_Lab2BGR)[0][0]
    
    # BGR 색공간 차이 계산
    diff = np.linalg.norm(image[:, :, :3].astype(np.float32) - np.array(face_bgr, dtype=np.float32), axis=2)
    
    # 임계값(threshold) 이내인 부분을 마스크로 설정
    mask = diff < threshold
    
    # 얼굴 부분 감지
    faces = detect_face(image[:, :, :3])
    face_mask = np.zeros(mask.shape, dtype=np.uint8)
    
    for (x, y, w, h) in faces:
        face_mask[y:y+h, x:x+w] = 1
        
        # 얼굴 사각형 아래 라인 기준으로 위쪽을 투명하게 설정
        image[:y+h, :, 3] = 0  # 얼굴 위쪽 부분을 투명하게 처리

    # 마스크 부분을 투명하게 설정
    result = image.copy()
    result[mask, 3] = 0  # 얼굴 색과 유사한 부분을 투명하게 변경
    
    return result

df = pd.read_excel("lab_colors.xlsx")
df["skin_bgr"] = df["skin_bgr"].apply(lambda x: np.array(list(map(int, x.strip('[]').split())), dtype=np.uint8))

# 사용 예시
for i in range(1, 6):
    image_path = f"Noukky_image/{i}.png"  # 전신 이미지 경로
    face_lab = df["skin_bgr"][i-1]  # 얼굴 Lab 값
    result_image = remove_similar_bgr(image_path, face_lab)

    if result_image is not None:
        cv2.imwrite(f"./Cloth_image/{i}.png", result_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])  # PNG로 저장 (투명도 유지)
