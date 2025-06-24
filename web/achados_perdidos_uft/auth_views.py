"""
Views de autenticação para a API REST do sistema de Achados & Perdidos
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.decorators import api_view, permission_classes


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View customizada para obtenção de token JWT com informações adicionais
    """
    def post(self, request, *args, **kwargs):
        # Chama a implementação original para validação e geração de tokens
        response = super().post(request, *args, **kwargs)
        
        # Se a autenticação foi bem-sucedida, adiciona informações extras
        if response.status_code == 200:
            user = request.user
            response.data.update({
                'user_id': user.id,
                'username': user.username,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username,
                'is_staff': user.is_staff
            })
        
        return response


class LogoutView(APIView):
    """
    View para logout de usuários - invalida o token de refresh
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Adiciona o token de refresh à blacklist
        """
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                # Adiciona o token à blacklist
                token.blacklist()
                return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Refresh token não fornecido."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_token(request, token_id):
    """
    Endpoint para revogar um token específico pelo ID
    """
    try:
        token = OutstandingToken.objects.get(id=token_id, user=request.user)
        
        # Verifica se o token já está na blacklist
        if hasattr(token, 'blacklistedtoken'):
            return Response({"detail": "Este token já foi revogado."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Adiciona o token à blacklist
        BlacklistedToken.objects.create(token=token)
        
        return Response({"detail": "Token revogado com sucesso."}, status=status.HTTP_200_OK)
    
    except OutstandingToken.DoesNotExist:
        return Response(
            {"error": "Token não encontrado ou não pertence ao usuário."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def revoke_all_tokens(request):
    """
    Endpoint para revogar todos os tokens do usuário, exceto o atual
    """
    try:
        tokens = OutstandingToken.objects.filter(user=request.user)
        current_token_jti = request.auth.get('jti')
        
        blacklisted_count = 0
        for token in tokens:
            # Não revoga o token atual
            if token.jti != current_token_jti:
                # Verifica se o token já está na blacklist
                if not hasattr(token, 'blacklistedtoken'):
                    BlacklistedToken.objects.create(token=token)
                    blacklisted_count += 1
        
        return Response({
            "detail": f"{blacklisted_count} token(s) revogado(s) com sucesso.",
            "current_token_preserved": True
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
