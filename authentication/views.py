from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST,
    HTTP_226_IM_USED
)


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes((AllowAny,))
def user_registration(request):
    try:
        data = request.data
        email = data.get('email')
        username = data.get('username')
        first_name = data.get('full_name')
        password = data.get('password')

        try:  
            user_object = User.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                is_staff=True
            )
            user_object.set_password(password)
            user_object.save()

            token = Token.objects.create(user=user_object)
            print("TOKEN", token)
            return Response({"token": {token.key}},status=HTTP_200_OK)
        except Exception as error:
            print("Error>>>>>>>", error)
            return Response({"message": error}, status=HTTP_226_IM_USED)
            
    except Exception as error:
        print(error)
        return Response({"Error": error}, status=HTTP_400_BAD_REQUEST)



# {
# "emai" : "puushkar@gmail.com",
# "username" : "puushkar@gmail.com",
# "first_name" : "aditya",
# "password" :"pushkarismalik!@####1234"
# }