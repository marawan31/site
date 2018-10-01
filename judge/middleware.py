from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.models import User
from judge.models import Language
from judge.models.profile import Profile
from judge.models.profile import Organization
from django.conf import settings

class ContestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            profile = request.user.profile
            profile.update_contest()
            request.participation = profile.current_contest
            request.in_contest = request.participation is not None
        else:
            request.in_contest = False
            request.participation = None
        return self.get_response(request)

class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_USER'
    def create_profile_if_not_exists(self, request):
        if hasattr(request, 'user') and type(request.user) is User:
            if not hasattr(request.user, 'email') and 'HTTP_X_USER_EMAIL' in request.META:
                email = request.META['HTTP_X_USER_EMAIL']
                request.user.email = email
                request.user.save()
            profile = None
            requiresSave = False
            if not hasattr(request.user, 'profile'):
                profile = Profile(user=request.user)
                profile.language = Language.objects.get(key='PY2')
                default_org_id = getattr(settings, 'DEFAULT_LOGIN_ORGANIZATION', 'default')
                org = None                
                try:
                    org = Organization.objects.get(key=default_org_id)
                except:
                    pass
                    
                if org:
                    profile.organizations.add(org)                
                requiresSave = True
            else:
                profile = request.user.profile
            if not profile.name and 'HTTP_X_USER_DISPLAYNAME' in request.META:
                displayName = request.META['HTTP_X_USER_DISPLAYNAME']
                profile.name = displayName
                requiresSave = True
            if requiresSave:
                profile.save()

    def process_request(self, request):
        super(CustomHeaderMiddleware, self).process_request(request)
        self.create_profile_if_not_exists(request)
