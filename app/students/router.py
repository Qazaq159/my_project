from typing import List, Dict
from fastapi import APIRouter, Depends
from app.students.rb import RBStudent
from app.students.dao import StudentDAO
from app.students.schemas import SStudent, SStudentDetail, SStudentAdd


router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get('/', summary='Получит всех студентов')
async def get_all_students(request_body: RBStudent = Depends()) -> List[SStudent]:
    return await StudentDAO.find_all(**request_body.to_dict())


@router.get('/{id}', summary='Получить одного студента по id')
async def get_student_by_id(student_id: int) -> SStudentDetail | Dict[str, str]:
    rez = await StudentDAO.find_full_data(student_id)
    if rez is None:
        return {'message': f'Student does not exists with this ID - {student_id}'}
    return rez


@router.get('/by_filter', summary='Fetch a student by filter')
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SStudentDetail | Dict[str, str]:
    rez = await StudentDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Student does not exists with these parameters'}
    return rez


@router.post("/add/")
async def add_student(student: SStudentAdd) -> dict:
    check = await StudentDAO.add_student(**student.model_dump())
    if check:
        return {"message": "Successfully added student", "student": student}
    else:
        return {"message": "Failed to add student"}


@router.delete('/dell/{student_id}')
async def dell_student_by_id(student_id: int) -> dict:
    check = await StudentDAO.delete_student_by_id(student_id=student_id)
    if check:
        return {"message": f"Student delete with ID {student_id} successfully"}
    return {"message": "Failed to delete student"}
