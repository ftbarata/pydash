from django.contrib.auth.models import User
from django.contrib.auth.models import Group as UserGroup
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from pydash.core.views import _sidebar_groups, _show_messages
from ldap3 import Server, Connection, ALL
from django.conf import settings


def _get_ldap_user_attrs_as_dict_of_lists(username, attr_list=['l']):
    server = Server(settings.LDAP_SERVER, get_info=ALL)
    conn = Connection(server, auto_bind=True)
    conn.search(settings.LDAP_SEARCH_BASE, '(uid={})'.format(username), attributes=attr_list)
    for dict_item_list in conn.response:
        if 'attributes' in dict_item_list.keys():
            return dict_item_list['attributes']


def login_user(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            username=request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            grant_user = False
            if user is not None:
                if user.is_staff or user.is_superuser:
                    grant_user = True
                else:
                    user_lotacao = _get_ldap_user_attrs_as_dict_of_lists(user, ['l'])['l'][0]
                    authorized_groups = UserGroup.objects.all()
                    for group in authorized_groups:
                        if str(group).upper() == str(user_lotacao).upper():
                            grant_user = True
                            break
                if grant_user:
                    if user is not None:
                        login(request, user)
                        context = _show_messages(10)
                        fullname = User.objects.get(username=request.POST['username']).get_short_name()
                        if fullname:
                            context.update({'status_message': 'Seja bem vindo {}.'.format(fullname)})
                        else:
                            context.update({'status_message': 'Seja bem vindo {}.'.format(user)})
                        return render(request, 'core/home.html', context)
                    else:
                        return render(request, 'auth_manager/login.html', {'status_message': 'Usuário ou senha incorreta.'})
                else:
                    return render(request, 'auth_manager/login.html', {'status_message': 'Acesso negado. Você não pertence a nenhum grupo com autorização de acesso. Entre em contato com a SUTIN/GEASI.'})
            else:
                return render(request, 'auth_manager/login.html', {'status_message': 'Acesso negado.'})
        else:
            context = _sidebar_groups()
            fullname = User.objects.get(username=request.POST['username']).get_full_name()
            context.update({'status_message': 'Seja bem vindo {}.'.format(fullname)})
            return render(request, 'core/home.html', context)

    else:
        return render(request, 'auth_manager/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'auth_manager/login.html', {'status_message': 'Você foi deslogado. Faça seu login novamente.'})
