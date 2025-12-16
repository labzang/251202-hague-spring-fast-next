# Titanic Service API - Postman 테스트 가이드

## 📦 Postman Collection 가져오기

### 방법 1: JSON 파일로 가져오기

1. Postman 실행
2. **Import** 버튼 클릭
3. `Titanic_Service_API.postman_collection.json` 파일 선택
4. Import 클릭

### 방법 2: OpenAPI로 가져오기

1. 서버 실행 후 다음 URL에서 OpenAPI 스키마 다운로드:
   ```
   http://localhost:9010/openapi.json
   ```
2. Postman에서 **Import** → **Link** 선택
3. URL 입력: `http://localhost:9010/openapi.json`
4. Import 클릭

## 🚀 서버 실행

테스트 전에 서버를 실행해야 합니다:

```bash
# Docker로 실행
cd C:\Users\hi\Documents\250930-hague-spring-fast-next\labzang.com
docker compose --profile ai up mlservice

# 또는 로컬에서 실행
cd ai.labzang.com/mlservice
python -m app.main
```

서버가 실행되면 다음 URL에서 확인할 수 있습니다:
- Base URL: `http://localhost:9010`

## 📋 API 엔드포인트 테스트 가이드

### 1. 기본 엔드포인트

#### 서비스 정보
```
GET http://localhost:9010/
```

**Postman 설정:**
- Method: `GET`
- URL: `http://localhost:9010/`
- Headers: 없음

**예상 응답:**
```json
{
  "service": "mlservice",
  "version": "1.0.0",
  "message": "Titanic Service API"
}
```

#### 상위 10명 승객 정보
```
GET http://localhost:9010/passengers/top10
```

**Postman 설정:**
- Method: `GET`
- URL: `http://localhost:9010/passengers/top10`
- Headers: 없음

### 2. 타이타닉 서비스 엔드포인트

#### 2.1 서비스 루트
```
GET http://localhost:9010/titanic/
```

**Postman 설정:**
- Method: `GET`
- URL: `http://localhost:9010/titanic/`

#### 2.2 헬스 체크
```
GET http://localhost:9010/titanic/health
```

**Postman 설정:**
- Method: `GET`
- URL: `http://localhost:9010/titanic/health`

**예상 응답:**
```json
{
  "status": "success",
  "message": "Titanic service is healthy",
  "data": {
    "status": "healthy",
    "service": "titanic"
  }
}
```

#### 2.3 승객 목록 조회
```
GET http://localhost:9010/titanic/passengers?limit=10
```

**Postman 설정:**
- Method: `GET`
- URL: `http://localhost:9010/titanic/passengers`
- Params 탭:
  - Key: `limit`
  - Value: `10` (1-100 사이의 값)

**예제:**
- `limit=5` → 5명의 승객 조회
- `limit=20` → 20명의 승객 조회

#### 2.4 데이터 통계
```
GET http://localhost:9010/titanic/statistics
```

**Postman 설정:**
- Method: `GET`
- URL: `http://localhost:9010/titanic/statistics`

**예상 응답 예시:**
```json
{
  "status": "success",
  "message": "Successfully retrieved statistics",
  "data": {
    "total_passengers": 891,
    "survived_count": 342,
    "survival_rate": 0.3838383838383838,
    "average_age": 29.69911764705882,
    "average_fare": 32.204207968574636
  }
}
```

#### 2.5 모델 상태 확인
```
GET http://localhost:9010/titanic/model/status
```

**Postman 설정:**
- Method: `GET`
- URL: `http://localhost:9010/titanic/model/status`

**예상 응답 (훈련 전):**
```json
{
  "status": "success",
  "message": "Model status retrieved successfully",
  "data": {
    "is_trained": false,
    "has_scaler": false,
    "has_label_encoders": false
  }
}
```

#### 2.6 모델 훈련
```
POST http://localhost:9010/titanic/train
```

**Postman 설정:**
- Method: `POST`
- URL: `http://localhost:9010/titanic/train`
- Headers:
  - Key: `Content-Type`
  - Value: `application/json`
- Body 탭 → raw → JSON 선택:
```json
{
  "test_size": 0.2,
  "random_state": 42,
  "n_estimators": 100
}
```

**파라미터 설명:**
- `test_size`: 테스트 데이터 비율 (0.1 ~ 0.5)
- `random_state`: 랜덤 시드 (재현 가능한 결과를 위해)
- `n_estimators`: 랜덤 포레스트 트리 개수 (10 ~ 1000)

**예상 응답:**
```json
{
  "status": "success",
  "message": "Model trained successfully with accuracy: 0.8324",
  "data": {
    "accuracy": 0.8324,
    "classification_report": {...},
    "confusion_matrix": [[...], [...]],
    "feature_importance": {...}
  }
}
```

**⏱️ 주의:** 모델 훈련은 시간이 걸릴 수 있습니다 (몇 초 ~ 수십 초).

#### 2.7 생존 예측 (단일)
```
POST http://localhost:9010/titanic/predict
```

**⚠️ 중요:** 모델을 먼저 훈련해야 합니다! (`/titanic/train` 호출)

**Postman 설정:**
- Method: `POST`
- URL: `http://localhost:9010/titanic/predict`
- Headers:
  - Key: `Content-Type`
  - Value: `application/json`
- Body 탭 → raw → JSON 선택:
```json
{
  "Pclass": 1,
  "Sex": "female",
  "Age": 25,
  "SibSp": 0,
  "Parch": 0,
  "Fare": 71.28,
  "Embarked": "C"
}
```

**필수 필드:**
- `Pclass`: 승선 등급 (1, 2, 3)
- `Sex`: 성별 (`male` 또는 `female`)
- `Age`: 나이 (숫자)
- `SibSp`: 형제/자매/배우자 수 (0 이상)
- `Parch`: 부모/자식 수 (0 이상)
- `Fare`: 요금 (0 이상의 숫자)
- `Embarked`: 승선 항구 (`C`, `Q`, `S`)

**예상 응답:**
```json
{
  "status": "success",
  "message": "Prediction completed. Survived: 1",
  "data": {
    "survived": 1,
    "survival_probability": 0.85,
    "death_probability": 0.15
  }
}
```

**다양한 예시:**

1. **생존 가능성이 높은 승객:**
```json
{
  "Pclass": 1,
  "Sex": "female",
  "Age": 25,
  "SibSp": 0,
  "Parch": 0,
  "Fare": 100.0,
  "Embarked": "C"
}
```

2. **생존 가능성이 낮은 승객:**
```json
{
  "Pclass": 3,
  "Sex": "male",
  "Age": 30,
  "SibSp": 0,
  "Parch": 0,
  "Fare": 7.25,
  "Embarked": "S"
}
```

#### 2.8 생존 예측 (배치)
```
POST http://localhost:9010/titanic/predict-batch
```

**⚠️ 중요:** 모델을 먼저 훈련해야 합니다!

**Postman 설정:**
- Method: `POST`
- URL: `http://localhost:9010/titanic/predict-batch`
- Headers:
  - Key: `Content-Type`
  - Value: `application/json`
- Body 탭 → raw → JSON 선택:
```json
[
  {
    "Pclass": 1,
    "Sex": "female",
    "Age": 25,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 71.28,
    "Embarked": "C"
  },
  {
    "Pclass": 3,
    "Sex": "male",
    "Age": 22,
    "SibSp": 1,
    "Parch": 0,
    "Fare": 7.25,
    "Embarked": "S"
  },
  {
    "Pclass": 2,
    "Sex": "female",
    "Age": 30,
    "SibSp": 1,
    "Parch": 1,
    "Fare": 20.0,
    "Embarked": "Q"
  }
]
```

**예상 응답:**
```json
{
  "status": "success",
  "message": "Batch prediction completed for 3 passengers",
  "data": {
    "predictions": [
      {
        "passenger_data": {...},
        "prediction": {
          "survived": 1,
          "survival_probability": 0.85,
          "death_probability": 0.15
        }
      },
      ...
    ],
    "count": 3
  }
}
```

## 🔄 테스트 시나리오

### 시나리오 1: 전체 워크플로우

1. **서비스 확인**
   ```
   GET /titanic/health
   ```

2. **데이터 확인**
   ```
   GET /titanic/passengers?limit=5
   GET /titanic/statistics
   ```

3. **모델 훈련**
   ```
   POST /titanic/train
   ```

4. **모델 상태 확인**
   ```
   GET /titanic/model/status
   ```
   → `is_trained: true` 확인

5. **생존 예측**
   ```
   POST /titanic/predict
   ```

### 시나리오 2: 빠른 테스트

1. 모델 훈련: `POST /titanic/train`
2. 예측: `POST /titanic/predict`

## 🐛 문제 해결

### 에러: "Model not trained"
**원인:** 모델이 훈련되지 않음
**해결:** 먼저 `POST /titanic/train` 호출

### 에러: "Service unhealthy"
**원인:** CSV 파일을 찾을 수 없음
**해결:** 서버 로그 확인, CSV 파일 경로 확인

### 에러: "Failed to predict"
**원인:** 필수 필드 누락 또는 잘못된 데이터 형식
**해결:** 요청 Body의 JSON 형식 확인

## 📝 Postman 환경 변수 설정 (선택사항)

Postman에서 환경 변수를 설정하면 URL을 쉽게 변경할 수 있습니다:

1. Postman에서 **Environments** 클릭
2. **+** 버튼으로 새 환경 생성
3. 변수 추가:
   - Variable: `base_url`
   - Initial Value: `http://localhost:9010`
   - Current Value: `http://localhost:9010`
4. 환경 선택 후 URL에서 `{{base_url}}` 사용:
   - 예: `{{base_url}}/titanic/health`

## 🎯 유용한 팁

1. **Pre-request Script 사용:**
   - 모델 훈련 후 자동으로 상태 확인

2. **Tests Script 사용:**
   - 응답 상태 코드 검증
   - 응답 시간 측정

3. **Collection Runner:**
   - 여러 요청을 순차적으로 실행

4. **변수 사용:**
   - 예측 결과를 변수에 저장하여 재사용

## 📚 추가 리소스

- Swagger UI: `http://localhost:9010/docs`
- ReDoc: `http://localhost:9010/redoc`
- OpenAPI Schema: `http://localhost:9010/openapi.json`


