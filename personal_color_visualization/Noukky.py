# 원본 이미지에서 사람 형체만 따서 저장
from rembg import remove
from PIL import Image

def remove_background(input_file, output_file, params = None):
    """
        inputfile: 변환할 이미지의 파일 경로
        outputfile: 배경제거 후 저장될 파일 경로
    """

    # 이미지 로드
    img = Image.open(input_file)

    # 배경 제거
    if params is None:
        out = remove(img) # 기본 옵션
    else:
        out = remove(data = img, **params) # 파라미터 저장
    
    # 저장
    out.save(output_file)
for i in range(405,1189):
    remove_background(f"original_image/{i}.png", f"Noukky_image/{i}.png")