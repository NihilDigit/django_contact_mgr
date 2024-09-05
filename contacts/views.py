import string
from sqlite3 import IntegrityError

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from .models import User, Contact, Todo
from .forms import ContactForm, TodoForm
import random


def login_view(request):
    if request.user.is_authenticated:
        return redirect('contacts:contact_list')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('contacts:contact_list')
        else:
            messages.error(request, 'Invalid user ID or password')

    return render(request, 'login.html')


@login_required(login_url='contacts:login')
def logout_view(request):
    logout(request)
    return redirect('contacts:login')


def generate_user_id():
    # 生成一个10位的随机字符串作为user_id
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 检查所有必要字段是否都已填写
        if not all([username, email, password]):
            messages.error(request, '请填写所有必要的字段')
            return render(request, 'register.html')

        try:
            # 生成唯一的user_id
            while True:
                user_id = generate_user_id()
                if not User.objects.filter(user_id=user_id).exists():
                    break

            # 尝试创建新用户
            new_user = User.objects.create_user(
                username=username,
                user_id=user_id,
                email=email,
                password=password
            )

            # 自动登录新用户
            login(request, new_user)

            # 添加成功消息
            messages.success(request, f'注册成功！您的用户ID是 {user_id}。欢迎使用联系人管理系统。')

            # 重定向到联系人列表页面
            return redirect('contacts:contact_list')

        except IntegrityError:
            # 如果 username 已存在，显示错误消息
            messages.error(request, '用户名已被注册')
        except ValueError as e:
            # 捕获可能的 ValueError，比如 username 为空
            messages.error(request, str(e))

    return render(request, 'register.html')


def contact_list_view(request):
    print("Entering contact_list_view")
    contacts = Contact.objects.filter(user=request.user, is_blocked=False)
    print(f"Total contacts: {contacts.count()}")

    for contact in contacts:
        print(f"Contact ID: {contact.ct_id}, Name: {contact.ct_name}")

    query = request.GET.get('search')
    if query:
        contacts = contacts.filter(ct_name__icontains=query)
        print(f"Filtered contacts count: {contacts.count()}")

    paginator = Paginator(contacts, 10)  # Show 10 contacts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(f"Page number: {page_number}")
    print(f"Total pages: {paginator.num_pages}")
    print(f"Items on current page: {len(page_obj)}")

    for item in page_obj:
        print(f"Item on page - ID: {item.ct_id}, Name: {item.ct_name}")

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'contact_list.html', context)


@login_required(login_url='contacts:login')
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.ct_id = generate_unique_ct_id()
            contact.save()
            messages.success(request, '联系人添加成功！')
            return redirect('contacts:contact_list')
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})


@login_required
def edit_contact(request, ct_id):
    contact = get_object_or_404(Contact, ct_id=ct_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            if form.cleaned_data.get('delete_avatar'):
                # 删除现有头像
                if contact.avatar:
                    contact.avatar.delete()
                contact.avatar = None
            elif not form.cleaned_data.get('avatar'):
                # 如果没有上传新头像且没有选择删除，保留原有头像
                form.cleaned_data['avatar'] = contact.avatar

            form.save()
            return redirect('contacts:contact_detail', ct_id=contact.ct_id)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'edit_contact.html', {'form': form, 'contact': contact})


@login_required(login_url='contacts:login')
def contact_detail(request, ct_id):
    contact = get_object_or_404(Contact, ct_id=ct_id, user=request.user)
    return render(request, 'contact_detail.html', {'contact': contact})


@login_required(login_url='contacts:login')
def blacklist_view(request):
    contacts = Contact.objects.filter(user=request.user, is_blocked=True)
    query = request.GET.get('query')
    if query:
        contacts = contacts.filter(Q(ct_name__icontains=query) | Q(ct_phone__icontains=query))

    paginator = Paginator(contacts, 10)  # 每页显示10个联系人
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'blacklist.html', context)


@login_required(login_url='contacts:login')
def block_contact_view(request, ct_id):
    contact = get_object_or_404(Contact, ct_id=ct_id, user=request.user)
    contact.is_blocked = True
    contact.save()
    return redirect('contacts:contact_list')


@login_required(login_url='contacts:login')
def unblock_contact(request, ct_id):
    contact = get_object_or_404(Contact, ct_id=ct_id, user=request.user)
    if request.method == 'POST':
        contact.is_blocked = False
        contact.save()
        messages.success(request, '联系人已从黑名单中移除。')
    return redirect('contacts:contact_detail', ct_id=ct_id)


@login_required(login_url='contacts:login')
def delete_contact_view(request, ct_id):
    contact = get_object_or_404(Contact, ct_id=ct_id, user=request.user)
    if request.method == "POST":
        contact.delete()
        messages.success(request, "联系人已成功删除。")
        return redirect('contacts:contact_list')
    return render(request, 'delete_contact.html', {'contact': contact})


@login_required(login_url='contacts:login')
def add_todo(request, ct_id):
    contact = get_object_or_404(Contact, ct_id=ct_id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.contact = contact
            todo.created_at = timezone.now()  # 确保设置 created_at
            todo.save()
            messages.success(request, f'已为 {contact.ct_name} 添加待办事项。')
            return redirect('contacts:contact_detail', ct_id=ct_id)
    else:
        form = TodoForm()
    return render(request, 'add_todo.html', {'form': form, 'contact': contact})


@login_required(login_url='contacts:login')
def delete_todo(request, ct_id, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, contact__ct_id=ct_id, contact__user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, '待办事项已成功删除。')
    return redirect('contacts:all_todos')


@login_required(login_url='contacts:login')
def toggle_todo(request, ct_id, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, contact__ct_id=ct_id, contact__user=request.user)
    if request.method == 'POST':
        todo.completed = not todo.completed
        todo.save()
        messages.success(request, '待办事项状态已更新。')
    return redirect('contacts:contact_detail', ct_id=ct_id)


@login_required(login_url='contacts:login')
def all_todos(request):
    todos = Todo.objects.filter(contact__user=request.user).select_related('contact')
    search_query = request.GET.get('search')
    if search_query:
        todos = todos.filter(Q(event__icontains=search_query) | Q(contact__ct_name__icontains=search_query))

    sort = request.GET.get('sort', '-time')
    if sort == 'name':
        todos = todos.order_by('contact__ct_name', '-time')
    elif sort == '-name':
        todos = todos.order_by('-contact__ct_name', '-time')
    elif sort == 'time':
        todos = todos.order_by('time')
    else:
        todos = todos.order_by('-time')

    paginator = Paginator(todos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'current_sort': sort,
    }
    return render(request, 'all_todos.html', context)


def generate_unique_ct_id():
    while True:
        ct_id = ''.join(random.choices('0123456789', k=10))
        if not Contact.objects.filter(ct_id=ct_id).exists():
            return ct_id
