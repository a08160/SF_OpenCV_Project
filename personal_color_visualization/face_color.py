import cv2
import numpy as np
import dlib
import matplotlib.pyplot as plt
import pandas as pd
class Color_extract:
    def __init__(self):
        # 얼굴 인식 모델 초기화 (dlib의 68 포인트 랜드마크 모델)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def get_facial_landmarks(self, image):
        # 얼굴 랜드마크 추출
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        for face in faces:
            landmarks = self.predictor(gray, face)
            return landmarks
        return None

    def extract_regions(self, image, shape):
        # 눈, 입술, 피부 영역을 추출
        mask_eyes = np.zeros(image.shape[:2], dtype=np.uint8)
        mask_lips = np.zeros(image.shape[:2], dtype=np.uint8)
        mask_skin = np.zeros(image.shape[:2], dtype=np.uint8)

        # 눈 영역 (인덱스 36~41)
        eyes_points = [(shape.part(i).x, shape.part(i).y) for i in range(36, 42)]
        eyes_hull = cv2.convexHull(np.array(eyes_points))
        cv2.fillConvexPoly(mask_eyes, eyes_hull, 255)

        # 입술 영역 (인덱스 48~59)
        lips_points = [(shape.part(i).x, shape.part(i).y) for i in range(48, 60)]
        lips_hull = cv2.convexHull(np.array(lips_points))
        cv2.fillConvexPoly(mask_lips, lips_hull, 255)

        # 피부 영역 (얼굴 윤곽선 기준)
        skin_points = [(shape.part(i).x, shape.part(i).y) for i in range(0, 17)]
        skin_hull = cv2.convexHull(np.array(skin_points))
        cv2.fillConvexPoly(mask_skin, skin_hull, 255)

        eyes_region = cv2.bitwise_and(image, image, mask=mask_eyes)
        lips_region = cv2.bitwise_and(image, image, mask=mask_lips)
        skin_region = cv2.bitwise_and(image, image, mask=mask_skin)

        return eyes_region, lips_region, skin_region, mask_eyes, mask_lips, mask_skin

    def get_dominant_color(self, region):
        # 해당 영역의 가장 지배적인 색상을 추출
        pixels = region.reshape(-1, 3)
        pixels = pixels[np.all(pixels != 0, axis=1)]  # 배경 제외
        if len(pixels) == 0:
            return (0, 0, 0)
        return np.mean(pixels, axis=0).astype(int)

    def calculate_area(self, mask):
        # 마스크에서 면적 계산
        return cv2.countNonZero(mask)

    def classify_main_color(self, eyes_bgr, lips_bgr, skin_bgr, eyes_area, lips_area, skin_area):
        # 면적 비율 계산
        total_area = eyes_area + lips_area + skin_area
        if total_area == 0:
            # 면적이 0인 경우를 처리하기 위해 기본 가중치를 사용
            eyes_weight = 0.3
            lips_weight = 0.2
            skin_weight = 0.5
        else:
            eyes_weight = eyes_area / total_area
            lips_weight = lips_area / total_area
            skin_weight = skin_area / total_area

        # 면적 비율을 기반으로 가중 평균
        avg_b = eyes_bgr[0] * eyes_weight + lips_bgr[0] * lips_weight + skin_bgr[0] * skin_weight
        avg_g = eyes_bgr[1] * eyes_weight + lips_bgr[1] * lips_weight + skin_bgr[1] * skin_weight
        avg_r = eyes_bgr[2] * eyes_weight + lips_bgr[2] * lips_weight + skin_bgr[2] * skin_weight

        color_1x1 = np.uint8([[[avg_b, avg_g, avg_r]]])
        lab_1x1 = cv2.cvtColor(color_1x1, cv2.COLOR_BGR2LAB)[0, 0]
        L_lab, a_lab, b_lab = lab_1x1

        return L_lab, a_lab, b_lab, skin_bgr

    def predict_personal_color(self, image_path: str) -> str:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"[ERROR] Cannot read image: {image_path}")

        shape = self.get_facial_landmarks(image)
        if shape is None:
            raise ValueError("[ERROR] No face found in image.")

        eyes_region, lips_region, skin_region, mask_eyes, mask_lips, mask_skin = self.extract_regions(image, shape)
        eyes_bgr = self.get_dominant_color(eyes_region)
        lips_bgr = self.get_dominant_color(lips_region)
        skin_bgr = self.get_dominant_color(skin_region)

        # 면적 계산
        eyes_area = self.calculate_area(mask_eyes)
        lips_area = self.calculate_area(mask_lips)
        skin_area = self.calculate_area(mask_skin)

        print(f"Eyes area: {eyes_area} pixels")
        print(f"Lips area: {lips_area} pixels")
        print(f"Skin area: {skin_area} pixels")

        L_lab, a_lab, b_lab, skin_bgr = self.classify_main_color(eyes_bgr, lips_bgr, skin_bgr, eyes_area, lips_area, skin_area)

        return L_lab, a_lab, b_lab, skin_bgr

# def visualize_lab_color(L_lab, a_lab, b_lab):
#     # Lab 값을 BGR로 변환하기 위해 먼저 numpy 배열로 변환
#     lab_1x1 = np.uint8([[[L_lab, a_lab, b_lab]]])  # Lab 색 공간에서 1x1 이미지를 만듬
#     bgr_color = cv2.cvtColor(lab_1x1, cv2.COLOR_LAB2BGR)  # Lab에서 BGR로 변환

#     # BGR에서 RGB로 변환
#     rgb_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2RGB)

#     # Matplotlib을 사용해 색상 표시
#     plt.imshow(np.ones((300, 300, 3), dtype=np.uint8) * rgb_color[0, 0])
#     plt.axis('off')  # 축 숨기기
#     plt.show()

# 예시 사용
if __name__ == "__main__":
    classifier = Color_extract()

    # DataFrame을 생성할 리스트
    results = []

    for i in range(1, 1189):
        image_path = f'Noukky_image/{i}.png'  # 분석할 이미지 경로를 입력하세요.
        try:
            L_lab, a_lab, b_lab, skin_bgr = classifier.predict_personal_color(image_path)
            print(f"Predicted L*a*b* color: L={L_lab}, a={a_lab}, b={b_lab}")
            
            # # L*a*b* 색상 시각화
            # visualize_lab_color(L_lab, a_lab, b_lab)

            # 결과를 리스트에 저장
            results.append({'image_id': i, 'face_L_lab': L_lab, 'face_a_lab': a_lab, 'face_b_lab': b_lab, 'skin_bgr':skin_bgr})

        except Exception as e:
            print(f"[ERROR] Failed to process {image_path}: {e}")
            continue  # 오류가 나면 다음 이미지로 넘어감

    # 결과를 DataFrame으로 변환
    df = pd.DataFrame(results)

    # DataFrame을 xlsx 파일로 저장
    output_file = 'lab_colors.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Results saved to {output_file}")