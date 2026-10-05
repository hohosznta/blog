---
title: "검색어 트렌드 조회"
slug: "naver-api-hub-search-trend"
updated: 2026-07-23T09:04:26Z
published: 2026-07-23T09:04:26Z
canonical: "api.ncloud-docs.com/naver-api-hub-search-trend"
---

> ## Documentation Index
> Fetch the complete documentation index at: https://api.ncloud-docs.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 검색어 트렌드 조회

Classic/VPC 환경에서 이용 가능합니다.

검색어 트렌드 API는 [네이버 데이터랩](https://datalab.naver.com/)의 [검색어트렌드](https://datalab.naver.com/keyword/trendSearch.naver)를 조회하는 RESTful API입니다. 주제어로 묶은 검색어에 대한 네이버 통합검색의 검색 추이 데이터를 확인할 수 있습니다.

## 요청

요청 형식을 설명합니다. 요청 형식은 다음과 같습니다.

| 메서드 | URI |
| --- | --- |
| POST | /search-trend/v1/search |

### 요청 헤더

NAVER API HUB에서 공통으로 사용하는 헤더에 대한 정보는 [NAVER API HUB 요청 헤더](/docs/naver-api-hub-overview#%EC%9A%94%EC%B2%AD%ED%97%A4%EB%8D%94)를 참조해 주십시오.

### 요청 바디

요청 바디에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `startDate` | String | Required | 조회 기간 시작 날짜 (`yyyy-mm-dd`) - 2016년 1월 1일부터 조회 가능 |
| `endDate` | String | Required | 조회 기간 종료 날짜 (`yyyy-mm-dd`) |
| `timeUnit` | String | Required | 구간 단위 - `date` \| `week` \| `month` - `date`: 일간 - `week`: 주간 - `month`: 월간 |
| `keywordGroups` | Array | Required | 주제어와 주제어에 해당하는 검색어 묶음 쌍의 배열: [keywordGroups](/docs/naver-api-hub-search-trend#keywordGroups) - 최대 5개의 쌍 설정 가능 |
| `device` | String | Optional | 검색 기기 - `pc` \| `mo` - `pc`: PC에서 검색 추이 - `mo`: 모바일에서 검색 추이 - 기본값: 모든 환경 |
| `gender` | String | Optional | 검색 사용자의 성별 - `m` \| `f` - `m`: 남성 - `f`: 여성 - 기본값: 모든 성별 |
| `ages` | Array | Optional | 검색 사용자의 연령 - `1` \| `2` \| `3` \| `4` \| `5` \| `6` \| `7` \| `8` \| `9` \| `10` \| `11` - `1`: 0∼12세 - `2`: 13∼18세 - `3`: 19∼24세 - `4`: 25∼29세 - `5`: 30∼34세 - `6`: 35∼39세 - `7`: 40∼44세 - `8`: 45∼49세 - `9`: 50∼54세 - `10`: 55∼59세 - `11`: 60세 이상 - 기본값: 모든 연령 |

#### keywordGroups

`keywordGroups`에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `groupName` | String | Required | 주제어 - 검색어 묶음을 대표하는 이름 |
| `keywords` | Array | Required | 주제어에 해당하는 검색어 - 최대 20개의 검색어 설정 가능 |

### 요청 예시

요청 예시는 다음과 같습니다.

```
curl --location --request POST https://naverapihub.apigw.ntruss.com/search-trend/v1/search
--header X-NCP-APIGW-API-KEY-ID: {Client ID}
--header X-NCP-APIGW-API-KEY: {Client Secret}
--header Content-Type: application/json
--data '{
    "startDate": "2023-01-01",
    "endDate": "2023-06-30",
    "timeUnit": "month",
    "keywordGroups": [
        { "groupName": "한글", "keywords": ["한글", "korean"] },
        { "groupName": "영어", "keywords": ["영어", "english"] }
    ],
    "device": "pc",
    "gender": "f",
    "ages": ["3", "4", "5", "6", "7", "8", "9", "10", "11"]
}'
```

## 응답

응답 형식을 설명합니다.

### 응답 바디

응답 바디에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `startDate` | String | - | 조회 기간 시작 날짜 (`yyyy-mm-dd`) |
| `endDate` | String | - | 조회 기간 종료 날짜 (`yyyy-mm-dd`) |
| `timeUnit` | String | - | 구간 단위 |
| `results` | Array | - | 조회 결과 목록: [results](/docs/naver-api-hub-search-trend#results) |

#### results

`results`에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `title` | String | - | 주제어 |
| `keywords` | Array | - | 주제어에 해당하는 검색어 |
| `data` | Array | - | 구간별 검색 추이 데이터: [data](/docs/naver-api-hub-search-trend#data) |

#### data

`data`에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `period` | String | - | 구간별 시작 날짜 (`yyyy-mm-dd`) |
| `ratio` | Number | - | 구간별 검색량의 상대적 비율 - 구간별 결과에서 가장 큰 값을 100으로 설정한 상댓값 |

### 응답 상태 코드

NAVER API HUB에서 공통으로 사용하는 응답 상태 코드에 대한 설명은 [NAVER API HUB 응답 상태 코드](/docs/naver-api-hub-overview#%EC%9D%91%EB%8B%B5%EC%83%81%ED%83%9C%EC%BD%94%EB%93%9C)를 참조해 주십시오.

### 응답 예시

응답 예시는 다음과 같습니다.

```
{
    "startDate": "2023-01-01",
    "endDate": "2023-06-30",
    "timeUnit": "month",
    "results": [
        {
            "title": "한글",
            "keywords": [
                "한글",
                "korean"
            ],
            "data": [
                {
                    "period": "2023-01-01",
                    "ratio": 70.15342
                },
                {
                    "period": "2023-02-01",
                    "ratio": 74.21207
                },
                {
                    "period": "2023-03-01",
                    "ratio": 100
                },
                {
                    "period": "2023-04-01",
                    "ratio": 84.46829
                }
            ]
        },
        {
            "title": "영어",
            "keywords": [
                "영어",
                "english"
            ],
            "data": [
                {
                    "period": "2023-01-01",
                    "ratio": 26.67976
                },
                {
                    "period": "2023-02-01",
                    "ratio": 25.81815
                },
                {
                    "period": "2023-03-01",
                    "ratio": 29.68029
                },
                {
                    "period": "2023-04-01",
                    "ratio": 27.57161
                }
            ]
        }
    ]
}
```
