from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent, SStudentAdd
from typing import Union


router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get("/", summary="Получить всех студентов", response_model=list[SStudent])
async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
    students = await StudentDAO.find_all(**request_body.to_dict())
    result = []
    for student in students:
        student_data = student.to_dict()  # Преобразуем студента в словарь
        student_data["major"] = student.major.major_name if student.major else None  # Преобразуем Major в строку
        result.append(SStudent(**student_data))  # Валидируем через SStudent
    return result

@router.get("/by_filter", summary="Получить одного студента по фильтру")
async def get_student_by_filter(request_body: RBStudent = Depends()) -> Union[SStudent, dict]:
    rez = await StudentDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Студент с указанными вами параметрами не найден!'}
    return rez

@router.get("/{id}", summary="Получить одного студента по id")
async def get_student_by_id(student_id: int) -> Union[SStudent, dict]:
    rez = await StudentDAO.find_full_data(student_id)
    if rez is None:
        return {'message': f'Студент с ID {student_id} не найден!'}
    return rez

@router.post("/add/")
async def add_student(student: SStudentAdd) -> dict:
    check = await StudentDAO.add_student(**student.dict())
    if check:
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}

@router.delete("/dell/{student_id}")
async def dell_student_by_id(student_id: int) -> dict:
    check = await StudentDAO.delete_student_by_id(student_id=student_id)
    if check:
        return {"message": f"Студент с ID {student_id} удален!"}
    else:
        return {"message": "Ошибка при удалении студента!"}