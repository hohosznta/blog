---
title: "블로그 검색 결과 조회"
slug: "naver-api-hub-search-blog"
updated: 2026-07-23T09:04:26Z
published: 2026-07-23T09:04:26Z
canonical: "api.ncloud-docs.com/naver-api-hub-search-blog"
---

> ## Documentation Index
> Fetch the complete documentation index at: https://api.ncloud-docs.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 블로그 검색 결과 조회

Classic/VPC 환경에서 이용 가능합니다.

네이버 검색의 블로그 검색 결과를 조회합니다.

참고

블로그 검색은 검색 API를 사용하며, 검색 API의 하루 호출 한도는 25,000회입니다.

## 요청

요청 형식을 설명합니다. 요청 형식은 다음과 같습니다.

| 메서드 | URI |
| --- | --- |
| GET | /search/v1/blog |

### 요청 헤더

NAVER API HUB에서 공통으로 사용하는 헤더에 대한 정보는 [NAVER API HUB 요청 헤더](/docs/naver-api-hub-overview#%EC%9A%94%EC%B2%AD%ED%97%A4%EB%8D%94)를 참조해 주십시오.

### 요청 쿼리 파라미터

요청 쿼리 파라미터에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `query` | String | Required | 검색어 - UTF-8로 인코딩 |
| `display` | Integer | Optional | 한 번에 표시할 검색 결과 개수 - `1`~`100` (기본값: `10`) |
| `start` | Integer | Optional | 검색 시작 위치 - `1`~`1000` (기본값: `1`) |
| `sort` | String | Optional | 검색 결과 정렬 방법 - `sim` (기본값) \| `date` - `sim`: 정확도 내림차순 - `date`: 날짜 내림차순 |
| `format` | String | Optional | 응답 형식 - `json` (기본값) \| `xml` |

### 요청 예시

요청 예시는 다음과 같습니다.

```
curl --location --request GET https://naverapihub.apigw.ntruss.com/search/v1/blog?query=커피&display=2&start=1&sort=date&format=json
--header X-NCP-APIGW-API-KEY-ID: {Client ID}
--header X-NCP-APIGW-API-KEY: {Client Secret}
```

## 응답

응답 형식을 설명합니다.

### 응답 바디

응답 바디에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `lastBuildDate` | String | - | 검색 결과를 생성한 시간 |
| `total` | Integer | - | 총 검색 결과 개수 |
| `start` | Integer | - | 검색 시작 위치 |
| `display` | Integer | - | 한 번에 표시할 검색 결과 개수 |
| `items` | Array | - | 개별 검색 결과 목록: [items](/docs/naver-api-hub-search-blog#items) |

#### items

`items`에 대한 설명은 다음과 같습니다.

| 필드 | 타입 | 필수 여부 | 설명 |
| --- | --- | --- | --- |
| `title` | String | - | 블로그 포스트의 제목 - 검색어와 일치하는 부분은 `&lt;b&gt;` 태그로 감쌈 |
| `link` | String | - | 블로그 포스트의 URL |
| `description` | String | - | 블로그 포스트 내용을 요약한 패시지 정보 - 검색어와 일치하는 부분은 `&lt;b&gt;` 태그로 감쌈 |
| `bloggername` | String | - | 블로그 포스트가 있는 블로그의 이름 |
| `bloggerlink` | String | - | 블로그 포스트가 있는 블로그의 주소 |
| `postdate` | String | - | 블로그 포스트가 작성된 날짜 |

### 응답 상태 코드

응답 상태 코드에 대한 설명은 다음과 같습니다.

| HTTP 상태 코드 | 코드 | 메시지 | 설명 |
| --- | --- | --- | --- |
| 400 | `SE01` | Incorrect query request (잘못된 쿼리요청입니다.) | API 요청 URL의 프로토콜, 파라미터 등에 오류가 있는지 확인 |
| 400 | `SE02` | Invalid display value (부적절한 display 값입니다.) | `display` 값이 허용 범위인지 확인 |
| 400 | `SE03` | Invalid start value (부적절한 start 값입니다.) | `start` 값이 허용 범위인지 확인 |
| 400 | `SE04` | Invalid sort value (부적절한 sort 값입니다.) | `sort` 값에 오타가 있는지 확인 |
| 400 | `SE06` | Malformed encoding (잘못된 형식의 인코딩입니다.) | 검색어를 UTF-8로 인코딩 |
| 404 | `SE05` | Invalid search api (존재하지 않는 검색 api 입니다.) | API 요청 URL에 오타가 있는지 확인 |
| 500 | `SE99` | System Error (시스템 에러) | 서버 내부에서 오류 발생 |

참고

NAVER API HUB에서 공통으로 사용하는 응답 상태 코드에 대한 설명은 [NAVER API HUB 응답 상태 코드](/docs/naver-api-hub-overview#%EC%9D%91%EB%8B%B5%EC%83%81%ED%83%9C%EC%BD%94%EB%93%9C)를 참조해 주십시오.

### 응답 예시

응답 예시는 다음과 같습니다.

```
{
    "lastBuildDate": "Thu, 11 Jun 2026 19:14:42 +0900",
    "total": 56692992,
    "start": 1,
    "display": 2,
    "items": [
        {
            "title": "<b>커피</b> 원두 고르는 법과 홈카페 입문 팁",
            "link": "https://blog.naver.com/{blogId}/{logNo}",
            "description": "오늘은 <b>커피</b> 원두를 고르는 기준을 정리해 봤습니다. 산미와 바디감에 따라 ... ",
            "bloggername": "{블로그 이름}",
            "bloggerlink": "blog.naver.com/{blogId}",
            "postdate": "20260611"
        },
        {
            "title": "동네 <b>커피</b> 맛집 탐방 후기",
            "link": "https://blog.naver.com/{blogId}/{logNo}",
            "description": "주말에 다녀온 <b>커피</b> 전문점 후기입니다. 핸드드립과 라떼 모두 ... ",
            "bloggername": "{블로그 이름}",
            "bloggerlink": "blog.naver.com/{blogId}",
            "postdate": "20260611"
        }
    ]
}
```
