from pydantic import BaseModel, validator, conint, constr, conlist
import datetime
from enum import Enum
from typing import Optional

class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


class Student(BaseModel):
    first_name: constr(max_length=255) #must be a string type 
    last_name: str #must be a string type
    age: conint(ge=10, le=20) # a way of constraining age value
    date_joined: datetime.date
    level: Optional[Level] #= Level.BEGINNER

    '''Another way of constraining age value 
    @validator("age")
    def validate_age(cls, age):
        if age < 10:
            raise ValueError("Age must be 10 or above!")
        print(age)
        return age'''
    

    @validator("level")
    def validate_level_from_age(cls, level, values):
        if level is not None:
            if level is Level.ADVANCED and values["age"] <14:
                raise ValueError("To be advanced the student must be above 14.")
        print(values)
        return level
    
class Course(BaseModel):
    title: constr(max_length=30)
    teacher: str
    students: Optional[conlist(item_type=Student, max_items= 10)] = []


student = Student(
    first_name="Harry",
    last_name="Potter",
    age = 20, #usign conint any value outside of range will pop up an error message that is intuitive
    date_joined=datetime.date(2020,1,1),
    level = Level.ADVANCED
)


course = Course(
    title="History",
    teacher="Albus Dumbledore",

)
#print(student)
#print(course)

course.students.append(student)
#print(course)

print(student.dict())

print(student.json())# makes a json representation

print(course.json())
