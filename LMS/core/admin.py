from django.contrib import admin
from .models import User, Student, Admin, Book, BookRequest, Category, UserProfile, BookReturn,Staff

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Book)
admin.site.register(BookRequest)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(BookReturn)
admin.site.register(Staff)

