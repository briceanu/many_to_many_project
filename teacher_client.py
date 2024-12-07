import requests
import sys
import json




def create_teachers():
    url = 'http://localhost:8000/api/teacher'

    data = {'name':'adriana',
            'beginning_teaching': '2015-09-15',
            'teaching_subject_1':'geography',
            'teaching_subject_2':'history',
            'teaching_subject_3':'chemistry',
            }


    res = requests.post(data=data,url=url)
    print(res.status_code)
    print(res.text)





def list_teachers():
    response = requests.get("http://localhost:8000/api/teacher")
    if response.status_code == 200:
        # Pretty-print the JSON response
        teachers = response.json()
        for teacher in teachers:
            print(json.dumps(teacher['teacher_id'],indent=4))
        # print(json.dumps(teachers, indent=4))  # Use indent=4 for better readability
    else:
        print(f"Error: {response.status_code}")
        print(response.text)





def create_students():
    url = 'http://localhost:8000/api/student'

    data = {'name':'rizea robert',
            'age': 29,
            'interested_in':'geogrphy, french and english',
            'email':'rizearobert@gmail.com',
             }


    res = requests.post(data=data,url=url)
    print(res.status_code)
    print(res.text)





def list_students():
    url = 'http://localhost:8000/api/student'
    
    response = requests.get(url)
    if response.status_code == 200:
        # Pretty-print the JSON response
        students = response.json()
        # for student in students:
        print(json.dumps(students, indent=4))  # Use indent=4 for better readability

            # print(json.dumps(student['student_id'], indent=4))  # Use indent=4 for better readability
    else:
        print(f"Error: {response.status_code}")
        print(response.text)






def create_course():
    url = 'http://localhost:8000/api/course'

    teacher_ids = [
    "f18900c4-aa26-47f0-ad6e-94471411a67d",
    "3682bc25-039c-4809-9eae-b011d7c16c37",
    "376570ab-3355-4951-91d6-8262e07877f6",
    "4d936d23-63d7-44bc-8218-0afa1eac2e19",
    "6d6bf362-2de1-47a2-9b79-b4773d8d9612",
    "28bc217e-5edd-48b0-afc4-d7d945325dee"
        ]

    student_ids = [

        "13c494e4-1fa7-465b-bc3f-342e187553e0",
        "d8688510-12f1-4d98-8509-095c62b2770e",
        "d2ab2184-67d5-4ca5-b518-3ccd0dbf87e8",
        "a6353edc-03b5-417e-a8e4-dd664de390fb",
        "85921fcd-55e9-4fb2-9bf9-e08973d84758",
        "d7af32d7-ca86-4422-a059-af5c34e5b807",
        "b13cc72b-edcd-409a-9cec-b7053ab82182",
        "91c2a474-c392-462b-b882-cb9223ef5e96",
        "bcc62b70-65d9-4520-add5-199ada587ce1",
            ]



    data = {
        'date_time_scheduled': '2024-06-27 17:30',  
        'duration': '06:00:00',  
        'charge': 160.20,
        'teachers': teacher_ids,  
        'students': student_ids,  
    }


    res = requests.post(data=data,url=url)
    print(res.status_code)
    print(res.text)





def list_courses():
    url = 'http://localhost:8000/api/course'

    response = requests.get(url)
    if response.status_code == 200:
        # Pretty-print the JSON response
        courses = response.json()
        for course in courses:
            print(json.dumps(course['course_id'],indent=4))
        # print(json.dumps(courses, indent=4))  # Use indent=4 for better readability
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def list_one_course():
    url = 'http://localhost:8000/api/one_course/3c7bac54-7f6b-4297-a389-a9b90f28775d'

    res = requests.get(url=url)
    print(res.status_code)
    print(res.text)


def list_param():
    url = 'http://localhost:8000/api/course_query?duration=02:00:20'

    res = requests.get(url=url)
    print(res.status_code)
    print(res.text)

def number_of_teachers():
    data = {'course_id':"f5b5fb82-adaf-4411-8c71-f2416b0fca51"}


    url = 'http://localhost:8000/api/number_of_teachers'

    res = requests.get(url=url,data=data)
    print(res.status_code)
    print(res.text)



def course_search():
    


    url = 'http://localhost:8000/api/course_search?charge=39&beginning_teaching=2021-05'

    res = requests.get(url=url)
    print(res.status_code)
    print(res.text)









if __name__ == '__main__':

    if sys.argv[1] == 'list_teachers':
        list_teachers()

    elif sys.argv[1] == 'create_teachers':
        create_teachers()
    elif sys.argv[1] == 'list_students':
        list_students()

    elif sys.argv[1] == 'create_students':
        create_students()

    elif sys.argv[1] == 'list_courses':
        list_courses()

    elif sys.argv[1] == 'create_course':
        create_course()
    
    elif sys.argv[1] == 'list_param':
        list_param()

    elif sys.argv[1] == 'list_one_course':
        list_one_course()

    elif sys.argv[1] == 'number_of_teachers':
        number_of_teachers()

    elif sys.argv[1] == 'course_search':
        course_search()
    else:
        print("you're search word doesn't match any of the functions")
    