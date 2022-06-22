from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home',views.homePage,name="homePage"),
    path('studentHome',views.studentHome,name="studentHome"),
    path('instructorHome', views.instructorHome, name="instructorHome"),
    path('managerHome', views.managerHome, name="managerHome"),
    path('studentLogin',views.studentLogin,name="studentLogin"),
    path('instructorLogin', views.instructorLogin, name="instructorLogin"),
    path('managerLogin', views.managerLogin, name="managerLogin"),
    path('listAllCourses', views.listAllCourses, name="listAllCourses"),
    path('addNewStudent', views.addNewStudent, name="addNewStudent"),
    path('addNewInstructor', views.addNewInstructor, name="addNewInstructor"),
    path('addCourse', views.addCourse, name="addCourse"),
    path('deleteStudent', views.deleteStudent, name="deleteStudent"),
    path('updateTitle', views.updateTitle, name="updateTitle"),
    path('viewStudents', views.viewStudents, name="viewStudents"),
    path('viewInstructors', views.viewInstructors, name="viewInstructors"),
    path('viewAllGrades', views.viewAllGrades, name="viewAllGrades"),
    path('viewAllCourses', views.viewAllCourses, name="viewAllCourses"),
    path('viewAverageGrade', views.viewAverageGrade, name="viewAverageGrade"),
    path('availableClassroom', views.availableClassroom, name="availableClassroom"),
    path('addPre', views.addPre, name="addPre"),
    path('viewOwnCourses', views.viewOwnCourses, name="viewOwnCourses"),
    path('viewOwnStudents', views.viewOwnStudents, name="viewOwnStudents"),
    path('updateCourseName', views.updateCourseName, name="updateCourseName"),
    path('addCourseIns', views.addCourseIns, name="addCourseIns"),
    path('giveGrade', views.giveGrade, name="giveGrade"),
    path('searchName', views.searchName, name="searchName"),
    path('filterCourse', views.filterCourse, name="filterCourse"),
    path('listCurrentlyTakingCourses', views.listCurrentlyTakingCourses, name="listCurrentlyTakingCourses"),
    path('createPost',views.createPost,name="createPost")
]