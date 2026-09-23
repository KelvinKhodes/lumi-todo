from flask import Blueprint, request, Response
from app.services.authentication_service import AuthenticationService
from app.schemas.authentication_dto import UserLoginDTO, UserTokenDTO
from app.routes.wrapper.response_wrapper import wrap_data
from app.cores.logging import logger
from datetime import datetime, timedelta
from app.exceptions.authentication_exception import AuthenticationException

def create_authentication_bp(authentication_service: AuthenticationService):
    authentication_bp = Blueprint("authentications", __name__, url_prefix="/authentications")

    @authentication_bp.post("/login")
    def create_authentication():
        """Authenticate a user.
        ---
        tags:
        - Authentication
        consumes:
        - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/UserLoginDTO'
        responses:
          200:
            description: Access and refresh tokens.
            schema:
              $ref: '#/definitions/TokenResponse'
          400:
            description: Invalid request payload.
        """
        payload = request.get_json()
        authentication_create_dto = UserLoginDTO.model_validate(payload)
        logger.info(f"Creating Authentication for user with NIM: {authentication_create_dto.nim}")

        token = authentication_service.login(authentication_create_dto)

        response = Response()
        response.headers.set("Authorization", f"Bearer {token.access_token}")
        response.set_cookie(key="refreshToken", value=token.refresh_token, expires=datetime.now() + timedelta(days=7))

        return wrap_data(token), 200

        
    @authentication_bp.post("/refresh")
    def refresh_authentication_filter():
        """Refresh an access token.
        ---
        tags:
          - Authentication
        parameters:
          - in: cookie
            name: refreshToken
            type: string
            required: true
            description: Refresh token yang disimpan di Cookie
        responses:
          200:
            description: Refreshed access and existing refresh tokens.
            schema:
              $ref: '#/definitions/TokenResponse'
          401:
            description: Missing or invalid refresh token.
        """
        logger.info("Get Authentication by filter")
        refresh_token = request.cookies.get("refreshToken")

        if refresh_token is None:
            raise AuthenticationException("Missing 'refreshToken' at Request Cookies")
        
        new_access_token = authentication_service.refresh(refresh_token)

        response = Response()
        response.headers.set("Authorization", f"Bearer {new_access_token}")
        logger.debug("Success refreshing access token")

        return wrap_data(UserTokenDTO(access_token=new_access_token, refresh_token=refresh_token)), 200
    
    @authentication_bp.post("/logout")
    def delete_authentication():
        """Invalidate the current refresh token.
        ---
        tags:
          - Authentication
        parameters:
          - in: cookie
            name: refreshToken
            type: string
            required: true
        responses:
          200:
            description: Authentication session ended.
            schema:
              $ref: '#/definitions/TokenResponse'
          401:
            description: Missing or invalid refresh token.
        """
        logger.info("Get Authentication by filter")
        refresh_token = request.cookies.get("refreshToken")
    
        if refresh_token is None:
            raise AuthenticationException("Missing 'refreshToken' at Request Cookies")
            
        authentication_service.logout(refresh_token)
           
        response = Response()
        response.headers.set("Authorization", "")
        response.set_cookie(key="refreshToken", value="", expires=datetime.now())
        logger.debug("Success refreshing access token")
    
        return wrap_data(UserTokenDTO(access_token="", refresh_token="")), 200

    return authentication_bp
