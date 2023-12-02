from django import forms
from .models import User, Student, Admin, Book, Category, UserProfile, BookReturn
from django.contrib.auth.forms import UserCreationForm 


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']

        

class AdminRegistrationForm(UserCreationForm):
    

    username=forms.CharField(
        widget = forms.TextInput(
            attrs={
                #'placeholder':"Your username"
            }
        )
    )
    password1=forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #'placeholder':"Your password1"
            }
        ), label= "Password"
    )
    password2=forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #'placeholder':"Confirm Your password"
            }
        ), label= "Confirm Password"
    )
    email=forms.CharField(
        widget = forms.TextInput(
            attrs={
                #'placeholder':"Your email"
            }
        )
    )

    class Meta:
        model = User
        fields =('username', 'email','password1','password2')
        
class StudentRegistrationForm(UserCreationForm):
    
    grade = forms.ChoiceField(choices=[('ND1', 'ND1'), ('ND2', 'ND2'), ('ND3', 'ND3'), ('HND1','HND1'), ('HND2','HND2'), ('HND3','HND3'), ('100L','100L'), ('200L','200L'), ('300L','300L'), ('400L','400L'), ('500L','500L'),], label="Your Level")


    username=forms.CharField(
        widget = forms.TextInput(
            attrs={
                'placeholder':"Write your full name"
            }
        ), 
    )
    mat_number=forms.CharField(
        widget = forms.TextInput(
            attrs={
                #'placeholder':"Your username"
            }
        ), 
    )
    password1=forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #'placeholder':"Your password1"
            }
        ), label= "Password"
    )
    password2=forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #'placeholder':"Confirm Your password"
            }
        ), label= "Confirm Password"
    )
    email=forms.CharField(
        widget = forms.TextInput(
            attrs={
                #'placeholder':"Your email"
            }
        )
    )
    
    
    class Meta:
        model = User
        fields = ('username', 'password1','password2', 'email','grade')

class StaffRegistrationForm(UserCreationForm):
    
    staff_role = forms.ChoiceField(choices=[('Lecturer', 'Lecturer'), ('Professor', 'Professor'), ('Non-Academic-Staff', 'Non-Academic-Staff'),], label="Staff Role")


    username=forms.CharField(
        widget = forms.TextInput(
            attrs={
                'placeholder':"Write your full name with underscore"
            }
        ), 
    )
    password1=forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #'placeholder':"Your password1"
            }
        ), label= "Password"
    )
    password2=forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                #'placeholder':"Confirm Your password"
            }
        ), label= "Confirm Password"
    )
    email=forms.CharField(
        widget = forms.TextInput(
            attrs={
                #'placeholder':"Your email"
            }
        )
    )
    
    
    class Meta:
        model = User
        fields = ('username', 'password1','password2', 'email','staff_role')

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This student ID is already in use.")
        return student_id
    

class CustomLoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput, max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    # You can add any additional fields you need here

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BookForm(forms.ModelForm):
    
    available_copies = forms.IntegerField(label='New Quantity',min_value=0,)
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'category','available', 'available_copies']  # Add other fields here
        widgets = {
            'available': forms.HiddenInput(),  # Hide the availability field for form submission
            
        }


class QuantityUpdateForm(forms.Form):
    increase_quantity = forms.IntegerField(min_value=0, required=False)
    decrease_quantity = forms.IntegerField(min_value=0, required=False)



class BookReturnForm(forms.ModelForm):
    class Meta:
        model = BookReturn
        fields = ['book']



class BookSearchForm(forms.Form):
    query = forms.CharField(
        label="Search Books",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by Book Name, Author, or Category'}),
    )
class StudentSearchForm(forms.Form):
    search_query = forms.CharField(label='Search by Name or Student ID', max_length=100)


class UpdateAvailabilityForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput)
    new_availability = forms.IntegerField(label='New Availability')





