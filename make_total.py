import pandas as pd

# CSV 파일 불러오기 (header=[0, 1] 두 번째 행을 사용하여 컬럼 이름으로 설정)
df = pd.read_csv("군·구별_총인구_및_구성비_20241223163725.csv", encoding="euc-kr", header=[0, 1])

# 데이터 확인
print(df.columns)

new_columns = []
years = range(2015, 2025)  # 2015부터 2024까지
for year in years:
    new_columns.append(f'{year}_인구')
    new_columns.append(f'{year}_구성비')

# 새 컬럼 이름을 df에 할당하기 전에, 컬럼 수가 맞는지 확인
print(f"새 컬럼 이름 수: {len(new_columns)}, 원본 컬럼 수: {len(df.columns)}")

# 컬럼 수가 맞다면, 컬럼을 새로 지정
if len(new_columns) == len(df.columns):
    df.columns = new_columns
else:
    print("컬럼 수가 일치하지 않습니다.")

# '행정구역'을 인덱스로 설정
df.set_index(df.columns[0], inplace=True)

# '합계'와 '군', '구'를 제외하고 필터링
df = df[df.index.str.contains("구|군")]

# 결과 출력
print(df.head())

# 전처리된 데이터 출력
df_transformed = df.T

# 결과 확인
print(df_transformed)

# CSV로 저장
df_transformed.to_csv("total.csv", encoding="euc-kr")
