from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement, catch_statement
import re
import hashlib


def index(req):
    #Logout the user if logged 
    if req.session:
        req.session.flush()
    
    isFailed=req.GET.get("fail",False) #Check the value of the GET parameter "fail"
    
    loginForm=UserLoginForm() #Use Django Form object to create a blank form for the HTML page

    return render(req,'loginIndex.html',{"login_form":loginForm,"action_fail":isFailed})





def studentLogin(req):
    #Retrieve data from the request body
    username=req.POST["username"]
    p = req.POST["password"]
    encoded = p.encode()
    password = hashlib.sha256(encoded).hexdigest()

    result=run_statement(f"SELECT * FROM students WHERE username='{username}' and password='{password}';") #Run the query in DB

    if result: #If a result is retrieved

        req.session["username"]=username #Record username into the current session
        return HttpResponseRedirect('../sites/studentHome') #Redirect user to home page
    else:
        return HttpResponseRedirect('../sites?fail=true')


def instructorLogin(req):
    # Retrieve data from the request body
    username = req.POST["username"]
    p = req.POST["password"]
    encoded = p.encode()
    password = hashlib.sha256(encoded).hexdigest()

    result = run_statement(
        f"SELECT * FROM instructors WHERE username='{username}' and password='{password}';")  # Run the query in DB

    if result:  # If a result is retrieved

        req.session["username"] = username  # Record username into the current session
        return HttpResponseRedirect('../sites/instructorHome')  # Redirect user to home page
    else:
        return HttpResponseRedirect('../sites?fail=true')


def managerLogin(req):
    # Retrieve data from the request body
    username = req.POST["username"]
    p = req.POST["password"]
    encoded = p.encode()
    password = hashlib.sha256(encoded).hexdigest()




    result = run_statement(
        f"SELECT * FROM database_managers WHERE username='{username}' and password='{password}';")  # Run the query in DB

    if result:  # If a result is retrieved

        req.session["username"] = username  # Record username into the current session
        return HttpResponseRedirect('../sites/managerHome')  # Redirect user to home page
    else:
        return HttpResponseRedirect('../sites?fail=true')


def homePage(req):
    result=run_statement(f"SELECT * FROM courses;") #Run the query in DB
    
    username=req.session["username"] #Retrieve the username of the logged-in user
    isFailed=req.GET.get("fail",False) #Try to retrieve GET parameter "fail", if it's not given set it to False

    return render(req,'userHome.html',{"results":result,"action_fail":isFailed,"username":username})


def studentHome(req):
    result = run_statement(f"SELECT * FROM students;")  # Run the query in DB

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    return render(req, 'studentHome.html', {"results": result, "action_fail": isFailed, "username": username})

def managerHome(req):
    result = run_statement(f"SELECT * FROM database_managers;")  # Run the query in DB

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    return render(req, 'managerHome.html', {"results": result, "action_fail": isFailed, "username": username})

def instructorHome(req):
    result = run_statement(f"SELECT * FROM instructors;")  # Run the query in DB

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    return render(req, 'instructorHome.html', {"results": result, "action_fail": isFailed, "username": username})

def listAllCourses(req):
    result = run_statement(f"SELECT C.course_id , C.name, I.surname, C.department_id,C.credits, C.classroom_id,  C.slot, C.quota,group_concat(P.prerequisite_id order by P.prerequisite_id ASC)  as prerequisites FROM courses C INNER JOIN instructors I on C.instructor_username = I.username LEft join prerequisites P ON C.course_id = P.course_id  WHERE I.username = C.instructor_username  group by course_id  ORDER BY course_id ASC;")  # Run the query in DB
   # surname = run_statement(f"SELECT SUBSTRING(instructor_username, locate('.',instructor_username)+1 ) FROM courses; ")

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    return render(req, 'ListAllCourses.html', {"results": result, "action_fail": isFailed, "username": username})

def addCourse(req):
    course_id =req.POST["course id"]
    username = req.session["username"]  # Retrieve the username of the logged-in user
    student_id = catch_statement(f"SELECT student_id FROM students S WHERE S.username='{username}';")

    try:
        run_statement(f"INSERT INTO enroll(student_id, course_id) VALUES({student_id},'{course_id}') ;")  # Run the query in DB
        return HttpResponseRedirect("../sites/studentHome")
    except Exception as e:
        print(str(e))
        return render(req, 'studentHome.html', {"action_fail":True, "username": username,"exception": str(e)})


def listCurrentlyTakingCourses(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    sid = catch_statement(f"SELECT student_id from students WHere username='{username}' ; ")
    result = run_statement(f"select G.course_id, C.name,G.grade From courses C, grades G where G.course_id = C.course_id and G.student_id='{sid}' UNION  select E.course_id, C.name, grade  From courses C,enroll E where E.course_id = C.course_id and E.student_id='{sid}';")  # Run the query in DB

    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    return render(req, 'listCurrentlyTakingCourses.html', {"results": result, "action_fail": isFailed, "username": username})

def addNewStudent(req):
    uname=req.POST["username"]
    name=req.POST["name"]
    surname=req.POST["surname"]
    p = req.POST["password"]
    encoded = p.encode()
    password = hashlib.sha256(encoded).hexdigest()
    email=req.POST["email"]
    sid = req.POST["student id"]
    did =req.POST["department id"]
    compcred = req.POST["completed credits"]
    gpa = req.POST["gpa"]

    try:
        run_statement(
            f"INSERT INTO students(username,name,surname,password,email,student_id,department_id,completed_credits,GPA) VALUES('{uname}','{name}','{surname}','{password}','{email}',{sid},'{did}',{compcred},{gpa});")  # Run the query in DB

        return HttpResponseRedirect("../sites/managerHome")
    except Exception as e:
        print(str(e))
        return render(req, 'managerHome.html', {"action_fail":True, "username": req.session["username"],"exception": str(e)})

def addNewInstructor(req):
    title= req.POST["title"]
    uname = req.POST["username"]
    name = req.POST["name"]
    surname = req.POST["surname"]
    p = req.POST["password"]
    encoded = p.encode()
    password = hashlib.sha256(encoded).hexdigest()
    email = req.POST["email"]
    did = req.POST["department id"]

    try:
        run_statement(
            f"INSERT INTO instructors(title,username,name,surname,password,email,department_id) VALUES('{title}','{uname}','{name}','{surname}','{password}','{email}','{did}');")  # Run the query in DB

        return HttpResponseRedirect("../sites/managerHome")
    except Exception as e:
        print(str(e))
        return render(req, 'managerHome.html', {"action_fail":True, "username": req.session["username"],"exception": str(e)})

def deleteStudent(req):
    sid = req.POST["student id"]
    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    try:
        run_statement(
            f"DELETE from students WHERE student_id = {sid}")  # Run the query in DB

        return HttpResponseRedirect("../sites/managerHome")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../sites/managerHome?fail=true')

def updateTitle(req):
    insname = req.POST["instructor username"]
    tname = req.POST["new title"]
    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    try:
        run_statement(
            f"UPDATE Instructors SET title = '{tname}' WHERE username = '{insname}' ;")  # Run the query in DB

        return HttpResponseRedirect("../sites/managerHome")
    except Exception as e:
        print(str(e))
        return render(req, 'managerHome.html', {"action_fail":True, "username": req.session["username"],"exception": str(e)})

def viewStudents(req):
    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False


    result =  run_statement(
            f"SELECT username, name, surname, email, department_id, completed_credits, GPA FROM Students ORDER BY completed_credits ASC;")  # Run the query in DB

    return render(req, 'viewStudents.html', {"results": result, "action_fail": isFailed, "username": username})

def viewInstructors(req):
    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False


    result =  run_statement(
            f"SELECT username, name, surname, email, department_id, title FROM Instructors;")  # Run the query in DB

    return render(req, 'viewInstructors.html', {"results": result, "action_fail": isFailed, "username": username})

def viewAllGrades(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    sid = req.POST["student id"]

    result =  run_statement(
            f"SELECT C.course_id, C.name, G.grade FROM courses C,grades G WHERE  student_id = '{sid}' and C.course_id = G.course_id and G.student_id = '{sid}';")  # Run the query in DB

    return render(req, 'viewAllGrades.html', {"results": result, "action_fail": isFailed, "username": username})

def viewAllCourses(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    uname = req.POST["instructor username"]

    result =  run_statement(
            f"SELECT C.course_id, C.name, C.classroom_id, R.campus, C.slot FROM courses C, classroom R  WHERE C.instructor_username = '{uname}' and C.classroom_id = R.classroom_id; ")  # Run the query in DB

    return render(req, 'viewAllCourses.html', {"results": result, "action_fail": isFailed, "username": username})

def viewAverageGrade(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    cid = req.POST["course id"]

    result =  run_statement(
            f"SELECT G.course_id, C.name, AVG(G.grade) FROM grades G, courses C WHERE C.course_id = '{cid}' and C.course_id = G.course_id  GROUP BY G.course_id ;")  # Run the query in DB

    return render(req, 'viewAverageGrade.html', {"results": result, "action_fail": isFailed, "username": username})

def availableClassroom(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    slt = req.POST["slot"]

    result =  run_statement(
            f"SELECT R.classroom_id, R.campus, R.classroom_capacity FROM classroom R WHERE NOT EXISTS (SELECT * FROM courses C WHERE C.classroom_id = R.classroom_id and C.slot = '{slt}');")  # Run the query in DB

    return render(req, 'availableClassroom.html', {"results": result, "action_fail": isFailed, "username": username})

def addPre(req):
    cid = req.POST["course id"]
    pid = req.POST["prerequisite id"]
    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    try:
        run_statement(
            f"INSERT INTO prerequisites(course_id, prerequisite_id) VALUES('{cid}','{pid}') ;")  # Run the query in DB

        return HttpResponseRedirect("../sites/instructorHome")
    except Exception as e:
        print(str(e))
        return render(req, 'instructorHome.html', {"action_fail": True, "username": username,"exception":str(e)})

def viewOwnCourses(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False





    result =  run_statement(
            f"SELECT C.course_id , C.name, C.classroom_id,  C.slot, C.quota,group_concat(P.prerequisite_id order by P.prerequisite_id ASC)  as prerequisites FROM courses C INNER JOIN instructors I on C.instructor_username = I.username LEft join prerequisites P ON C.course_id = P.course_id  WHERE I.username = C.instructor_username and  I.username='{username}' group by course_id  ORDER BY course_id ASC;")  # Run the query in DB

    return render(req, 'viewOwnCourses.html', {"results": result, "action_fail": isFailed, "username": username})

def viewOwnStudents(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    cid=req.POST["course id"]

    res = catch_statement(f"SELECT instructor_username From courses WHERE course_id = '{cid}'")
    err="This course is not belong to you."


    if res == req.session["username"]:

        result =  run_statement(
                f"SELECT S.username, S.student_id, S.email, S.name, S.surname FROM students S WHERE EXISTS (SELECT * FROM enroll A, courses C, instructors I WHERE  A.course_id = '{cid}' and C.course_id = '{cid}' and C.instructor_username = '{username}' and S.student_id = A.student_id and I.username = '{username}'); ")  # Run the query in DB

        return render(req, 'viewOwnStudents.html', {"results": result, "action_fail": isFailed, "username": username})
    else:

        return render(req, 'instructorHome.html', {"action_fail": True, "username": username,"exception":err })


def updateCourseName(req):
    c_id = req.POST["course id"]
    c_name = req.POST["new course name"]
    i_uname = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    res = catch_statement(f"Select instructor_username from courses where course_id = '{c_id}';")

    if res == i_uname:

        try:
            run_statement(
                f"UPDATE courses SET name = '{c_name}' WHERE instructor_username = '{i_uname}' and course_id = '{c_id}';")  # Run the query in DB

            return HttpResponseRedirect("../sites/instructorHome")
        except Exception as e:
            print(str(e))
            return render(req, 'instructorHome.html', {"action_fail": True, "username": i_uname,"exception":str(e) })
    else:
        e="This course is not belong to you."
        return render(req, 'instructorHome.html', {"action_fail": True, "username": i_uname, "exception": e})

def addCourseIns(req):
    course_id =req.POST["course id"]
    name = req.POST["name"]
    credits = req.POST["credits"]
    classroomid= req.POST["classroom ID"]
    slot = req.POST["time slot"]
    quota = req.POST["quota"]

    username = req.session["username"]  # Retrieve the username of the logged-in user
    department_id = catch_statement(f"SELECT department_id FROM instructors I WHERE I.username='{username}';")
    course_code = re.findall('\d+',course_id)[0]


    try:
        run_statement(f"INSERT INTO courses(course_id,name,classroom_id,department_id,course_code,credits, instructor_username,quota,slot) VALUES('{course_id}','{name}','{classroomid}','{department_id}',{course_code},{credits},'{username}',{quota},{slot} );")  # Run the query in DB
        return HttpResponseRedirect("../sites/instructorHome")
    except Exception as e:

        return render(req, 'instructorHome.html', {"action_fail": True, "username": username, "exception":str(e)})

def giveGrade(req):
    c_id = req.POST["course id"]
    s_id = req.POST["student id"]
    grade = req.POST["grade"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False

    res = catch_statement(f"SELECT instructor_username From courses WHERE course_id = '{c_id}'")
    if res == req.session["username"]:

        try:
            run_statement(
                f"INSERT INTO grades(grade,student_id,course_id) VALUES({grade},{s_id},'{c_id}');")  # Run the query in DB



            return HttpResponseRedirect("../sites/instructorHome")
        except Exception as e:
            print(str(e))
            return render(req, 'instructorHome.html', {"action_fail": True, "username": req.session["username"],"exception":str(e) })
    else:
        e = "This is not your course."
        return render(req, 'instructorHome.html', {"action_fail": True, "username": req.session["username"],"exception":e })

def searchName(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False
    keyword = req.POST["keyword"]


    result =  run_statement(
            f"SELECT C.course_id, C.name, I.surname, C.department_id, C.credits, C.classroom_id, C.slot, C.quota, group_concat(P.prerequisite_id order by P.prerequisite_id ASC)  as prerequisites FROM courses C INNER JOIN instructors I on I.username = C.instructor_username LEft join prerequisites P ON C.course_id = P.course_id  WHERE  C.name LIKE '%{keyword}%' group by course_id  ORDER BY course_id ASC ;")  # Run the query in DB

    return render(req, 'searchName.html', {"results": result, "action_fail": isFailed, "username": username})

def filterCourse(req):

    username = req.session["username"]  # Retrieve the username of the logged-in user
    isFailed = req.GET.get("fail", False)  # Try to retrieve GET parameter "fail", if it's not given set it to False
    did=req.POST["department id"]
    camp = req.POST["campus"]
    minc = req.POST["minimum credits"]
    maxc = req.POST["maximum credits"]


    result =  run_statement(
            f"Call filterCourse('{did}','{camp}',{minc},{maxc}) ;")  # Run the query in DB

    return render(req, 'filterCourse.html', {"results": result, "action_fail": isFailed, "username": username})

def createPost(req):
    #Retrieve data from the request body
    title=req.POST["title"]
    body=req.POST["body"]
    logged_user=req.session["username"]
    try:
        run_statement(f"CALL CreatePost('{title}','{body}','{logged_user}')")
        return HttpResponseRedirect("../sites/home")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../sites/home?fail=true')
