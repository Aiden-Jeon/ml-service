from fastapi import HTTPException, status


class BadRequest(HTTPException):
    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": message,
            },
        )
