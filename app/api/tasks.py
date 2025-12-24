from fastapi.routing import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
def create_task():
    pass


@router.get("/")
def get_task_list():
    pass


@router.get("/{pk}")
def get_one_task(pk: int):
    pass


@router.put("/{pk}")
def update_task():
    pass


@router.delete("/{pk}")
def delete_task():
    pass