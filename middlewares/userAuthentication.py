from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class UserAuth(BaseHTTPMiddleware):
    def __init__(
            self,
            app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/user/home/signup" and request.method == "POST":
            try:
                json_data = await request.json()
                password = json_data.get("password")
                if password:
                    import bcrypt
                    password_bytes = password.encode('utf-8')  # converting password into bytes
                    salt = bcrypt.gensalt()  # salt is used to add some extra text to the password
                    hashed_password = bcrypt.hashpw(password_bytes, salt)
                    hashed_password = hashed_password.__bytes__().decode('utf-8')
                    print(f"actual password is {password}, whereas hashed password is {hashed_password}\n")
                    request.state.hashed_password = str(hashed_password)
                    return await call_next(request)

            except Exception as error:
                print(error)
        return await call_next(request)
