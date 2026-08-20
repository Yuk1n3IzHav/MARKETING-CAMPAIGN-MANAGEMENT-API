from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_tasks():
    pass


@router.get("/{task_id}")
def get_task(task_id: int):
    pass


@router.post("/")
def create_task():
    pass


@router.put("/{task_id}")
def update_task(task_id: int):
    pass


@router.delete("/{task_id}")
def delete_task(task_id: int):
    pass
