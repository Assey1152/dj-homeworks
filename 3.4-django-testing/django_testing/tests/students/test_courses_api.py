import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course

base_url = '/api/v1/courses/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


@pytest.mark.django_db
def test_course_filter(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?id={courses[3].id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[3].name


@pytest.mark.django_db
def test_course_create(client):
    data = {
        'name': 'course_test'
    }
    post_response = client.post('/api/v1/courses/', data=data)
    get_response = client.get(f'/api/v1/courses/?name={data["name"]}')
    get_data = get_response.json()
    assert post_response.status_code == 201
    assert get_response.status_code == 200
    assert get_data[0]['name'] == data['name']


@pytest.mark.django_db
def test_course_update(client, course_factory):
    course = course_factory(_quantity=1)
    data = {
        'name': 'new_name'
    }
    patch_response = client.patch(f'/api/v1/courses/{course[0].id}/', data=data)
    get_response = client.get(f'/api/v1/courses/?name={data["name"]}')
    get_data = get_response.json()
    assert patch_response.status_code == 200
    assert get_response.status_code == 200
    assert get_data[0]['name'] == data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    count = Course.objects.count()

    delete_response = client.delete(f'/api/v1/courses/{courses[5].id}/')
    get_response = client.get(f'/api/v1/courses/{courses[5].id}/')

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
    assert Course.objects.count() == count - 1


@pytest.mark.django_db
def test_max_students_success(client, course_factory, student_factory, settings):
    settings.MAX_STUDENTS_PER_COURSE = 2
    course = course_factory(_quantity=1)
    students = student_factory(_quantity=2)
    students_id = [i.id for i in students]
    response = client.patch(f'/api/v1/courses/{course[0].id}/', data={'students': students_id})
    assert response.status_code == 200
    get_response = client.get(f'/api/v1/courses/{course[0].id}/')
    data = get_response.json()
    assert course[0].students.count() <= settings.MAX_STUDENTS_PER_COURSE
    assert data['students'] == students_id


@pytest.mark.django_db
def test_max_students_fail(client, course_factory, student_factory, settings):
    settings.MAX_STUDENTS_PER_COURSE = 2
    course = course_factory(_quantity=1)
    students = student_factory(_quantity=3)
    students_id = [i.id for i in students]
    response = client.patch(f'/api/v1/courses/{course[0].id}/', data={'students': students_id})
    assert response.status_code == 400
