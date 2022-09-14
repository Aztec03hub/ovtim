from unicodedata import name
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import Helpers
from .library.readConfig import *

# Import Routers
from app.routers import managescanners, weblink

# My Imports
#from fastapi_socketio import SocketManager

# Create App
app = FastAPI()

# Pass App into SocketManager
#socket_manager = SocketManager(app=app)

# Configure Jinja2
templates = Jinja2Templates(directory="templates")

# Mount Static Files. Usage Examples:
# CSS - <link href="{{ url_for('static', path='/css/mycssfile.css') }}" rel="stylesheet">
# ICO - <link rel="icon" href="{{ url_for('static', path='/img/myicon.ico') }}" sizes="32x32"/>
# JS  - <script src="{{ url_for('static', path='/js/myscript.js') | safe}}"></script>
# Note: if a served static file results in '*.filetype.map' 404 Not Found, OPEN THE DAMN FILE AND REMOVE THE .MAP CALL AT END-OF-FILE!
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include our routers in the app
app.include_router(managescanners.router)
app.include_router(weblink.router)

# Main App Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Other Routes
@app.get("/page/{page_name}", response_class=HTMLResponse)
async def page(request: Request, page_name: str):
    return templates.TemplateResponse("page.html",  {"request": request})