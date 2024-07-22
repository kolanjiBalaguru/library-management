from django.shortcuts import render,redirect
from .form import CustomUserForm
# from app.form import CustomUserForm
from app.models import *
from django.contrib.auth.models import User
# from django.contrib.auth import get_user
# from django.http import HttpResponse,JsonResponse
# from rest_framework.decorators import api_view
# from app.models import Book_Login
from django.contrib.auth import authenticate,login
from datetime import datetime, timedelta
from django.db import transaction
# Create your views here.

def home(request):
    return render(request,'home.html')
def signup(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        query_dict = request.POST
        username = query_dict.get('username')
        email =  query_dict.get('email')
        if form.is_valid():
            print(1)
            form.save()
            admin_user = User.objects.filter(email=email).first()
            user_id = admin_user.id
            print(user_id)
            user_details = StudentDetails(username = username,email = email,user_id = user_id)
            user_details.save()
            return redirect('userlogin')
    return render(request,'student_register.html',{'form':form})

def studentlogin(request):
    print(1)
    if request.method=='POST':
        print(2)
        name=request.POST.get('Name')
        pwd=request.POST.get('Password')
        print(name)
        print(pwd)
        try:
            user=authenticate(request,username=name,password=pwd)
            print(1)
            if user is not None:
                print(2)
                login(request,user)
                print(3)
                user_id = request.user.id
            print(4)
            student=StudentDetails.objects.filter(user_id = user_id).first()
            print(student)
            print(5)
            if student.status==1:
                print(5.5)
                return redirect('take')
            else:
                print(6)
                return redirect ('student_login')

        except:
            pass
    return render(request,'student_login.html')

def adminlogin(request):
    print(1)
    if request.method=='POST':
        print(2)
        name=request.POST.get('Name')
        pwd=request.POST.get('Password')
        print(name)
        print(pwd)
        try:
            print(3)
            user=authenticate(request,username=name,password=pwd)
            print(user)
            print(4)
            if user is not None:
                print(5)
                login(request,user)
                print(6)
                return redirect('Bookdetails')
            else:
                print(7)
                return redirect ('admin_login')

        except:
            pass
    return render(request,'admin_login.html')

def Bookdetails(request):
    obj=BookDetails.objects.all()
    return render(request,'Bookdetails.html',{'obj':obj})

def take(request):
    return render(request,'take.html')
    
def lib(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            date = datetime.now().date()
            library=BookDetails.objects.create(name=request.POST.get('Name'),book_code=request.POST.get('Code'),author_name=request.POST.get('Author'),
                                            date=request.POST.get('Date'),status=request.POST.get('Status'),amount=request.POST.get('Amount'),
                                            created_date=date,created_by=user_id,available_books = request.POST.get('available_books'),
                                            book_img = request.FILES['updatebook'])
            return redirect("Bookdetails")
        else:
            return redirect("book")
    return render(request, 'book.html')

def updatebook(request,pk):
    obj=BookDetails.objects.get(id=pk)
    if request.method=='POST':
        library = BookDetails.objects.filter(id=pk).first()
        library.name = request.POST.get('Name')
        library.book_code = request.POST.get('Code')
        library.author_name = request.POST.get('Author')
        library.date = request.POST.get('Date')
        library.amount = request.POST.get('Amount')
        library.available_books = request.POST.get('available_books')
        library.book_img = request.FILES['updatebook']
        date = datetime.now().date()
        library.updated_date = date
        library.save()
        return redirect('Bookdetails')
    return render(request,'updatebook.html',{'obj':obj})

def deletebook(request,pk):
    obj=BookDetails.objects.filter(id=pk).delete()
    return redirect('Bookdetails')

def take(request):
    obj = BookDetails.objects.all()
    if request.method=='POST':
        aa=request.POST.get('search')
        bb=request.POST.get('searchcode')
        if bb =='':
            obj  = BookDetails.objects.filter(name=aa)
            
        if aa == '':
            obj = BookDetails.objects.filter(book_code=bb)
        if aa != '' and bb != '':
             obj = BookDetails.objects.filter(book_code=bb,name =aa)

        
    return render(request,'take.html',{'obj':obj})

@transaction.atomic()
def takebook(request,pk):
        if request.user.is_authenticated:
            user_id = request.user.id
            date = datetime.now().date()
            book_id = pk
            book_details = BookDetails.objects.filter(id = book_id).first()
            if book_details.available_books != 0:
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                book_quantity = book_details.available_books
                user_details = StudentDetails.objects.filter(user_id = user_id).first()
                #Amount Reduction
                user_amount = user_details.wallet_balance
                current_amount = user_amount - book_price
                user_details.wallet_balance = current_amount
                user_details.save()
                
                #Book History Registeration
                student = StudentDetails.objects.filter(user_id = user_id).first()
                student_id = student.id
                book_history = Booktransferhistory(student_id = student_id,code = book_code,
                                                    book_name = book_name,status = "Take")
                book_history.save()
                    
                #UserBookstatus Registeration
                status = UserBookStatus(student_id=student_id,book_id = book_id)
                status.save()

                #UserBookDetails Registeration
                user = UserBookDetails.objects.filter(student_id = student_id).first()
                if user is  None:
                    user_book_details = UserBookDetails(student_id = student_id,
                                                books_quantity = 1,updated_at = date)
                    user_book_details.save()
                else:
                    user_update = UserBookDetails.objects.filter(student_id = student_id).first()
                    books_quantity = user_update.books_quantity 
                    quantity = int(books_quantity) +1
                    user_update.books_quantity = quantity
                    user_update.save()

                #Books reduction in BookDetails
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity-=1

                book_details.available_books = quantity
                if quantity == 0:
                    book_details.status = 'Unavailable'
                book_details.save()
            else:
                print("No stocks")
            return redirect('take')
        
@transaction.atomic()
def retainbook(request,pk):
    if request.user.is_authenticated:
        user_id = request.user.id
        book_id = pk
        student = StudentDetails.objects.filter(user_id = user_id).first()
        student_id = student.id
        user_book = UserBookStatus.objects.filter(student_id=student_id,book_id=book_id).first()
        if user_book is not None:
            if user_book.status == 1:
                date = datetime.now().date()
                    
                #Details
                book_details = BookDetails.objects.filter(id = book_id).first()
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                book_quantity = book_details.available_books

                #Book History Registeration
                student = StudentDetails.objects.filter(user_id = user_id).first()
                student_id = student.id
                book_history = Booktransferhistory(student_id = student_id,code = book_code,
                                                    book_name = book_name,status = "Return")
                book_history.save()

                # books reduction
                books_reduction = UserBookDetails.objects.filter(student_id = student_id).first()
                book_quantity = books_reduction.books_quantity
                quantity = book_quantity-1
                books_reduction.books_quantity = quantity
                books_reduction.save()

                #books updation
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity+=1
                book_details.available_books = quantity
                if quantity !=0:
                    book_details.status = 'Available'
                book_details.save()
                user_book.status = 0
                user_book.delete()
            else:
                print("you dont have book so you are not able to return")

        else:
            print("please purchase book")


                
    return redirect('take')
   
   
@transaction.atomic()
def add_cash(request):
    all_students=StudentDetails.objects.all()
    print(21)
    if request.method=='POST':
        print(22)
        student_id=request.POST.get('member_id')
        print(23)
        add_amount=request.POST.get('new_amount')
        print(24)
        add_amt=float(add_amount)
        print(25)
        if student_id is not None:
            print(26)
            student_data=StudentDetails.objects.filter(user_id=student_id).first()
            print(27)
            student_amt=student_data.wallet_balance+add_amt
            print(28)
            student_data.wallet_balance=student_amt
            print(29)
            student_data.save()
            print(30)
            return redirect("Bookdetails")
        else:
            return redirect("add_cash")
        return render(request,'add_cash.html')  
    else:
        return render(request,'add_cash.html') 

    

    