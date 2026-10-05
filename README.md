# 네이버 블로그 자동화

실제 방문 후기와 사진을 바탕으로 검색 자료를 조사하고, 블로그 초안과 썸네일을 준비하는 로컬 작업 자료입니다.

현재 저장소에는 작성 프롬프트, 워크플로우 설계, 주제별 NAVER API HUB 자료 수집 코드와 썸네일 자료가 포함됩니다. 전체 워크플로우를 한 번에 실행하는 프로그램이나 자동 발행 기능은 아직 포함되어 있지 않습니다. GitHub Actions는 사용하지 않습니다.

## 구성

| 파일 | 용도 |
| --- | --- |
| `AGENTS.md` | 블로그 작업 전에 워크플로우 전체를 읽도록 하는 에이전트 지침 |
| `naver-blog-prompt.md` | 글 작성 규칙과 프롬프트 |
| `blog-workflow-plan.md` | 조사·기획·집필·검수·발행 준비 설계 |
| `naver-blog-api-guide.md` | 블로그 검색 API 참고 자료 |
| `naver-search-trend.md` | 검색 트렌드 API 참고 자료 |
| `<주제>/research/*.py` | 주제별 검색 결과·트렌드 수집 |
| `썸네일/template.css` | 썸네일 디자인 자료 |
| `을지로자야/thumbnail/render.py` | 기존 썸네일 렌더링 예제 |
| `<주제>/thumbnail/prompt*.txt` | 썸네일 생성 프롬프트 |

## 검색 자료 수집

Python 3.9 이상이 필요합니다. 검색 자료 수집 코드는 Python 표준 라이브러리만 사용합니다.

```bash
git clone https://github.com/hohosznta/blog.git
cd blog
cp .env.example .env
```

`.env`에 본인의 NAVER API HUB 인증 값을 입력합니다.

```dotenv
NAVER_CLIENT_KEY=발급받은_클라이언트_키
NAVER_SECRET=발급받은_시크릿
```

실제 `.env`는 Git에서 제외됩니다. 키는 커밋하거나 README에 붙여 넣지 않습니다.

주제에 맞는 수집 스크립트를 실행합니다.

```bash
python3 문래갈매기/research/collect.py
```

결과는 해당 `research/` 폴더에 JSON으로 저장됩니다. 기존 스크립트는 당시 조사에 사용한 검색어와 날짜를 코드에 고정해 두었습니다. 새 조사를 할 때는 실행 전 `queries`, 검색어 그룹, 조회 시작·종료 날짜를 확인하고 수정하세요. 스크립트에 따라 변수 이름과 출력 파일 이름은 다릅니다. API 사용에는 본인의 API 이용 설정이 필요합니다.

## 글 작성

Codex에서는 이 저장소 폴더를 프로젝트로 열어 작업하세요. 루트의 `AGENTS.md`에 블로그 기획·집필·수정·검수 전에 `blog-workflow-plan.md` 전체를 읽도록 명시되어 있습니다. 파일을 읽을 수 없으면 집필을 시작하지 않도록 정했습니다. `AGENTS.md`를 자동으로 읽지 않는 AI 도구에는 이 지침과 워크플로우 문서를 직접 제공해야 합니다.

1. 주제 폴더에 실제 경험을 기록한 `후기.md`와 사진을 로컬로 준비합니다.
2. 수집한 검색 결과와 트렌드를 참고해 답할 질문과 근거를 정리합니다.
3. `naver-blog-prompt.md`를 AI 작성 도구에 전달하고 원문 경험과 확인된 자료를 함께 제공합니다.
4. 초안의 사실·가격·날짜·사진 배치를 검수한 뒤 네이버 블로그에 직접 발행합니다.

상세 단계와 개선 계획은 `blog-workflow-plan.md`를 참고하세요. 설계 문서의 모든 단계가 코드로 구현된 것은 아닙니다.

## 썸네일 예제

썸네일 렌더링 예제에만 추가 패키지가 필요합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-thumbnail.txt
```

현재 `을지로자야/thumbnail/render.py`는 작성자의 macOS 환경에 맞춰져 있습니다. 실행하려면 다음 준비가 필요합니다.

- 로컬 Google Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Pretendard Bold·Medium·SemiBold OTF 폰트: 코드의 `fontroot`를 본인 폰트 폴더로 수정
- 배경 사진: `을지로자야/thumbnail/source.jpg`

```bash
python3 을지로자야/thumbnail/render.py
```

HTML, 썸네일 이미지와 렌더링 검사 JSON은 같은 폴더에 생성됩니다. 다른 주제로 사용할 때는 코드의 문구와 출력 이름도 수정하세요.

## 저장소에 포함하지 않는 자료

사진·영상, 방문 후기 원문, 완성된 글, API 응답, 수집한 외부 페이지, 인증 키와 생성 결과는 로컬에 보관합니다. `.gitignore`는 자동화 소스와 재사용 문서만 추적하도록 설정되어 있습니다. 새 파일 유형을 공유하려면 `.gitignore`에 허용 규칙을 추가하세요.
