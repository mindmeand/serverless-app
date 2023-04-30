from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.consultation import ConsultationHistoryResource, ConsultationResource, DeleteHistoryResource
from resources.user import UserImageResource, UserInfoResource, UserLoginResource, UserLogoutResource, UserRegisterResource
from resources.user import jwt_blacklist

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) : 
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api = Api(app)

# 유저 관련
api.add_resource(UserRegisterResource, '/user/register')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserLogoutResource, '/user/logout')
api.add_resource(UserImageResource, '/user/image')

api.add_resource(UserInfoResource, '/user/info')
api.add_resource(DeleteHistoryResource,'/consultation/<int:id>')

api.add_resource(ConsultationHistoryResource,'/consultation/my')

# 상담 관련
api.add_resource(ConsultationResource,'/consultation')

if __name__ == '__main__' :
    app.run()