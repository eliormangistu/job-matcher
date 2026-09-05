from fastapi import APIRouter
from app.core import SuccessMessage, StatusCode
from app.schemas import BaseResponse

router = APIRouter()

@router.get("/")
def health_check():
     return BaseResponse(
        True,
        StatusCode.OK,
        SuccessMessage.SUCCESS,
        None
    )
  