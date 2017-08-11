from ldap3 import Server, Connection, ALL
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Group, Message
from django.contrib.auth.models import Group as UserGroup
from django.shortcuts import render
from django.contrib.sessions.models import Session
from pydash.profiles_manager.models import UserProfile
from pydash.mail_notifications.send_mail import send_unique_email
from .forms import MessageForm, GroupForm

def __get_ldap_user_attrs_as_dict_of_lists(username, attr_list=['l']):
    server = Server(settings.LDAP_SERVER, get_info=ALL)
    conn = Connection(server, auto_bind=True)
    conn.search(settings.LDAP_SEARCH_BASE, '(uid={})'.format(username), attributes=attr_list)
    for dict_item_list in conn.response:
        if 'attributes' in dict_item_list.keys():
            return dict_item_list['attributes']


def _sidebar_groups():
    groupdownlist, groupfaillist, groupoklist = [], [], []
    message_severity = ''
    for group in Group.objects.all():
        group_name = group.name
        severity_templist = []
        for message in group.messages.all():
            if message.severity not in severity_templist:
                severity_templist.append(message.severity)

        counter = 0
        for ms in severity_templist:
            if ms == 'alta':
                counter += 4
            elif ms == 'media':
                counter += 2
            elif ms == 'baixa':
                counter += 1
        if counter >= 4:
            message_severity = 'alta'
        elif counter == 2 or counter == 3:
            message_severity = 'media'
        elif counter == 1:
            message_severity = 'baixa'

        if not message_severity or len(severity_templist) == 0:
            message_severity = 'baixa'

        if message_severity == 'alta' and group_name not in groupdownlist:
            groupdownlist.append(group_name)
        elif message_severity == 'media' and group_name not in groupfaillist:
            groupfaillist.append(group_name)
        elif message_severity == 'baixa' and group_name not in groupoklist:
            groupoklist.append(group_name)

    for group in groupoklist:
        if group in groupfaillist or group in groupdownlist:
            groupoklist.remove(group)
    for group in groupfaillist:
        if group in groupdownlist:
            groupfaillist.remove(group)

    def group_messages_count(group_name):
        total = 0
        for group in Group.objects.get(name=group_name).messages.all():
            total += 1
        return total

    tuples_groupoklist, tuples_groupfaillist, tuples_groupdownlist = [], [], []

    for group_name in groupdownlist:
        if " " in group_name:
            tuples_groupdownlist.append((group_name, group_messages_count(group_name), group_name.replace(" ", "___")))
        else:
            tuples_groupdownlist.append((group_name, group_messages_count(group_name)))
    for group_name in groupfaillist:
        if " " in group_name:
            tuples_groupfaillist.append((group_name, group_messages_count(group_name), group_name.replace(" ", "___")))
        else:
            tuples_groupfaillist.append((group_name, group_messages_count(group_name)))
    for group_name in groupoklist:
        if " " in group_name:
            tuples_groupoklist.append((group_name, group_messages_count(group_name), group_name.replace(" ", "___")))
        else:
            tuples_groupoklist.append((group_name, group_messages_count(group_name)))

    context = {
            'tuples_groupdownlist': tuples_groupdownlist,
            'tuples_groupfaillist': tuples_groupfaillist,
            'tuples_groupoklist': tuples_groupoklist,
        }
    return context


def _show_messages(limit=0, group=''):

    def _left_zero_datetime(value):
        strnumber = str(value)
        if len(strnumber) == 1:
            return '0' + strnumber
        else:
            return strnumber

    context = _sidebar_groups()
    messages_context = []
    if limit == 0:
        if len(group) == 0:
            queryset = Message.objects.all().order_by('-updated_at')
        else:
            queryset = Group.objects.get(name=group).messages.all().order_by('-updated_at')
    else:
        if len(group) == 0:
            queryset = Message.objects.all().order_by('-updated_at')
        else:
            queryset = Group.objects.get(name=group).messages.all().order_by('-updated_at')[:limit]

    for message in queryset:
        if message:
            id = message.id
            author = message.author
            created_at = _left_zero_datetime(timezone.localtime(message.created_at).day) + '/' + _left_zero_datetime(timezone.localtime(message.created_at).month) + '/' + _left_zero_datetime(timezone.localtime(message.created_at).year) + ' - ' + _left_zero_datetime(timezone.localtime(message.created_at).hour) + ':' + _left_zero_datetime(timezone.localtime(message.created_at).minute) + ':' + _left_zero_datetime(timezone.localtime(message.created_at).second)
            severity = message.severity
            if severity == 'alta':
                header_class = 'messageheaderAlert'
            elif severity == 'media':
                header_class = 'messageheaderFail'
            else:
                header_class = 'messageheader'

            header = author + ', Criado em: ' + str(created_at)
            if User.objects.all().filter(first_name=author).exists():
                username = User.objects.get(first_name=author).last_name
            else:
                username = 'Usuário removido'
            messages_context.append({'id': id, 'message': message.message, 'detailed_message': message.detailed_message, 'header_class': header_class, 'header': header, 'username': username})
    context['items'] = messages_context
    return context


def home_page_view(request):
    if request.user.is_authenticated:
        template_name = 'core/home.html'
        session_id = request.session.session_key
        session = Session.objects.get(session_key=session_id)
        uid = session.get_decoded().get('_auth_user_id')
        user_from_session_id = User.objects.get(pk=uid)
        context = _show_messages(limit=10)
        context['user'] = user_from_session_id
        return render(request, template_name, context)
    else:
        return render(request, 'auth_manager/login.html', {'status_message': 'Faça seu login primeiro.'})


def show_message_view(request, group):
    if "___" in group:
        group = group.replace("___", " ")

    template_name = 'core/status_messages.html'

    context = _show_messages(group=group)
    return render(request, template_name, context)


def add_message_view(request):
    if request.user.is_authenticated:
        if 'is_admin' in request.session:
            if request.session['is_admin']:
                if request.method == 'POST':
                    session_id = request.session.session_key
                    session = Session.objects.get(session_key=session_id)
                    uid = session.get_decoded().get('_auth_user_id')
                    user_from_session_id = User.objects.get(pk=uid)
                    fullname = User.objects.get(username=user_from_session_id).get_short_name()
                    message_form = MessageForm(request.POST)
                    group_form = GroupForm(request.POST)

                    if message_form.is_valid() and group_form.is_valid():
                        message = message_form.cleaned_data['message']
                        detailed_message = message_form.cleaned_data['detailed_message']
                        severity = message_form.cleaned_data['severity']
                        id_groups_name_list = request.POST.getlist('groups')
                        message_instance = Message(message=message, detailed_message=detailed_message, severity=severity, author = fullname)
                        message_instance.save()
                        for gid in id_groups_name_list:
                            group_instance = Group.objects.get(pk=gid)
                            group_instance.messages.add(message_instance)


                        admin_groups = []
                        for g in UserGroup.objects.all():
                            admin_groups.append(str(g).upper())

                        notification_groups_for_this_message = []
                        for i in Message.objects.get(message=message, detailed_message=detailed_message, severity=severity, author=fullname).group_set.all():
                            notification_groups_for_this_message.append(str(i).upper())

                        user_notifications_subscribed_groups = []
                        for u in UserProfile.objects.get(username=user_from_session_id).notification_groups.all():
                            user_notifications_subscribed_groups.append(str(u).upper())

                        for user in UserProfile.objects.all():
                            if user.notification_groups.all().exists():
                                match = False
                                for x in notification_groups_for_this_message:
                                    for y in user_notifications_subscribed_groups:
                                        if x == y:
                                            ldap_attrs = __get_ldap_user_attrs_as_dict_of_lists(user.username, ['l'])
                                            lotacao = ldap_attrs['l'][0]

                                            if str(lotacao).upper() in admin_groups:
                                                mail_message = 'Mensagem: {}\n\nMensagem detalhada: {}'.format(message, detailed_message)
                                            else:
                                                mail_message = 'Mensagem: {}'.format(message)

                                            send_unique_email(subject='Alerta', message=mail_message, recipient=user.email)
                                            match = True
                                            break
                                    if match:
                                        break

                    message_form = MessageForm()
                    group_form = GroupForm()
                    sidebar_context_groups = _sidebar_groups()
                    sidebar_context_groups.update({'message_form': message_form, 'group_form': group_form, 'message_saved': 'Mensagem salva.'})
                    return render(request, 'core/new_message.html', sidebar_context_groups)
                else:
                    message_form = MessageForm()
                    group_form = GroupForm()
                    sidebar_context_groups = _sidebar_groups()
                    sidebar_context_groups.update({'message_form': message_form, 'group_form': group_form})
                    return render(request, 'core/new_message.html', sidebar_context_groups)
            return render(request, 'core/home.html', {'status_message': 'Não autorizado.'})
        else:
            return render(request, 'core/home.html', {'status_message': 'Não autorizado.'})
    else:
        return render(request, 'auth_manager/login.html', {'status_message': 'Faça seu login primeiro.'})


def delete_message_view(request, id):
    if request.user.is_authenticated:
        if 'is_admin' in request.session:
            if request.session['is_admin']:
                context = _show_messages(10)
                if request.method == 'GET':
                    session_id = request.session.session_key
                    session = Session.objects.get(session_key=session_id)
                    uid = session.get_decoded().get('_auth_user_id')
                    user_from_session_id = User.objects.get(pk=uid)
                    admin_groups = []
                    for g in UserGroup.objects.all():
                        admin_groups.append(str(g).upper())

                    notification_groups_for_this_message = []
                    for i in Message.objects.get(pk=id).group_set.all():
                        notification_groups_for_this_message.append(str(i).upper())

                    user_notifications_subscribed_groups = []
                    for u in UserProfile.objects.get(username=user_from_session_id).notification_groups.all():
                        user_notifications_subscribed_groups.append(str(u).upper())

                    for user in UserProfile.objects.all():
                        if user.notification_groups.all().exists():
                            match = False
                            for x in notification_groups_for_this_message:
                                for y in user_notifications_subscribed_groups:
                                    if x == y:
                                        ldap_attrs = __get_ldap_user_attrs_as_dict_of_lists(user.username, ['l'])
                                        lotacao = ldap_attrs['l'][0]

                                        if str(lotacao).upper() in admin_groups:
                                            message = 'Mensagem: {}\n\nMensagem detalhada: {}'.format(Message.objects.get(pk=id).message, Message.objects.get(pk=id).detailed_message)
                                        else:
                                            message = 'Mensagem: {}'.format(Message.objects.get(pk=id).message)

                                        send_unique_email(subject='Resolvido', message=message, recipient=user.email, solved=True)
                                        message = None
                                        match = True
                                        break
                                if match:
                                    break

                    Message.objects.all().get(pk=id).delete()
                    context = _show_messages(10)
                    context.update({'status_message': 'Mensagem removida.'})
                    return render(request, 'core/home.html', context)
                else:
                    return render(request, 'core/home.html', context)
        return render(request, 'core/home.html', {'status_message': 'Não autorizado.'})
    else:
        return render(request, 'auth_manager/login.html', {'status_message': 'Faça seu login primeiro.'})


def add_group_view(request):
    if request.user.is_authenticated:
        if 'is_admin' in request.session:
            if request.session['is_admin']:
                if request.method == 'POST':
                    group_name = request.POST['group_name']
                    Group.objects.create(name=group_name)
                    sidebar_context_groups = _sidebar_groups()
                    sidebar_context_groups.update({'group_created_message': 'Grupo {} criado.'.format(group_name)})
                    return render(request, 'core/new_group.html', sidebar_context_groups)
                else:
                    sidebar_context_groups = _sidebar_groups()
                    return render(request, 'core/new_group.html', sidebar_context_groups)
        return render(request, 'core/home.html', {'status_message': 'Não autorizado.'})
    else:
        return render(request, 'auth_manager/login.html', {'status_message': 'Faça seu login primeiro.'})


def del_group_view(request):
    if request.user.is_authenticated:
        if 'is_admin' in request.session:
            if request.session['is_admin']:
                if request.method == 'POST':
                    id_groups_name_list = request.POST.getlist('groups')
                    for gid in id_groups_name_list:
                        Group.objects.get(pk=gid).delete()
                    sidebar_context_groups = _sidebar_groups()
                    group_form = GroupForm()
                    sidebar_context_groups.update({'group_form': group_form})
                    sidebar_context_groups.update({'status_message': 'Grupos removidos.'})
                    return render(request, 'core/del_group.html', sidebar_context_groups)
                else:
                    group_form = GroupForm()
                    sidebar_context_groups = _sidebar_groups()
                    sidebar_context_groups.update({'group_form': group_form})
                    return render(request, 'core/del_group.html', sidebar_context_groups)
        return render(request, 'core/home.html', {'status_message': 'Não autorizado.'})
    else:
        return render(request, 'auth_manager/login.html', {'status_message': 'Faça seu login primeiro.'})


def public_home_view(request):
        template_name = 'core/home.html'
        context = _show_messages()
        return render(request, template_name, context)
