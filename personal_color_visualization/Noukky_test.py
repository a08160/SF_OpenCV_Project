# 원본 이미지에서 사람 형체만 따서 저장
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2

# U2-Net 모델 로딩
model = torch.load('u2net.pth')  # 모델 파일 경로
model.eval()

# 이미지 전처리
def preprocess_image(image_path):
    image = Image.open(image_path).convert('RGB')
    preprocess = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return preprocess(image).unsqueeze(0)

# 이미지에서 사람 형체 추출
def extract_person(image_path):
    image_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(image_tensor)
    
    # 출력은 (1, 1, 320, 320) 형상으로 나온다.
    mask = output[0, 0].cpu().numpy()
    mask = (mask > 0.5).astype(np.uint8)  # 마스크 thresholding

    # 원본 이미지를 로드하고 마스크를 이용해 배경을 제거
    original_image = cv2.imread(image_path)
    masked_image = cv2.bitwise_and(original_image, original_image, mask=mask)

    return masked_image

# 결과 이미지 보기
masked_image = extract_person('personal_color_visualization\original_image\2.png')
cv2.imshow('Extracted Person', masked_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
