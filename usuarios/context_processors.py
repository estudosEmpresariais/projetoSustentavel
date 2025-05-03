

def dados_globais(request):
    return {
        'user_id': request.META.get('REMOTE_ADDR'),
        'username': request.user,
    }