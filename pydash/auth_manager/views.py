from pydash.core.views import _show_messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as UserGroup
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from pydash.profiles_manager.models import UserProfile
from pydash.profiles_manager.forms import ProfileForm
from .helper_functions import _get_ldap_user_attrs_as_dict_of_lists


def login_user(request):
    if request.method == 'POST':
        username = ''
        if not request.user.is_authenticated:
            username=request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if not _get_ldap_user_attrs_as_dict_of_lists(user) is None:
                    user_lotacao = _get_ldap_user_attrs_as_dict_of_lists(user, ['l'])['l'][0]
                else:
                    user_lotacao = 'nogroup'

                authorized_groups = UserGroup.objects.all()
                for group in authorized_groups:
                    if str(group).upper() == str(user_lotacao).upper():
                        request.session['is_admin'] = True
                        break
            else:
                return render(request, 'auth_manager/login.html', {'status_message': 'Usuário ou senha incorreta.'})

        if 'is_admin' not in request.session:
            ldap_attrs = _get_ldap_user_attrs_as_dict_of_lists(username, ['telephoneNumber', 'l', 'mail'])
            if ldap_attrs is None:
                mail = 'usuario_removido'
                phone = 'usuario_removido'
                lotacao = 'usuario_removido'
            else:
                mail = ldap_attrs['mail'][0]
                if ldap_attrs['telephoneNumber']:
                    phone = ldap_attrs['telephoneNumber'][0]
                else:
                    phone = 'Não disponível.'

                lotacao = ldap_attrs['l'][0]

            if UserProfile.objects.filter(username=username).exists():
                form = ProfileForm(instance=UserProfile.objects.get(username=username))
            else:
                new_profile = UserProfile(username=username, email=mail, lotacao=lotacao, phone=phone,description='',photo=settings.UPLOAD_TO_PROFILE_MODEL_IMAGE_FIELD_NAME + '/' + settings.DEFAULT_IMAGE_FILENAME)
                new_profile.save()
                form = ProfileForm(instance=UserProfile.objects.get(username=username))

            request.session['can_edit_profile'] = True
            return render(request, 'profiles_manager/profile.html', {'form': form})

        context = _show_messages(10)
        fullname = User.objects.get(username=request.POST['username']).get_short_name()
        if fullname:
            context.update({'status_message': 'Seja bem vindo {}.'.format(fullname)})
        else:
            context.update({'status_message': 'Seja bem vindo {}.'.format(username)})
        return render(request, 'core/home.html', context)
    else:
        return render(request, 'auth_manager/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'auth_manager/login.html', {'status_message': 'Você foi deslogado. Faça seu login novamente.'})
