import pandas as pd

# CSV 파일 읽기
df = pd.read_csv("군·구별_남녀_인구_및_성비_20241223163828.csv", encoding="euc-kr")

df.columns = df.iloc[0]
df = df.drop(0)

# 첫 번째 열을 인덱스로 설정
df.set_index(df.columns[0], inplace=True)

# 연도별로 '남', '여', '성비' 항목을 '남_연도', '여_연도', '성비_연도' 형태로 변환
years = range(2015, 2025)  # 2015-2024년 데이터
columns = ['남 (명)', '여 (명)', '성비 (여자1백명당 명)']  

# 새로운 열 이름을 생성
new_columns = []
for year in years:
    new_columns.append(f'남_{year}')
    new_columns.append(f'여_{year}')
    new_columns.append(f'성비_{year}')

# 열 이름이 새로운 형식과 일치하는지 확인 후 변경
if len(df.columns) == len(new_columns):
    df.columns = new_columns
else:
    print(f"열 이름의 개수가 일치하지 않습니다. 기존 열 개수: {len(df.columns)}, 생성된 열 이름 개수: {len(new_columns)}")

# 데이터프레임 확인
print(df.head())

# CSV로 저장
df.to_csv("gender.csv", encoding="euc-kr")
