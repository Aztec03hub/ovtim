from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/weblink", response_class=HTMLResponse)
def get_weblink(request: Request):
    return templates.TemplateResponse('weblink.html', context={'request': request})