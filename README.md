# pyoniverse-api

## 배포 방법

**chalice deploy 를 이용해 배포합니다.**

### 1. 최초 배포

1. `python deploy.py --stage={stage_name}`

### 2. 배포 업데이트

1. `python deploy.py --stage={stage_name}`

### 3. 별도 스테이지 배포(한 게이트웨이 고정방법)

Chalice 는 기본적으로 배포 시, Stage 마다 새로운 게이트웨이를 생성합니다.
이것을 방지하기 위해 `.chalice/deployed` 파일을 수정합니다.

1. 다른 스테이지에 대해 `1. 최초 배포` 수행
2. `.chalice/deployed/{stage_name}.json` 의 `rest_api_id` `rest_api_url` 을 다른 스테이지와 동일하게 바꾸기
3. `2. 배포 업데이트` 수행

PS) 다른 스테이지에서 `rest_api_url`의 마지막 `/{stage_name}` 은 변경해야 합니다.
