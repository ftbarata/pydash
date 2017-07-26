from django.contrib.auth.models import User
import os
from django.conf import settings
from django.shortcuts import render
from .forms import ProfileForm
from .models import UserProfile
from pydash.auth_manager.views import _get_ldap_user_attrs_as_dict_of_lists
from django.contrib.sessions.models import Session


def profile_view(request, username=''):
    if not username:
        session_id = request.session.session_key
        session = Session.objects.get(session_key=session_id)
        uid = session.get_decoded().get('_auth_user_id')
        username = User.objects.get(pk=uid)
    ldap_attrs = _get_ldap_user_attrs_as_dict_of_lists(username, ['telephoneNumber', 'l', 'mail'])
    mail = ldap_attrs['mail'][0]
    phone = ldap_attrs['telephoneNumber'][0]
    lotacao = ldap_attrs['l'][0]
    if UserProfile.objects.filter(username=username).exists():
        form = ProfileForm(instance=UserProfile.objects.get(username=username))
    else:
        new_profile = UserProfile(username=username, email=mail, lotacao=lotacao, phone=phone, description='', photo=settings.PROFILE_IMAGES_DIR_NAME + '/' + settings.DEFAULT_IMAGE_FILENAME)
        new_profile.save()
        form = ProfileForm(instance=UserProfile.objects.get(username=username))

    if request.method == 'POST':
        if request.user.is_authenticated:
            current_photo = UserProfile.objects.get(username=username).photo
            if request.FILES:
                if os.path.isfile(str(settings.MEDIA_ROOT) + (str(current_photo))):
                    print(str(current_photo).split('/')[1])
                    if not str(current_photo).split('/')[1] == settings.DEFAULT_IMAGE_FILENAME:
                        os.remove(str(settings.MEDIA_ROOT) + (str(current_photo)))
                data = {'username': username, 'lotacao': lotacao, 'phone': phone, 'email': mail, 'description': request.POST['description'], 'photo': request.FILES['photo']}
                updated_form = ProfileForm(data, request.FILES,instance=UserProfile.objects.get(username=username))
            else:
                if 'photo-clear' in request.POST:
                    if request.POST['photo-clear'] == 'on':
                        if os.path.isfile(str(settings.MEDIA_ROOT) + (str(current_photo))):
                            print(str(current_photo).split('/')[1])
                            if not str(current_photo).split('/')[1] == settings.DEFAULT_IMAGE_FILENAME:
                                os.remove(str(settings.MEDIA_ROOT) + (str(current_photo)))
                blank_photo = UserProfile.objects.get(username=username)
                blank_photo.photo = settings.PROFILE_IMAGES_DIR_NAME + '/' + settings.DEFAULT_IMAGE_FILENAME
                blank_photo.save()
                data = {'username': username, 'lotacao': lotacao, 'phone': phone, 'email': mail,'description': request.POST['description']}
                updated_form = ProfileForm(data, instance=UserProfile.objects.get(username=username))

            if updated_form.is_valid():
                updated_form.save()
                updated_form = ProfileForm(instance=UserProfile.objects.get(username=username))
                return render(request, 'profiles_manager/profile.html',{'status_message': 'Perfil atualizado.', 'form': updated_form})
            else:
                print(form.errors)
                return render(request, 'profiles_manager/profile.html', {'status_message': 'Erro.', 'form': form, 'errors': form.errors.as_data()})
        else:
            return render(request, 'profiles_manager/profile.html', {'status_message': 'Permissão negada. Você não está autenticado.', 'form': form, 'errors': form.errors.as_data()})
    else:
        return render(request, 'profiles_manager/profile.html', {'form': form })