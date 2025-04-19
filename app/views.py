from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.utils import timezone

from .models import Quote
from .tasks import task_do_something


class QuoteListView(ListView):
    model = Quote
    template_name = "index.html"
    context_object_name = "quotes"


class QuoteDetailView(DetailView):
    model = Quote
    template_name = "preview.html"
    context_object_name = "quote"
    pk_url_kwarg = 'id'


class QuoteCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "form.html")

    def post(self, request):
        text = request.POST.get("text")
        author = request.POST.get("author")
        source = request.POST.get("source", "")
        is_featured = request.POST.get("is_featured", "") == "on"

        task_do_something()  # berjalan di background -> Queue (Antrian)

        Quote.objects.create(
            text=text, 
            author=author, 
            source=source, 
            is_featured=is_featured, 
            user=request.user
        )
        return redirect("index")


class QuoteUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        quote = get_object_or_404(Quote, id=id)
        # Memeriksa apakah pengguna yang sedang login adalah pemilik quote
        if quote.user != request.user:
            messages.error(request, "Anda tidak memiliki izin untuk mengedit quote ini.")
            return redirect("index")
        context = {"quote": quote}
        return render(request, "form.html", context)

    def post(self, request, id):
        quote = get_object_or_404(Quote, id=id)
        # Memeriksa apakah pengguna yang sedang login adalah pemilik quote
        if quote.user != request.user:
            messages.error(request, "Anda tidak memiliki izin untuk mengedit quote ini.")
            return redirect("index")
        quote.text = request.POST.get("text")
        quote.author = request.POST.get("author")
        quote.source = request.POST.get("source", "")
        quote.is_featured = request.POST.get("is_featured", "") == "on"
        quote.save()
        return redirect("quote", id=id)


class QuoteDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        quote = get_object_or_404(Quote, id=id)
        # Memeriksa apakah pengguna yang sedang login adalah pemilik quote
        if quote.user != request.user:
            messages.error(request, "Anda tidak memiliki izin untuk menghapus quote ini.")
            return redirect("index")
        quote.delete()
        return redirect("index")


class TodayQuoteView(View):
    def get(self, request):
        today = timezone.now().date()
        
        # Coba ambil quote yang terfeatured
        featured_quote = Quote.objects.filter(is_featured=True).first()
        
        # Jika tidak ada quote yang terfeatured, ambil quote paling baru
        quote_of_the_day = featured_quote or Quote.objects.first()
        
        context = {"quote": quote_of_the_day, "today": today}
        return render(request, "today.html", context)


# Authentication Views
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'auth/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'auth/login.html')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'auth/register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, 'auth/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'auth/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'auth/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f"Welcome to Quotes App, {username}! Your account has been created.")
        return redirect('index')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully")
        return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_quotes = Quote.objects.filter(user=request.user)
        context = {
            'user_quotes': user_quotes
        }
        return render(request, 'auth/profile.html', context)
