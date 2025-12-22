from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.core import Crud, Database, SessionDep, templates
from src.routes import category_route, items_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    Database.connect()
    yield
    Database.disconnect()


app = FastAPI(title="Finance Tracker", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(items_route)
app.include_router(category_route)

crud = Crud()


@app.get("/")
def index(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
        },
    )


@app.get("/list")
def list_page(request: Request):
    return templates.TemplateResponse("list_page.html", {"request": request})


@app.get("/health", include_in_schema=False)
def health_check_endpoint():
    """Return the health status of the API

    This endpoint is used for monitoring purposes to verify that the API
    is up and running. It returns a simple JSON response indicating the
    status of the application.
    """
    return JSONResponse(content={"status": "ok"})


@app.get("/label")
def get_categories(request: Request, session: SessionDep):
    labels = crud.get_label(session)
    return templates.TemplateResponse(
        "components/labels.html", {"request": request, "labels": labels}
    )


@app.post("/label")
def add_label(session: SessionDep, name: str):
    """Add a new label to the database

    Args:
        session: The database session injected by FastAPI.
        name: The name of the new label.

    Returns:
        JSON response indicating whether the label was added successfully.
    """
    if crud.set_label(session, name):
        return JSONResponse(
            content={"status": "success added new label"}, status_code=201
        )
    else:
        return JSONResponse(
            content={"status": "failed added new label"}, status_code=400
        )
