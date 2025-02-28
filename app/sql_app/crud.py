from sqlalchemy.orm import Session
from . import models, schemas # 기존에 생성한 모델과 스키마 불러오기

############################ Fashion_Item ############################
def get_item(db: Session, item_id: int):
   
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item: schemas.ItemCreate):
 
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item: models.Item):
   
    db.delete(item)
    db.commit()

def get_items(db: Session, skip: int = 0, limit: int = 10):
   
    return db.query(models.Item).offset(skip).limit(limit).all()

############################ MySQL DB ############################

# def process_and_store_data(json_data: dict, db: Session):
#     results = json_data['results']

#     for result in results:
#         # Location 생성 또는 조회
#         location_name = result['intersection']
#         location = db.query(models.Location).filter(models.Location.name == location_name).first()
#         if not location:
#             location = models.Location(name=location_name)
#             db.add(location)
#             db.flush()

#         # Actual 및 Predicted 데이터 생성 및 저장
#         for date, actual, predicted in zip(result['dates'], result['actual'], result['predicted']):
#             datetime_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            
#             actual_data = models.Actual(
#                 location_id=location.id,
#                 actual_value=actual,
#                 datetime=datetime_obj
#             )
#             db.add(actual_data)

#             predicted_data = models.Predicted(
#                 location_id=location.id,
#                 predicted_value=predicted,
#                 datetime=datetime_obj
#             )
#             db.add(predicted_data)

#     db.commit()