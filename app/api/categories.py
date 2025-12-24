from typing import Annotated, List
from uuid import uuid1
import shutil

from fastapi import Form, Depends, HTTPException, status, File, UploadFile
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..models.user import User
from ..models.task import Category
from ..schemas.categories import CategoryResponse
from .deps import get_admin, get_user, get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse)
def create_categories(
    name: Annotated[str, Form()],
    color: Annotated[str, Form()],
    icon: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists."
        )

    if icon.content_type not in ["image/svg+xml", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="icon should be svg format"
        )

    if icon.content_type == "image/svg+xml":
        icon_extention = "svg"
    elif icon.content_type == "image/png":
        icon_extention = "png"

    icon_path = f"media/category-icons/{str(uuid1())}.{icon_extention}"
    with open(icon_path, "wb") as f:
        shutil.copyfileobj(icon.file, f)

    new_category = Category(name=name, color=color, icon=icon_path)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_category_list(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    categories = db.query(Category).all()
    return categories


@router.get("/{pk}")
def get_one_category(pk: int):
    pass


@router.put("/{pk}")
def update_category():
    pass


@router.delete("/{pk}")
def delete_category():
    pass