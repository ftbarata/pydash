from ldap3 import Server, Connection, ALL
from django.conf import settings


def _get_ldap_user_attrs_as_dict_of_lists(username, attr_list=['l']):
    server = Server(settings.LDAP_SERVER, get_info=ALL)
    conn = Connection(server, auto_bind=True)
    conn.search(settings.LDAP_SEARCH_BASE, '(uid={})'.format(username), attributes=attr_list)
    for dict_item_list in conn.response:
        if 'attributes' in dict_item_list.keys():
            return dict_item_list['attributes']
    return None


def _get_ldap_username_from_cn(cn):
    server = Server(settings.LDAP_SERVER, get_info=ALL)
    conn = Connection(server, auto_bind=True)
    conn.search(settings.LDAP_SEARCH_BASE, '(cn={})'.format(cn), attributes='uid')
    for dict_item_list in conn.response:
        if 'attributes' in dict_item_list.keys():
            return dict_item_list['attributes']['uid'][0]
    return None