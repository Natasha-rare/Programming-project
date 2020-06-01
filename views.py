from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth import password_validation
# from .tokens import account_activation_token
# from .forms import *
# import json
# import vk_api
# from .models import Bot
# from virtualperson.settings import DEBUG
from os import system as shell


def signup(request):
    """
    Страница регистрации. Отправляет письмо на указанную почту со ссылкой для подтверждения

    :param request: запрос Django
    :return: форма регистрации / сообщение о подтверждении по почте
    """

    if request.method == 'POST':
        if 'username' in request.POST and 'email' not in request.POST \
                and 'password1' not in request.POST and 'password2' not in request.POST:
            username_occupation = User.objects.filter(username=request.POST['username']).exists()
            return HttpResponse(content_type='json', content=json.dumps({'username_occupation': username_occupation, }))
        if 'email' in request.POST and 'username' not in request.POST \
                and 'password1' not in request.POST and 'password2' not in request.POST:
            email_occupation = User.objects.filter(email=request.POST['email']).exists()
            return HttpResponse(content_type='json', content=json.dumps({'email_occupation': email_occupation, }))

        if 'password1' in request.POST and 'username' not in request.POST \
                and 'email' not in request.POST and 'password2' not in request.POST:
            try:
                password_validation.validate_password(request.POST['password1'])
            except:
                password_incorrect = True
            else:
                password_incorrect = False

            return HttpResponse(content_type='json', content=json.dumps({'is_password_unsafe': password_incorrect, }))

        form = SignUpForm(request.POST)
        if not form.is_valid():
            """
            Реализуется метод захвата ошибки из словаря ошибок Django и вывод ошибки пользователю.
            """
            errors = str(form.errors)
            count = 0
            mess = ''
            for i in errors:
                if i == '>':
                    count += 1
                if count == 4:
                    mess += i
                    if i == '<':
                        break
            mess = mess[1: -1]
            return render(request, 'registration/signup.html', {
                'mess': mess,
                'form': SignUpForm(),
            })

        user = form.save(commit=False)  # это точно нужно?
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Активация аккаунта'
        message = render_to_string('registration/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email],
        )
        email.send()
        return render(request, 'registration/email_activate_message.html')
    if request.method == 'GET':
        return render(request, 'registration/signup.html', {
            'form': SignUpForm(),
        })
    return HttpResponse(status=405)


def activate(request, uidb64, token):
    """
    Этот метод нужен для подтверждения адреса электронной почте. При переходе по ссылке из письма, адрес подтверждается.

    :param request: сам запрос
    :param uidb64:
    :param token: токен, отправленный в письме
    :return: страница 'Email подтверждён' / HTTP 409 'Conflict'
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'registration/email_confirmed.html', {})

    return HttpResponse('Activation link is invalid!',
                        status=409)  # 409 'Conflict' - запрос конфликтует с текущим состоянием сервера


def main(request):
    max_bot_id = Bot.objects.aggregate(Max('id')).get('id__max')
    # max_user_id = User.objects.aggregate(Max('id')).get('id__max')
    max_user_id = User.objects.count()
    if max_bot_id is None: max_bot_id = 0
    if max_user_id is None: max_user_id = 0
    return render(request, 'startpage.html', {
        'user': request.user.id,
        'count_bot_all': max_bot_id,
        'count_user': max_user_id,
        'count_bot_active': Bot.objects.count(),
    })


@login_required
def lk(request, user_id):
    """
    Личный кабинет
    :param request: запрос Django
    :param user_id: id пользователя
    :return:
    """
    if request.user.id != user_id:
        return HttpResponse(status=403, content='Forbidden')

    if request.method == 'GET':
        list_of_bots = Bot.objects.filter(owner=request.user)

        bots_one_by_three = []

        for i in range(0, len(list_of_bots), 3):
            tmp_arr = [list_of_bots[i]]
            if i + 1 < len(list_of_bots):
                tmp_arr.append(list_of_bots[i + 1])
            if i + 2 < len(list_of_bots):
                tmp_arr.append(list_of_bots[i + 2])
            bots_one_by_three.append(tmp_arr)

        return render(request, 'lk.html', {
            'id': request.user.id,
            'bots': bots_one_by_three,
        })
    elif request.method == 'DELETE':
        user = User.objects.get(pk=request.user.pk)
        user.delete()
        return HttpResponse(status=200, content='Пользователь удалён')
    return HttpResponse(status=405)

