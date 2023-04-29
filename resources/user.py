from datetime import datetime
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error
from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password

# 회원가입
class UserRegisterResource(Resource) :
    def post(self) :
        # { "name": "김이름",
        # "birthDate": "19980101",
        # "email": "abc@naver.com",
        # "password": "12345" }

        data = request.get_json()

        try :
            validate_email( data["email"] )
        except EmailNotValidError as e :
            print(str(e))
            return {'error' : str(e)}, 400

        if len(data["password"]) < 4 or len(data["password"]) > 20 :
            return {'error' : '비밀번호 길이 확인'}, 400

        hashed_password = hash_password(data["password"])
        print(hashed_password)

        try :
            connection = get_connection()
            query = '''insert into user
                    (name, birthDate, email, password)
                    values
                    (%s, %s, %s, %s);'''
            
            record = (data["name"], data["birthDate"], data["email"], hashed_password)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            user_id = cursor.lastrowid



        except Error as e :
            print(e)
            return {"error" : str(e)}, 500

        finally:
            cursor.close()
            connection.close()

        access_token = create_access_token(user_id)
        return {"result" : "success", "access_token" : access_token}, 200

# 로그인
class UserLoginResource(Resource) :
    def post(self) :
        # {"email": "abc@naver.com",
        # "password": "1234"}

        data = request.get_json()

        try :
            connection = get_connection()

            query = '''select *
                    from user
                    where email = %s ;'''

            record = (data["email"], )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            if len(result_list) == 0 :
                return {"error" : "회원가입한 사람이 아닙니다"} , 400

            i = 0
            for row in result_list :
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
                i = i + 1



        except Error as e :
            print(e)

            return {"error" : str(e)}, 500
        
        finally:
            cursor.close()
            connection.close()


        check = check_password( data['password'], result_list[0]['password'] )

        if check == False :
            return {"error" : "비밀번호가 일치하지 않습니다"} , 400

        access_token = create_access_token( result_list[0]['id'] )

        return {"result" : "success", "access_token" : access_token}, 200

jwt_blacklist = set()
# 로그아웃
class UserLogoutResource(Resource) :
    @jwt_required()
    def post(self) :
        
        jti = get_jwt()['jti']
        print(jti)

        jwt_blacklist.add(jti)

        return {'result' : 'success'}, 200

# 유저 정보 조회
class UserInfoResource(Resource) :
    @jwt_required()
    def get(self) :
        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''select name, birthDate, email
                    from user
                    where id = %s ;'''

            record = ( user_id, )

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()


        except Error as e :
            print(e)


        finally:
            cursor.close()
            connection.close()

        

            return {"result" : "fail", "error" : str(e)}, 500

        if len(result_list) == 0 :
            return {"error" : "잘못된 유저 아이디 입니다"}, 400

        return {"result" : "success", "user" : result_list[0]}, 200

# 유저 정보 수정
    @jwt_required()
    def put(self) :
        # {"name": "김이름",
        # "birthDate": "19980101",
        # "email": "abc@naver.com"}
        
        data = request.get_json()
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            connection.begin()

            query = ''' update user
                    set
                    name = %s,
                    birthDate = %s,
                    email = %s
                    where id = %s; '''

            record = (data['name'], data['birthDate'], data['email'], user_id)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()



        except Error as e :
            connection.rollback()
            print(e)
        finally:
            cursor.close()
            connection.close()

            return {"result" : "fail", "error" : str(e)}, 500

        return {"result" : "success"}, 200
    
    # 유저 정보 삭제 (회원 탈퇴)
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            connection.begin()

            query = '''DELETE FROM user
                    WHERE id = %s;'''

            record = (user_id,)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

        except Error as e:
            connection.rollback()
            print(e)
            return {"result": "fail", "error": str(e)}, 500
        finally:
            cursor.close()
            connection.close()

        return {"result": "success"}, 200