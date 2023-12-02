from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, AdminRegistrationForm, BookForm, CustomLoginForm, BookSearchForm, UserProfileForm
from .models import Book, Admin, Student, BookRequest, Category, UserProfile, BookReturn, Staff
from django.contrib import messages
from .forms import CategoryForm, StudentSearchForm, UpdateAvailabilityForm, QuantityUpdateForm, BookReturnForm, StaffRegistrationForm
from django.db.models import Q 


def categories(request):
    categories = Category.objects.all()
    return render(request, 'core/categories.html', {'categories': categories})

def category_books(request, category_id):
    category = Category.objects.get(pk=category_id)
    books = Book.objects.filter(category=category)
    return render(request, 'core/category_list.html', {'category': category, 'books': books})

@login_required
def request_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # Check if the book is available
    if not book.available:
        messages.error(request, 'This book is not available for request.')
    else:
        # Check if the student has already requested this book
        existing_request = BookRequest.objects.filter(student=request.user, book=book, is_approved=False).first()
        if existing_request:
            messages.warning(request, 'You have already requested this book.')
        else:
            # Create a book request
            book_request = BookRequest(student=request.user, book=book)
            book_request.save()
            messages.success(request, 'Book request sent successfully.')

    return redirect('request_book')

@login_required
def approved_books(request):
    student = request.user
    approved_requests = BookRequest.objects.filter(student=student, is_approved=True)
    returned_books = BookReturn.objects.all()
    approved_books = [request.book for request in approved_requests if request.book not in returned_books]

    return render(request, 'core/approved_books.html', {'approved_books': approved_books, 'returned_books': returned_books})





def view_requests(request):  
    if not request.user.is_admin:
        return redirect('login')
    requests = BookRequest.objects.filter(is_approved=False)
    return render(request, 'core/view_requests.html', {'requests': requests})


def approve_request(request, request_id):
    if not request.user.is_admin:
        return redirect('login')
    book_request = BookRequest.objects.get(pk=request_id)
    book_request.is_approved = True
    book_request.book.available_copies -= 1  # Decrement available copies when approved
    book_request.book.save()
    book_request.save()
    # Optionally, add a success message
    messages.success(request, 'Book request approved.')
    return redirect('view_requests')

def available_books(request):
    books = Book.objects.filter(available=True)
    return render(request, "core/request.html", {'books': books})


def index(request):
    return render(request, "core/index.html")

def about(request):
    return render(request, "core/about.html")

def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_student = True
            user.save()
            student = Student(user=user)
            student.save()
            login(request, user)
            return redirect('student_dashboard')  
    else:
        form = StudentRegistrationForm()
    return render(request, 'core/student_registration.html', {'form': form})

def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            staff = Staff(user=user)
            staff.save()
            login(request, user)
            return redirect('staff_dashboard')  
    else:
        form = StaffRegistrationForm()
    return render(request, 'core/staff_registration.html', {'form': form})

def admin_registration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_admin = True
            user.save()
            admin = Admin(user=user)
            admin.save()
            login(request, user)
            return redirect('admin_dashboard')  
    else:
        form = AdminRegistrationForm()
    return render(request, 'core/admin_registration.html', {'form': form})


def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('login')
    quantity_form = QuantityUpdateForm()

    if quantity_form.is_valid():
        book_id = request.POST.get('book_id')
        increase_quantity = form.cleaned_data['increase_quantity']
        decrease_quantity = form.cleaned_data['decrease_quantity']

        book = Book.objects.get(pk=book_id)

        if increase_quantity:
            book.available_copies += increase_quantity
        elif decrease_quantity:
            book.available_copies -= decrease_quantity
        
        quantity_form
        book.save()
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            
              
            form.save()
            return redirect('admin_dashboard')
        
            
    else:
        form = BookForm()

    books = Book.objects.all()
    context = {'form': form, 'books': books, "quantity_form":quantity_form}
    return render(request, 'core/admin_dashboard.html', context)

    #elif request.user.is_student:
        # Student-specific features
        #return render(request, 'core/student_dashboard.html')


def update_availability(request, book_id):
    if not request.user.is_admin:
        return redirect('login')

    book = get_object_or_404(Book, pk=book_id)
    book.available = not book.available
    book.save()
    return redirect('admin_dashboard')


def user_login(request):
    form = CustomLoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)
            if user is not None:
                if user.is_admin == True:
                    login(request, user)
                    return redirect('admin_dashboard')
                if user.is_student == True:
                    login(request, user)
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()

    return render(request, 'core/login.html', {'form': form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    # Optionally, add a success message
    messages.success(request, 'Book deleted successfully.')
    return redirect('admin_dashboard') 


def student_dashboard(request):
    available_books = Book.objects.filter(available=True)
    unavailable_books = Book.objects.filter(available=False)
    student = Student.objects.get(user=request.user)
    student_id = student.student_id
    context = {
        'available_books': available_books,
        'unavailable_books': unavailable_books,
        'student_id':student_id,
    
    }
    return render(request, 'core/student_dashboard.html', context)

def staff_dashboard(request):
    available_books = Book.objects.filter(available=True)
    unavailable_books = Book.objects.filter(available=False)
    staff = Staff.objects.get(user=request.user)
    staff_role = staff.staff_role
    context = {
        'available_books': available_books,
        'unavailable_books': unavailable_books,
        'staff_role':staff_role,
    
    }
    return render(request, 'core/staff_dashboard.html', context)

def librarian_add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_category')
    else:
        form = CategoryForm()

    return render(request, 'core/add_category.html', {'form': form})


def search_books(request):
    form = BookSearchForm(request.GET)
    query = request.GET.get('query')
    books = []

    if query:
        # Perform the search based on the query
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, 'core/search.html', {'form': form, 'query': query, 'books': books})

def search_students(request):
    if request.method == 'POST':
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Perform the search
            students = UserProfile.objects.filter(user__username__icontains=search_query) | \
                       UserProfile.objects.filter(student_id__icontains=search_query)
        else:
            students = UserProfile.objects.none()
    else:
        form = StudentSearchForm()
        students = UserProfile.objects.none()

    return render(request, 'core/search_student.html', {'form': form, 'students': students})

def user_profile(request):
    # Get the user's profile or create one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'core/user_profile.html', {'profile': profile})

def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Check if a new profile picture was provided
            new_profile_picture = form.cleaned_data.get('profile_picture')
            if not new_profile_picture:
                # No new picture provided, keep the existing one (or the default)
                form.cleaned_data['profile_picture'] = profile.profile_picture
            form.save()
            return redirect('user_profile')

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'core/edit_user_profile.html', {'form': form, 'profile': profile})

def view_all_students(request):
    # Fetch all student profiles
    students = UserProfile.objects.all()
    
    return render(request, 'view_all_students.html', {'students': students})


def update_available_copies(request, book_id):
    if not request.user.is_admin:
        return redirect('login')
            
    action = request.POST.get('action')

    book = get_object_or_404(Book, pk=book_id)
    if action == 'increment':
        book.available_copies += 1
    elif action == 'decrement':
        book.available_copies -= 1

    book.save()


    return redirect('admin_dashboard')

def student_returns(request):
    returns = BookReturn.objects.filter(student=request.user)
    return render(request, 'core/student_return.html', {'returns': returns})

def return_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    
    # Check if the student has previously returned this book
    if BookReturn.objects.filter(book=book, student=request.user).exists():
        return redirect('student_returns')

    # Create a book return record
    book_return = BookReturn(book=book, student=request.user)
    book_return.returned=True
    book_return.save()

    # Increase the available copies of the book
    book.available_copies += 1
    book.save()
    
    return redirect('student_returns')









