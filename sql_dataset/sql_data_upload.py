from sqlalchemy import create_engine
import pandas as pd

# 데이터 로드
df = pd.read_excel(r'C:/Users/SAMSUNG/Documents/code/OpenCV/Project/sql_dataset/fashion_data.xlsx')

# MySQL 연결 설정
engine = create_engine("mysql+pymysql://root:leedonggun6932*1@localhost/test_db6")

# 1) 인덱스를 컬럼으로 변환
df = df.reset_index()

# 2) 컬럼 이름을 'id'로 변경
df.rename(columns={'index': 'id'}, inplace=True)

# 데이터 업로드
df.to_sql('fashion_data', engine, if_exists='append', index=False)