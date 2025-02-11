from typing import List
from fastapi import APIRouter
from app.majors.dao import MajorsDAO
from app.majors.schemas import SMajorsAdd, SMajorsUpdDesc, SMajor

router = APIRouter(prefix='/majors', tags=['Работа с факультетами'])


@router.post("/add/")
async def register_user(major: SMajorsAdd) -> dict:
    check = await MajorsDAO.add(**major.model_dump())
    if check:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        return {"message": "Ошибка при добавлении факультета!"}


@router.put("/update_description/")
async def update_major_description(major: SMajorsUpdDesc) -> dict:
    check = await MajorsDAO.update(filter_by={'major_name': major.major_name},
                                   major_description=major.major_description)
    if check:
        return {"message": "Successfully updated major description", "major": major}
    else:
        return {"message": "Failed while updating major description"}


@router.delete("/delete/{major_id}")
async def delete_major(major_id: int) -> dict:
    check = await MajorsDAO.delete(id=major_id)
    if check:
        return {"message": "Successfully deleted major", "major": major_id}
    return {"message": "Failed while deleting major"}


@router.get("/majors/")
async def get_majors() -> List[SMajor]:
    return await MajorsDAO.find_all()
