from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/managescanners", response_class=HTMLResponse)
def get_managescanners(request: Request):
    return templates.TemplateResponse('managescanners.html', context={'request': request})