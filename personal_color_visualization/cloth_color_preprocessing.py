import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_dominant_color_lab(region):
    # RGB에서 Lab로 변환
    lab_region = cv2.cvtColor(region, cv2.COLOR_RGB2LAB)
    
    # 해당 영역의 가장 지배적인 색상 추출
    pixels = lab_region.reshape(-1, 3)
    pixels = pixels[np.all(pixels != 0, axis=1)]  # 배경 제외
    if len(pixels) == 0:
        return (0, 0, 0)  # 배경만 있는 경우
    
    return np.mean(pixels, axis=0).astype(int)

# 기존 Excel 파일 읽기
try:
    df = pd.read_excel('lab_colors.xlsx')
except FileNotFoundError:
    # 파일이 없으면 새로 만들기
    df = pd.DataFrame(columns=['cloth_L_lab', 'cloth_a_lab', 'cloth_b_lab'])

# 1.png부터 1188.png까지 반복
for i in range(1, 1189):
    # 이미지 로드
    image_path = f'./Cloth_image/{i}.png'
    image = cv2.imread(image_path)
    if image is None:
        print(f"Warning: {image_path} not found.")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 지배적인 색상 추출
    dominant_color_lab = get_dominant_color_lab(image)

    # Lab 값 출력
    print(f"Dominant color in Lab space for {i}.png: {dominant_color_lab}")

    # 새로운 데이터 추가
    new_data = {
        'cloth_L_lab': [dominant_color_lab[0]],
        'cloth_a_lab': [dominant_color_lab[1]],
        'cloth_b_lab': [dominant_color_lab[2]]
    }

    new_df = pd.DataFrame(new_data)

    # 기존 데이터와 새로운 데이터를 합치기
    df = pd.concat([df, new_df], ignore_index=True)

# Excel 파일에 저장
df.to_excel('lab_colors.xlsx', index=False)

# 마지막으로 저장된 데이터를 확인하는 시각화 예시
dominant_color_rgb = cv2.cvtColor(np.uint8([[dominant_color_lab]]), cv2.COLOR_LAB2RGB)[0][0]
plt.imshow([[dominant_color_rgb]])  # 색상을 화면에 표시
plt.axis('off')  # 축 없애기
plt.show()
