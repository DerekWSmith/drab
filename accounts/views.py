from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.modelfolder import Library, Tag
from .serializers import RegisterUserSerializer

'''
This file is about Users from ana ccount perspective

There is another file in core.viewfolder, which handles users in terms of band membership .


'''


User = get_user_model()


class RegisterUser(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        """
        Return JWT tokens on successful registration of new user.
        """
        # creates the user record
        response = super().create(request, *args, **kwargs)
        #  retrieves the new user record
        user = User.objects.get(email=request.data.get('email'))
        # the library display depends on the preferred_name
        # As we are just created, we don't have a preferred name: Copy the email across
        user.preferred_name = 'My Library'
        user.save()

        # we need to delegate the users library to the user
        Library.objects.create(user_id=user.id, library_id=user.id, active=True)




        # we also need to add some default tags for the library
        tags_to_copy = Tag.objects.filter(library=None)
        for tag in tags_to_copy:
            # Create a copy of the tag with new user ID as library tag
            tag_copy = Tag.objects.create(
                library_id=user.id,
                tag=tag.tag,
                icon=tag.icon,
                file=tag.file,
                active=True,
            )

        tokens = RefreshToken.for_user(user)
        response.data = {
            'refresh': str(tokens),
            # IDE reports an issue with access_token.  in reality, no issue exists
            'access': str(tokens.access_token),
        }
        return response


class TokenObtainPairViewUpdateLastLogin(TokenObtainPairView):
    """
    Override TokenObtainPairView to update last_login field.
    And to return user/delegate details
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data.get('email'))

        user_data = {
            'id': user.id,
            'email': user.email,
            'last_login': user.last_login,
            'is_school': user.is_school,
            'subscription': user.subscription,
            'subscription_active': user.subscription_active,
            'subscription_renewal_date': user.subscription_renewal_date,
            'subscription_notes': user.subscription_notes,
            'contact_details': user.contact_details,
            'preferred_name': user.preferred_name,
            'library_name': user.library_name(),
        }

        library_data = []

        delegates = Library.objects.filter(user=user)
        for d in delegates:
            # if d.user != d.library:  # Check if it's a non-recursive delegation
            delegate_user = User.objects.get(id=d.library_id)
            if d.is_library_valid():
                library_data.append({
                    'id': d.id,
                    'user_id': d.user_id,
                    'library_id': d.library_id,
                    'active': d.active,
                    'start_date': d.start_date,
                    'end_date': d.end_date,
                    'library_name' : delegate_user.library_name(),
                    'library_owner_name': delegate_user.preferred_name,
                    'library_owner_email': delegate_user.email,
                    'delegation_valid': d.is_library_valid()
                })

        response.data['user'] = user_data
        response.data['libraries'] = library_data

        user_logged_in.send(sender=user.__class__, request=request, user=user)

        return response


