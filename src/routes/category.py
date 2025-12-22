from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from src.core import Crud, SessionDep, templates

router = APIRouter(prefix="/category", tags=["Category"])
crud = Crud()


@router.get("/", response_class=HTMLResponse)
def get_categories(request: Request, session: SessionDep):
    categories = crud.get_category(session)
    return templates.TemplateResponse(
        "components/categories.html", {"request": request, "categories": categories}
    )


@router.post("/add")
def add_category(session: SessionDep, name: str = Form(...)):
    """Add a new category to the database

    Args:
        session (Session): The database session injected by FastAPI.
        name (str): The name of the new category.
    """
    crud.set_category(session, name)
