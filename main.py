"""FastAPI application for classifying uploaded file names by extension."""

from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


APP_DIR = Path(__file__).resolve().parent
MAX_FILES_PER_REQUEST = 100

# Extensions are kept without a leading period for convenient display and comparison.
CATEGORY_EXTENSIONS: dict[str, set[str]] = {
    "이미지": {"jpg", "jpeg", "png", "gif"},
    "문서": {"pdf", "docx", "pptx", "txt"},
    "영상": {"mp4", "mov", "avi"},
    "압축파일": {"zip", "rar", "7z"},
}

app = FastAPI(title="파일 확장자 분류기")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
templates = Jinja2Templates(directory=APP_DIR / "templates")


def safe_file_name(filename: str) -> str:
    """Return only the final name part if a client submits a path as the filename."""
    return filename.replace("\\", "/").rsplit("/", maxsplit=1)[-1]


def classify_file_name(filename: str) -> dict[str, str]:
    """Classify a filename using its final extension, without saving the uploaded file."""
    display_name = safe_file_name(filename)
    extension = Path(display_name).suffix.lower().lstrip(".")

    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return {
                "name": display_name,
                "extension": extension or "없음",
                "category": category,
                "category_class": category,
            }

    return {
        "name": display_name,
        "extension": extension or "없음",
        "category": "기타",
        "category_class": "기타",
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"results": None, "error": None})


@app.post("/classify", response_class=HTMLResponse)
async def classify_files(
    request: Request,
    files: list[UploadFile] | None = File(default=None),
) -> HTMLResponse:
    if not files:
        return templates.TemplateResponse(
            request,
            "index.html",
            {"results": None, "error": "업로드할 파일을 하나 이상 선택해 주세요."},
            status_code=400,
        )

    if len(files) > MAX_FILES_PER_REQUEST:
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "results": None,
                "error": f"한 번에 최대 {MAX_FILES_PER_REQUEST}개 파일까지 분류할 수 있습니다.",
            },
            status_code=400,
        )

    results = []
    for uploaded_file in files:
        # File content is intentionally never read or written to permanent storage.
        if not uploaded_file.filename:
            continue
        results.append(classify_file_name(uploaded_file.filename))
        await uploaded_file.close()

    if not results:
        return templates.TemplateResponse(
            request,
            "index.html",
            {"results": None, "error": "유효한 파일 이름을 찾을 수 없습니다."},
            status_code=400,
        )

    return templates.TemplateResponse(request, "index.html", {"results": results, "error": None})


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, _: RequestValidationError) -> HTMLResponse:
    """Show a friendly page when the request does not contain valid form data."""
    return templates.TemplateResponse(
        request,
        "index.html",
        {"results": None, "error": "요청 형식이 올바르지 않습니다. 파일을 다시 선택해 주세요."},
        status_code=400,
    )
