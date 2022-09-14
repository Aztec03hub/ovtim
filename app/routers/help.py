from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/help", response_class=HTMLResponse)
def get_help(request: Request):
    return templates.TemplateResponse('help.html', context={'request': request})