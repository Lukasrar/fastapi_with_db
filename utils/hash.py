from passlib.context import CryptContext


SECRET_KEY = '57c0a5eff8dbd9dac9300be80102cb32c0dc19bdd507491a866c3be645882ed7'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def HashPassword(password: str):
   return bcrypt_context.hash(password)

def VerifyPassword(password: str, hashedPassword: str):
   return bcrypt_context.verify(password, hashedPassword)