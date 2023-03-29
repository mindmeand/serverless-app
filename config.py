
class Config :
    HOST = 'yh-104db.ce4cnusg3buq.ap-northeast-2.rds.amazonaws.com'
    DATABASE = 'mindmeand'
    DB_USER = 'mindmeand_db_user'
    DB_PASSWORD = 'yh1234db'

    SALT = 'dskj29jcdn12jn'

    # JWT 관련 변수를 셋팅
    JWT_SECRET_KEY = 'yhacdemy20230105##hello'
    JWT_ACCESS_TOKEN_EXPIRES = False # 만료없이 설정
    PROPAGATE_EXCEPTIONS = True # 에러가 나면 보여줄것

    # openAI SecretKey
    openAIKey="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"