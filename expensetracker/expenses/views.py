from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        
       
        login(request, user)
        
        messages.success(request, "Registration successful. Logged in automatically.")
        return redirect('expense_list')  

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('expense_list')  # Ensure this route exists
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expense_list.html', {'expenses': expenses})


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully.")
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'expense_form.html', {'form': form})


@login_required
@login_required
def expense_update(request, expense_id):
    expense = Expense.objects.filter(id=expense_id, user=request.user).first()
    
    if not expense:
        messages.error(request, "Expense not found.")
        return redirect('expense_list')  # Redirect if the expense is missing

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expense_form.html', {'form': form})


@login_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
        return redirect('expense_list')

    return render(request, 'expense_confirm_delete.html', {'expense': expense})
