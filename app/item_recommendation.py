from sqlalchemy.orm import Session
from sqlalchemy import text
import random


class ItemRecommendation:
    def __init__(self, personal_color: str, gender: str, db: Session):
        self.personal_color = personal_color
        self.gender = gender
        self.db = db
        self.recommendations = {
            '상의': [],
            '하의': [],
        }

    def recommend_items_by_category(self, num_recommendations=5):
        for category in self.recommendations.keys():
            # SQL 쿼리 수정: 필요한 컬럼 추가
            sql_query = text("""
                SELECT 이미지링크, 상품명, 브랜드명
                FROM fashion_data
                WHERE personal_color = :personal_color
                  AND 성별 = :gender
                  AND 대분류 = :category
            """)

            # 쿼리 실행
            result = self.db.execute(sql_query, {
                'personal_color': self.personal_color,
                'gender': self.gender,
                'category': category
            }).fetchall()

            # 결과에서 필요한 데이터를 추출
            items = [
                {
                    'image_url': row[0],
                    'item_name': row[1],
                    'brand_name': row[2]
                }
                for row in result
            ]

            # 랜덤 추천
            if items:
                random_items = random.sample(
                    items,
                    min(len(items), num_recommendations)
                )
                self.recommendations[category] = random_items

        return self.recommendations
