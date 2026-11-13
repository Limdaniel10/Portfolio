# Chaehyun Lim — 통합 Portfolio (GitHub Pages)

**하나의 저장소 · 하나의 Pages 배포 · 여섯 화면**: Home + About Me + Career + Traveling + Writing + Reading.

이 ZIP은 GitHub에 올리는 **전체 소스 저장소**입니다. ZIP 파일 자체를 GitHub에 업로드하는 것이 아니라, **압축을 푼 뒤 안에 있는 파일과 폴더 전부**를 저장소 최상위에 넣어야 합니다. `.github` 폴더도 반드시 포함하세요.

- 권장 저장소 이름: `Portfolio` (대소문자 일치)
- 권장 공개 주소: `https://limdaniel10.github.io/Portfolio/`
- 배포 방식: **GitHub Actions** (구식 `Deploy from a branch`가 아님)
- 최상위 `index.html` = Home, `about/`, `career/`, `traveling/`, `writing/`, `reading/` = 각각의 주소
- 배포 워크플로는 **`.github/workflows/deploy.yml` 하나만 사용**. 원래 여섯 ZIP에 있던 독립 배포 워크플로는 중복 실행되지 않도록 병합했습니다.

## 1. 폴더 구조

```text
Portfolio/
├── index.html                        # Home
├── about/index.html                 # About Me
├── career/index.html                # Career
├── traveling/                       # 지도, 이동 경로, 지도 라이브러리, 현행 JS 데이터
│   ├── index.html, app.js, style.css
│   ├── assets/                       # Leaflet, world.js, data.js
│   ├── data/baseline.json           # 기존 여행 기록 보호용 원본
│   └── sheets/                      # Google Sheets 초기 입력 CSV 9개
├── writing_source/                  # **여기에 Markdown 추가**
│   ├── content/collections.yml      # 작품 메타데이터
│   ├── content/collections/...      # 각 원고: 1회차 = 1개의 .md
│   ├── content/essays/              # 독립 에세이 .md
│   ├── content/readings/            # 독서 관련 글 .md (처음에는 비어 있음)
│   ├── content/fiction/             # 소설 연재 추가 시
│   ├── assets/                      # Writing 원본 디자인
│   └── scripts/build.py             # 자동 HTML 생성기
├── reading/
│   ├── index.html, app.js, styles.css
│   ├── sheets/Books.csv             # Google Sheets 초기 입력용
│   ├── sheets/MonthlyPages.csv      # Google Sheets 초기 입력용
│   └── data/{books,monthly-pages}.json
├── assets/resume.pdf                # Career 이력서 파일
├── css/, js/                        # 공통 루트 배치, 홈/소개/경력 CSS·JS
├── scripts/
│   ├── sync_reading.py              # Sheets 또는 CSV → Reading JSON
│   ├── sync_travel.py               # Sheets 또는 CSV → Traveling data.js
│   └── build_site.py                # 6개 화면을 _site/로 통합 생성
├── tests/                            # 읽기/링크/데이터 검증
├── .github/workflows/deploy.yml      # 유일한 배포 워크플로
├── .nojekyll, .gitignore
└── requirements.txt
```

`writing/`, `data/countries.json`, `data/visited-world.svg`는 자동으로 생성됩니다. **`_site/` 폴더는 배포용 결과물이므로 Git에 올릴 필요가 없습니다.** `.gitignore`에 포함했습니다.

## 2. GitHub에 올리기 — 가장 안전한 순서

**기존 사이트 백업:** 현재 GitHub `Portfolio` 저장소로 이동 → **Code → Download ZIP**으로 먼저 백업합니다. 기존 Git 저장소의 변경 이력은 그대로 유지하는 편이 좋습니다.

### GitHub Desktop 이용 (권장, Windows)

1. GitHub Desktop 설치 및 로그인 → **File → Clone repository** → `limdaniel10/Portfolio` 선택.
2. 받은 통합 ZIP을 **압축 해제**합니다. 압축을 푼 곳에서 `index.html`, `.github`, `about`, `career` 등이 보이면 올바른 루트입니다.
3. 압축을 푼 파일·폴더를 복제한 `Portfolio` 로컬 폴더의 **최상위에 그대로 복사**합니다. 덮어쓰기 허용. 오래된 독립 Pages 워크플로가 있다면 지우고 이 ZIP의 `.github/workflows/deploy.yml` 하나만 남깁니다.
4. GitHub Desktop의 **Changes**에서 변경 내용 확인 → Summary에 `Integrate portfolio` → **Commit to main** → **Push origin**.
5. GitHub 웹사이트 → `Portfolio` → **Settings → Pages → Build and deployment → Source: GitHub Actions**. 기존에 `Deploy from a branch`였다면 꼭 변경합니다.
6. **Actions** 탭에서 `Build and deploy full Portfolio` 워크플로가 성공인지 확인한 뒤 위 주소를 방문합니다.

**중요:** ZIP 파일 1개를 `Add file → Upload files`로 업로드해도 GitHub가 압축을 자동으로 풀어주지 않습니다. 반드시 내부 파일들을 올리세요. 기존 저장소에 이미 `gh-pages` 방식 또는 다른 배포 워크플로가 있다면 충돌 가능성을 제거해야 합니다.

**CLI 이용시**: `git clone https://github.com/limdaniel10/Portfolio.git` 후 압축을 푼 파일을 클론 폴더에 복사하고, `git add -A && git commit -m "Integrate portfolio" && git push origin main` 실행. 강제 push(`--force`)는 사용하지 마세요.

## 3. Writing — 새로운 글 하나 추가하기

예: `writing_source/content/collections/solo-abroad/041.md`

```markdown
---
title: 새로운 여행의 시작
collection_id: solo-abroad
chapter: 41
date: 2026-11-12
category: collections
special: false
status: text
brunch_url: https://brunch.co.kr/@lim-eat-less/230
---

이곳부터 본문입니다.

## 소제목

Markdown 내용은 배포 시 HTML 페이지로 자동 변환됩니다.
```

파일 추가 후 GitHub에 commit/push하면 GitHub Actions가 **작품 목차, 해당 회차 페이지, 이전·다음 회차 링크, 전체 목록 JSON을 모두 자동 갱신**합니다. 별도 HTML 또는 JSON 수작업이 필요 없습니다. 새로운 작품은 `writing_source/content/collections.yml`에 작품 메타데이터를 한 번 추가해야 합니다.

**현재 Writing 원고 상태 (2026-11-12 업데이트):** `el-salvador`의 1~13화와 `arctic`의 1~7화는 저자의 Brunch 원문을 Markdown으로 보관합니다. `tallinn` 1~9화, `venezuela` 1화, `short-disappearance` 1화는 검증 가능한 작가 원문 주소를 찾지 못해 임의로 작성하지 않았습니다. 다른 작품의 과거 미확인 원고는 `writing_source/MISSING_TEXT.csv`와 실제 Markdown을 확인하세요. 원고를 추가할 때는 `writing_source/content/collections/<작품ID>/NNN.md` 하나씩 넣습니다. 안전한 수집 도구는 `writing_source/scripts/sync_brunch_originals.py`, 출처 매핑은 `writing_source/brunch_import.yml`입니다.

## 4. Reading — Google Sheets 연동

기본적으로 ZIP에 있는 기존 **1,412권**과 **84개월의 MonthlyPages 기록**을 CSV/JSON에 보존했습니다. Sheets 연결을 **하지 않아도** 해당 기록으로 GitHub Pages가 정상 배포됩니다.

### 최초 Google Sheet 만들기

1. Google Sheets 파일 하나 생성. 탭을 **정확히** `Books`, `MonthlyPages`로 만듭니다.
2. 제공된 `reading/sheets/Books.csv`의 **전체 행을 `Books` 탭**에, `reading/sheets/MonthlyPages.csv` 전체 행을 **`MonthlyPages` 탭**에 CSV 가져오기로 입력합니다. `CompletedDate` 열은 **Plain text(일반 텍스트)** 형식으로 설정하여 `YYYY-MM` 형식을 유지하세요. 머리글은 변경하지 마세요. 부분 데이터만 가져오면 데이터 보호 검사 때문에 동기화 실패합니다.
3. Google Cloud에서 **Google Sheets API**를 활성화하고 **서비스 계정**을 만든 뒤 JSON 키를 생성합니다. 서비스 계정 이메일(`client_email`)에 Google Sheet **Viewer** 권한을 공유합니다.
4. GitHub `Portfolio` → **Settings → Secrets and variables → Actions**에서
   - **Repository secret**: `GOOGLE_SERVICE_ACCOUNT_JSON` = 서비스 계정 JSON 키 **전체 내용** (파일은 Git에 절대로 올리지 말 것)
   - **Repository variable**: `GOOGLE_SHEETS_ID` = Sheet URL의 `/d/`와 `/edit` 사이 ID
5. **Actions → Build and deploy full Portfolio → Run workflow**로 시험합니다. 설정이 정상이면 매일 12:17 UTC에 변경 여부를 다시 확인하고 자동 배포합니다. 수동 Git commit 없이 Google Sheet 행을 추가해도 공개 사이트가 갱신됩니다.

계산 규칙은 고정입니다: **완독 권수 = Books의 `CompletedDate`**, **페이지 수 = MonthlyPages의 `PagesRead`**. 책별 페이지 수를 합산하지 않습니다. 월/연도 중복, 책 ID 중복, 과거 기록 삭제, 잘못된 날짜 등을 검사합니다.

Sheets를 연결하지 않았다면 `reading/sheets/*.csv`를 수정하여 Git에 push하는 방식으로도 갱신할 수 있습니다.

## 5. Traveling — Google Sheets 연동 (9개 탭)

기존 여행 데이터 전체를 원형대로 보존하는 CSV 9개를 `traveling/sheets/`에 넣었습니다:

`Countries`, `Places`, `DomesticPlaces`, `Visits`, `Airports`, `Flights`, `AirportNights`, `Stays`, `SurfaceRoutes`.

1. **별도의** Google Spreadsheet 하나를 만들고, 위 이름 그대로 9개의 시트를 만듭니다.
2. 각 `traveling/sheets/<탭이름>.csv`의 **전체 데이터**를 대응하는 탭에 가져옵니다. CSV 파일마다 첫 행의 컬럼 이름이 동일해야 합니다. `months` 및 `start_date`/`end_date` 필드는 Google Sheets에서 **Plain text(일반 텍스트)**로 취급해 `2026-11`, `2026-11-12` 같은 값을 보존하세요.
3. 같은 서비스 계정 이메일에 **Viewer** 공유합니다.
4. GitHub Actions **Repository variable** `GOOGLE_TRAVEL_SHEETS_ID`에 이 두 번째 Spreadsheet의 ID를 넣습니다. `GOOGLE_SERVICE_ACCOUNT_JSON` secret은 Reading과 **공유**합니다.
5. Actions에서 워크플로를 수동 실행해 확인하면, 이후에는 Google Sheet 수정 내용이 자동으로 여행 지도·홈 국가 수·홈 지도에 반영됩니다.

**장소 추가 예시:** `Countries`에 없는 국가라면 국가 행부터 추가 → `Places`에 고유한 `id`, 장소명, 국가 2자리 코드, 위도, 경도 추가 → `Visits`에 **동일한 `place_id`**, 방문 `year`, `months` (예: `2026-11`) 추가 → 연도별 국가 방문 기간까지 보존하려면 `Stays`에도 추가. 한 번에 여러 월을 입력할 땐 `2026-11;2026-12`처럼 **세미콜론 구분**. 국내 장소는 `DomesticPlaces` 탭에 추가합니다. 항공편을 추가하려면 필요한 공항을 `Airports` 탭에 먼저 추가하고 `Flights`에 등록합니다.

원본의 비행 경로 및 육로 경로 곡선은 기존 좌표가 변경되지 않는 한 **그대로 유지**합니다. 새 장소는 새 지도 점으로, 새 항공편은 단순한 개략선으로 나타납니다. 모든 데이터를 입력하지 않고 일부 행만 올리면 이전 기록 삭제로 판정하여 **배포가 차단**됩니다.

**원본의 일부 국가 코드(`GB`, `MD`)는 계산 기준이 다른 중복 항목으로 저장되어 있으므로, 두 행을 임의로 병합하면 안 됩니다.** 방문국 수는 `Countries`의 `count_in_195 = TRUE` 개수를 기준으로 집계합니다. 도시·지역 336개와 같은 기존 역사적 수치는 원본 데이터와 집계 기준이 완전히 대응되지 않아 별도로 유지합니다.

Sheets를 연결하지 않으면 `traveling/sheets/*.csv` 파일을 수정하고 commit/push해도 됩니다. 데이터 구조·열 이름을 바꾸지 마세요.

## 6. About Me / Career 수동 수정

- About Me: `about/index.html`, `css/about.css`
- Career: `career/index.html`, `css/career.css`, `js/career.js`
- 이력서 내용 및 형식 수정: `scripts/build_resume.py`에서 편집합니다. GitHub Actions가 배포 시 `_site/assets/resume.pdf`를 새로 생성하므로, 저장소의 기존 `assets/resume.pdf`를 직접 교체해도 배포본에 반영되지 않습니다. Career의 Resume 링크는 브라우저 새 탭에서 PDF를 엽니다.
- 홈 문구·카드: `index.html`, `css/home.css`, `js/home.js`
- Career의 TSMC/Georgia Tech/HAFS 로고 이미지는 원본처럼 외부 URL을 참조하며, 로딩 실패 시 텍스트 대체 로고를 표시합니다.
- About Me의 인물 사진은 원본 ZIP부터 **Portrait 자리표시자**였으므로 실제 사진을 추가하려면 직접 넣어야 합니다.

## 7. 컴퓨터에서 로컬 테스트 (Python)

저장소 루트에서:

```bash
python -m pip install -r requirements.txt
python scripts/sync_reading.py --from-csv
python scripts/sync_travel.py --from-csv
python scripts/build_site.py --base /
python tests/test_integration.py
python writing_source/tests/test_build.py
python -m unittest discover -s tests -p "test_sync_*.py"
python -m http.server 8000 --directory _site
```

브라우저 주소: `http://localhost:8000/`. **`index.html`을 더블클릭하여 `file://`로 열면 JSON fetch가 실패할 수 있으므로 HTTP 서버로 확인하세요.**

**배포 URL을 바꾸는 경우:** 워크플로의 `python scripts/build_site.py --base /Portfolio/`에서 `/Portfolio/`를 실제 저장소 이름에 맞게 바꿔야 합니다. 루트에 배포되는 `username.github.io` 특별 저장소라면 `--base /`로 변경하세요.

## 8. 장애 확인

- 사이트가 404: 저장소 이름 대소문자, Pages 설정이 **GitHub Actions**인지, Actions 배포 성공 여부 확인.
- Writing만 404: Markdown 파싱 오류, `writing_source/content` 메타데이터, Actions 로그 확인.
- Reading이 업데이트되지 않음: 서비스 계정 공유, secret, `GOOGLE_SHEETS_ID`, `Books`/`MonthlyPages` 탭의 **전체 기존 데이터** 확인.
- Traveling이 업데이트되지 않음: `GOOGLE_TRAVEL_SHEETS_ID` 변수, 9개 탭 이름·열, 국가/장소 ID 연결, Actions 로그 확인.
- 데이터 일부 누락: 동기화 스크립트는 **기존 항목 삭제를 기본 거부**합니다. 의도적으로 원본을 삭제할 때만 로컬에서 `--allow-deletions` 옵션을 사용하며, GitHub 자동 배포에서는 삭제를 허용하지 않습니다.
- 원고 본문 누락: `writing_source/MISSING_TEXT.csv` 확인. 작성자가 직접 Markdown 본문을 추가해야 합니다.

이 ZIP은 기존 사이트를 대신하는 **단일 통합본**이며 기존 데이터 손실을 피하기 위해 기존 아카이브·원고·이력서를 그대로 포함합니다.
