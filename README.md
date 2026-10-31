# 파일 확장자 분류 웹서비스

여러 파일을 업로드하면 **파일 이름의 마지막 확장자**를 기준으로 카테고리를 표시하는 로컬 웹서비스입니다. Python과 FastAPI로 만들었으며, 업로드 파일의 내용은 읽거나 서버에 영구 저장하지 않습니다.

## 주요 기능

- 여러 파일을 한 번에 업로드하고 분류 결과 확인
- 이미지, 문서, 영상, 압축파일, 기타 분류
- 대소문자를 구분하지 않는 확장자 판별
- 파일 미선택, 잘못된 요청, 한 번에 100개 초과 업로드에 대한 오류 안내

## 분류 기준

| 카테고리 | 확장자 |
| --- | --- |
| 이미지 | jpg, jpeg, png, gif |
| 문서 | pdf, docx, pptx, txt |
| 영상 | mp4, mov, avi |
| 압축파일 | zip, rar, 7z |
| 기타 | 위 목록 외 확장자 또는 확장자 없음 |

## 실행 환경

- Windows PowerShell
- Python 3.10 이상
- 가상환경 없이 전역 Python 설치 환경에서도 실행 가능

## 설치 방법

저장소를 내려받은 뒤 프로젝트 폴더로 이동합니다.

```powershell
cd "파일을-내려받은-경로\file_extension_classifier"
```

필요한 패키지를 설치합니다.

```powershell
python -m pip install -r requirements.txt
```

## 실행 방법

다음 명령으로 개발 서버를 실행합니다.

```powershell
python -m uvicorn main:app --reload
```

브라우저에서 [http://127.0.0.1:8000](http://127.0.0.1:8000)을 엽니다. 파일을 여러 개 선택한 후 **파일 분류하기**를 누르면 결과를 확인할 수 있습니다.

서버를 종료하려면 PowerShell 창에서 `Ctrl+C`를 누릅니다.

## 프로젝트 구조

```text
file_extension_classifier/
├── main.py                 # FastAPI 라우팅과 확장자 분류 로직
├── requirements.txt        # 실행에 필요한 Python 패키지
├── templates/
│   └── index.html          # 웹 화면 템플릿
└── static/
    └── style.css           # 화면 스타일
```
Deployment test completed on Render.