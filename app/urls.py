from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuoteListView.as_view(), name='index'),
    path('quote/<int:id>/', views.QuoteDetailView.as_view(), name='quote'),
    path('quote/create/', views.QuoteCreateView.as_view(), name='quote_create'),
    path('quote/<int:id>/update/', views.QuoteUpdateView.as_view(), name='quote_update'),
    path('quote/<int:id>/delete/', views.QuoteDeleteView.as_view(), name='quote_delete'),
    path('today/', views.TodayQuoteView.as_view(), name='today_quote'),
    
    # Authentication URLs
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]