# Titanic Service API - Swagger 문서 가이드

## 📚 Swagger UI 접근 방법

서버 실행 후 다음 URL로 접근할 수 있습니다:

### 1. Swagger UI (대화형 API 문서)
```
http://localhost:9010/docs
```

### 2. ReDoc (다른 스타일의 API 문서)
```
http://localhost:9010/redoc
```

### 3. OpenAPI JSON Schema
```
http://localhost:9010/openapi.json
```

## 🚀 서버 실행 방법

### Docker로 실행
```bash
cd C:\Users\hi\Documents\250930-hague-spring-fast-next\labzang.com
docker compose --profile ai up mlservice
```

### 로컬에서 실행
```bash
cd ai.labzang.com/mlservice
pip install -r requirements.txt
python -m app.main
```

## 📋 API 엔드포인트 목록

### 기본 엔드포인트
- `GET /` - 서비스 정보
- `GET /passengers/top10` - 상위 10명 승객 정보
- `GET /passengers/top10/print` - 상위 10명 승객 정보 터미널 출력

### 타이타닉 서비스 엔드포인트 (`/titanic`)
- `GET /titanic/` - 타이타닉 서비스 루트
- `GET /titanic/health` - 헬스 체크
- `GET /titanic/passengers` - 승객 목록 조회
- `GET /titanic/statistics` - 데이터 통계 정보
- `GET /titanic/model/status` - 모델 훈련 상태 확인
- `POST /titanic/train` - 머신러닝 모델 훈련
- `POST /titanic/predict` - 승객 생존 예측
- `POST /titanic/predict-batch` - 배치 예측

## 💡 Swagger UI 사용 방법

1. **서버 실행 확인**
   ```bash
   curl http://localhost:9010/
   ```

2. **브라우저에서 Swagger UI 열기**
   - `http://localhost:9010/docs` 접속

3. **API 테스트**
   - 각 엔드포인트를 클릭하여 상세 정보 확인
   - "Try it out" 버튼 클릭
   - 필요한 파라미터 입력
   - "Execute" 버튼으로 API 호출
   - 응답 결과 확인

## 📝 API 사용 예시

### 1. 승객 목록 조회
```bash
curl -X GET "http://localhost:9010/titanic/passengers?limit=5"
```

### 2. 통계 정보 조회
```bash
curl -X GET "http://localhost:9010/titanic/statistics"
```

### 3. 모델 훈련
```bash
curl -X POST "http://localhost:9010/titanic/train" \
  -H "Content-Type: application/json" \
  -d '{
    "test_size": 0.2,
    "random_state": 42,
    "n_estimators": 100
  }'
```

### 4. 생존 예측
```bash
curl -X POST "http://localhost:9010/titanic/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Pclass": 1,
    "Sex": "female",
    "Age": 25,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 71.28,
    "Embarked": "C"
  }'
```

## 🎯 Swagger UI 주요 기능

1. **인터랙티브 테스트**: 브라우저에서 직접 API 호출 가능
2. **자동 문서화**: 코드에서 자동으로 API 문서 생성
3. **스키마 검증**: 요청/응답 스키마 자동 검증
4. **예제 요청**: 각 엔드포인트별 예제 제공

## 📖 추가 정보

- FastAPI는 OpenAPI 3.0 표준을 따릅니다
- 모든 엔드포인트는 자동으로 Swagger 문서에 포함됩니다
- Pydantic 모델을 사용하면 자동으로 스키마가 생성됩니다

