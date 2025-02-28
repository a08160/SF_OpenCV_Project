from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os


from app.personal_color import Color_extract  # 퍼스널 컬러 분류기
from sql_app.database import SessionLocal, engine, Base
from sql_app import models
from item_recommendation import ItemRecommendation
import sys
import os
from pathlib import Path

# 현재 디렉토리에서 sql_app 경로를 인식하도록 추가
sys.path.append(str(Path(__file__).resolve().parent / "sql_app"))


# DB 초기화
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Color_extract 인스턴스 생성
classifier = Color_extract(r'/Users/eunseo/Downloads/AURA/api/shape_predictor_68_face_landmarks.dat')


# DB 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/predict")
def predict_personal_color(file: UploadFile = File(...)):
    """
    1) 업로드된 이미지를 서버 임시 파일로 저장
    2) Color_extract로 퍼스널 컬러 예측
    3) 결과 반환
    """
    # 1) 업로드된 파일을 임시 경로로 저장
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2) 퍼스널 컬러 예측
    try:
        result = classifier.predict_personal_color(temp_filename)
        return {"success": True, "personal_color": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        # 3) 임시 파일 제거
        if os.path.exists(temp_filename):
            os.remove(temp_filename)



@app.post("/recommendations")
def get_recommendations(personal_color: str, gender: str, db: Session = Depends(get_db)):
    """
    주어진 퍼스널 컬러와 성별에 따라 추천 아이템을 반환합니다.
    """
    try:
        recommender = ItemRecommendation(personal_color, gender, db)
        recommendations = recommender.recommend_items_by_category(num_recommendations=5)
        if not any(recommendations.values()):
            raise HTTPException(status_code=404, detail="No items found for the given criteria")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during recommendation: {str(e)}")
    
    return {"success": True, "recommendations": recommendations}



@app.post("/predict-and-recommend")
def predict_and_recommend(file: UploadFile = File(...), gender: str = "여성", db: Session = Depends(get_db)):
    """
    1) 이미지를 업로드하여 퍼스널 컬러를 예측
    2) 예측된 퍼스널 컬러와 성별에 따라 추천 아이템을 반환
    3) 추천 결과를 데이터베이스에 저장
    """
    # 1) 퍼스널 컬러 예측
    prediction_result = predict_personal_color(file)
    if not prediction_result["success"]:
        return prediction_result

    personal_color = prediction_result["personal_color"]

    # 2) ItemRecommendation 클래스를 사용하여 추천 결과 생성
    recommender = ItemRecommendation(personal_color, gender, db)
    recommendations = recommender.recommend_items_by_category(num_recommendations=5)

    # 3) 추천 결과를 데이터베이스에 저장
    save_recommendations_to_db(db, {
        "personal_color": personal_color,
        "recommendations": recommendations
    })

    return {
        "success": True,
        "personal_color": personal_color,
        "recommendations": recommendations
    }


def save_recommendations_to_db(db: Session, json_data: dict):
    """
    추천 결과를 데이터베이스에 저장합니다.
    """
    personal_color = json_data.get("personal_color")
    recommendations = json_data.get("recommendations", {})

    for category, items in recommendations.items():
        for item in items:
            db_item = models.Recommendations(
                category=category,
                image_url=item["image_url"],
                item_name=item["item_name"],
                brand_name=item["brand_name"],
                personal_color=personal_color
            )
            db.add(db_item)
    db.commit()

