import requests


def get_all_students():
    url = "http://127.0.0.1:8000/students"
    response = requests.get(url)
    return response.json()


def get_students_with_param_requests(course: int):
    url = "http://127.0.0.1:8000/students"
    response = requests.get(url, params={"course": course})
    return response.json()


students = get_students_with_param_requests(course=2)
for student in students:
    print(student)

students = get_all_students()
for i in students:
    print(i)