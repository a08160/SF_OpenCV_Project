# 누끼 이미지에서 얼굴만 분리

import cv2
import os

# 감지기 불러오기
cascade1 = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")
cascade2 = cv2.CascadeClassifier(cv2.data.haarcascade + "haarcascade_fullbody.xml")

# 이미지 로드
image_path = "Noukky_image/1.png"  # 사용할 이미지 경로
image = cv2.imread(image_path)

if image is None:
    print("이미지를 불러올 수 없습니다.")
else:
    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 얼굴 감지
    faces = cascade1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    bodies = cascade2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

    output_dir1 = "face_image"  # 얼굴 저장할 폴더 이름
    output_dir2 = "body_image"  # 몸 저장할 폴더 이름

    # 얼굴만 잘라서 저장
    for i, (x, y, w, h) in enumerate(faces):
        face = image[y:y+h, x:x+w]  # 얼굴 영역 자르기
        face_filename = os.path.join(output_dir1, f"{i+1}.png")
        cv2.imwrite(face_filename, face)  # 얼굴 저장
        print(f"얼굴 {i+1} 저장 완료: {face_filename}")
    
    for i, (x, y, w, h) in enumerate(bodies):
        body = image[y:y+h, x:x+w]
        body_filename = os.path.join(output_dir2, f"{i+1}.png")
        cv2.imwrite(body_filename, body) # 몸 저장
        print(f"몸 {i+1} 저장 완료: {body_filename}")