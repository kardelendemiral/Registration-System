import mysql.connector
import environ
import hashlib

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='berfin2000',
    database='project2',
    auth_plugin='mysql_native_password'
)


def addStudent(username, name, surname, password, email, studentid, departmentid, credits, gpa):
    cursor = connection.cursor()
    encoded = password.encode()
    result = hashlib.sha256(encoded).hexdigest()
    cursor.execute(
        f"INSERT INTO students(username,name,surname,password,email,student_id,department_id,completed_credits,GPA) VALUES('{username}','{name}','{surname}','{result}','{email}',{studentid},'{departmentid}',{credits},{gpa});")
    connection.commit()


def addIns(title, username, name, surname, password, email, departmentid):
    cursor = connection.cursor()
    encoded = password.encode()
    result = hashlib.sha256(encoded).hexdigest()
    cursor.execute(
        f"INSERT INTO instructors(title,username,name,surname,password,email,department_id) VALUES('{title}','{username}','{name}','{surname}','{result}','{email}','{departmentid}');")
    connection.commit()


def addManager(username, password):
    cursor = connection.cursor()
    encoded = password.encode()
    result = hashlib.sha256(encoded).hexdigest()
    cursor.execute(f"INSERT INTO database_managers(username, password) VALUES('{username}','{result}')")
    connection.commit()


def createTables():
    cursor = connection.cursor()
    cursor.execute("""
    USE project2;

CREATE TABLE IF NOT EXISTS Departments (
department_name varchar(25) NOT NULL, # name of the department
department_id varchar(25) NOT NULL,   # id of the department
PRIMARY KEY(department_id), # id is the primary key of this relation
UNIQUE(department_id,department_name) # the tuple that contains department_id and department_name should be unique
);

CREATE TABLE IF NOT EXISTS Instructors (
title varchar(100) NOT NULL, # title of the instructor
username varchar(25) NOT NULL, # username of the instructor
name varchar(25) NOT NULL, # name of the instructor 
surname varchar(25) NOT NULL, # surname of the instructor
password varchar(256) NOT NULL, # password of the instructor
email varchar(100) NOT NULL,  # email of the instructor
department_id varchar(25) NOT NULL, # department id of the instructor
PRIMARY KEY(username), # username is the primary key of this relation
FOREIGN KEY(department_id) REFERENCES Departments(department_id) # department id is the foreign key which makes reference from departments relation
 ); 

CREATE TABLE IF NOT EXISTS Students ( 
username varchar(25) NOT NULL, # username of the student
name varchar(25) NOT NULL, # name of the student
surname varchar(25) NOT NULL, # surname of the student
password varchar(256) NOT NULL, # password of the student
email varchar(100) NOT NULL, # email of the student
student_id INTEGER NOT NULL, # student_id of the student
department_id varchar(25) NOT NULL, # department id of the student
completed_credits INTEGER,
GPA float,  # the GPA of the student
Unique(username),
PRIMARY KEY(student_id), # student id is the primary key of this relation
FOREIGN KEY(department_id) REFERENCES Departments(department_id) # department id is the foreign key which makes reference from departments relation
);




CREATE TABLE IF NOT EXISTS Classroom(
 classroom_id varchar(25), # id of the classroom that course given
 campus varchar(100), # campus name that course is given
 classroom_capacity INTEGER, # classroom capacity of the course
 PRIMARY KEY(classroom_id)
 );

CREATE TABLE IF NOT EXISTS Courses (
 course_id varchar(25) NOT NULL, # id of the course
 name varchar(100) NOT NULL, # name of the course
 classroom_id varchar(25), # id of the classroom that course given
 department_id varchar(25) NOT NULL, # id of the department that course belongs to
 course_code INTEGER NOT NULL, # code of the course
 credits INTEGER NOT NULL, # credits of the course
 instructor_username varchar(25), # username of the instructor that teach the course
 quota INTEGER, # quota of the course
 slot INTEGER, # time slot of the course
 PRIMARY KEY(course_id),  # primary key of the course id
 UNIQUE(slot, classroom_id),  # the tuple that contains slot and classroom should be unique
 FOREIGN KEY(department_id) REFERENCES Departments(department_id), # department id is the foreign key which makes reference from departments relation
 FOREIGN KEY( classroom_id) REFERENCES Classroom( classroom_id), # classrom id is the foreign key which makes reference from classroom relation
 CHECK( slot >=1 AND slot<= 10) # time slot should be between 1 and 10
 # The Course ID of a prerequisite must be less than the ID of the succeeding course:   course_id > prerequisite[i], for all i
);


CREATE TABLE IF NOT EXISTS PREREQUISITES (
	course_id varchar(25) NOT NULL,
    prerequisite_id varchar(25),
    PRIMARY KEY(course_id, prerequisite_id),
    FOREIGN KEY(course_id) REFERENCES Courses(course_id),
    FOREIGN KEY(prerequisite_id) REFERENCES Courses(course_id),
    CHECK (prerequisite_id < course_id )
);

CREATE TABLE IF NOT EXISTS Grades ( 
grade FLOAT, # grade
student_id INTEGER NOT NULL, # student id who owns the grade
course_id varchar(25) NOT NULL, # id of the course 
PRIMARY KEY(student_id, course_id), # primary keys are student id and course id 
FOREIGN KEY(student_id) REFERENCES students(student_id) ON UPDATE CASCADE ON DELETE CASCADE,  # student id is the foreign key which makes reference from students relation
FOREIGN KEY(course_id) REFERENCES courses(course_id) ON UPDATE CASCADE ON DELETE CASCADE # course id is the foreign key which makes reference from course relation
);

CREATE TABLE IF NOT EXISTS Database_Managers ( 
username varCHAR(25) NOT NULL, # username of the database manager
password varCHAR(256) NOT NULL,  # password of the database manager
PRIMARY KEY(username) # primary key of the database managers is username
# There can be at most 4 database managers registered to the
# system:    (SELECT  Count(*) AS tableSize FROM DatabaseManager) <= 4 
);




CREATE TABLE IF NOT EXISTS Enroll (
student_id INTEGER NOT NULL, # id of the student that enrolled in the course
course_id varchar(25) NOT NULL, # id of the course that is enrolled
grade FLOAT,
PRIMARY KEY(student_id, course_id), # student id and course id are the primary keys of this relation
FOREIGN KEY(student_id) REFERENCES Students(student_id)  ON UPDATE CASCADE ON DELETE CASCADE, # student id is the foreign key which makes reference from students relation
#FOREIGN KEY(student_id) REFERENCES Grades(student_id) ON UPDATE CASCADE ON DELETE CASCADE, # student id is the foreign key which makes reference from student relation
FOREIGN KEY(course_id) REFERENCES Courses (course_id) ON UPDATE CASCADE ON DELETE CASCADE # course id is the foreign key which makes reference from course relation
);






DELIMITER $$
CREATE TRIGGER  LimitDatabaseManager BEFORE INSERT ON database_managers FOR EACH ROW
BEGIN
	IF (SELECT COUNT(*) FROM database_managers) = 4 THEN
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There cannot be more than 4 database managers.'; 
	END IF;
END;
$$



DELIMITER $$
CREATE TRIGGER TitleCheck BEFORE INSERT ON instructors FOR EACH ROW
BEGIN
	IF New.title != "Assistant Professor" and New.title != "Associate Professor" and New.title != "Professor" THEN
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Allowed titles are Assistant Professor, Associate Professor and Professor.'; 
	END IF;
END;
$$


DELIMITER $$
CREATE TRIGGER TitleCheck2 BEFORE UPDATE ON instructors FOR EACH ROW
BEGIN
	IF New.title != "Assistant Professor" and New.title != "Associate Professor" and New.title != "Professor" THEN
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Allowed titles are Assistant Professor, Associate Professor and Professor.'; 
	END IF;
END;
$$


DELIMITER $$
CREATE TRIGGER updateg BEFORE INSERT ON grades FOR EACH ROW
BEGIN

DECLARE kredi INTEGER;
DECLARE total INTEGER;
DECLARE agno FLOAT;
SELECT
 credits, completed_credits, GPA
INTO
 kredi, total, agno
FROM
courses,students
WHERE
course_id = New.course_id and student_id = New.student_id;

   UPDATE students
SET 
   completed_credits = total + kredi

WHERE
   student_id = NEW.student_id;


	UPDATE students
SET 
    GPA = (total*agno+ kredi*New.grade)/(total+kredi)

WHERE
   student_id = NEW.student_id;

END;



$$

DELIMITER $$
CREATE TRIGGER quotaT BEFORE INSERT ON Courses FOR EACH ROW
BEGIN
	DECLARE kapasite INTEGER;
	SELECT
	classroom_capacity
	INTO
	kapasite
	FROM
	classroom
	WHERE
	classroom_id = New.classroom_id;

    IF (New.quota > kapasite) THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Quota exceeds classroom capacity.'; 
    END IF;
END;
$$

DELIMITER $$
CREATE TRIGGER addcourse BEFORE INSERT ON enroll FOR EACH ROW
BEGIN
	Declare enrolledc INTEGER;
    Declare kota INTEGER;
    SELECT  COUNT(student_id) INTO enrolledc
    FROM enroll WHERE course_id = New.course_id GROUP BY course_id;
    SELECT quota INTO kota FROM courses C WHERE New.course_id = C.course_id;


	IF EXISTS(SELECT * from grades G WHERE New.student_id=G.student_id and New.course_id=G.course_id)
    THEN
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You cannot take a course twice'; 

    ELSEIF (EXISTS (SELECT * from prerequisites P
    WHERE New.course_id = P.course_id and NOT EXISTS (SELECT * from grades G WHERE P.prerequisite_id= G.course_id and New.student_id = G.student_id and New.course_id = G.course_id  )  )  )
    THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Before adding this course, you should pass all the prerequisites'; 

    ELSEIF enrolledc >= kota
    THEN  
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You cannot add this course due to quota restrictions'; 

	END IF;
END;
$$


DELIMITER $$
CREATE TRIGGER grading BEFORE INSERT ON Grades FOR EACH ROW
BEGIN
    IF NOT EXISTS(SELECT * from enroll E WHERE E.student_id = New.student_id and E.course_id = New.course_id)

    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This student is not taking this course';

    ELSE DELETE FROM enroll E WHERE  E.student_id = New.student_id and E.course_id = New.course_id;
    END IF;
END;
$$



DELIMITER $$
CREATE PROCEDURE filterCourse(IN d_id varchar(25), IN camp varchar(100), IN minc INTEGER, IN maxc INTEGER)
BEGIN 
SELECT course_id,name,C.classroom_id,department_id,course_code,credits, instructor_username,quota,slot from courses C, classroom R WHERE C.department_id = d_id and R.campus = camp and C.classroom_id = R.classroom_id and C.credits<=maxc and C.credits>=minc;
END;
$$





""")

