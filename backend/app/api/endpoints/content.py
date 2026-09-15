from fastapi import APIRouter, Header, HTTPException

from app.cache.content import get_content, invalidate_content
from app.core.config import CONTENTFUL_WEBHOOK_SECRET
from app.core.logger import ServiceLogger
from app.schemas import BaseResponse
from app.schemas.content import ContentResponse
from app.core import SuccessMessage, StatusCode, ErrorMessage

router = APIRouter()

logger = ServiceLogger("content")

router = APIRouter(
    prefix="/content",
    tags=["content"],
)


@router.get("", response_model=BaseResponse[ContentResponse])
def get_content_endpoint() -> BaseResponse[ContentResponse]:
    return BaseResponse(
        success=True,
        status_code=StatusCode.OK,
        message=SuccessMessage.CONTENT,
        data=get_content(),
    )


@router.post("/webhook")
def content_webhook(
    x_contentful_webhook_secret: str | None = Header(default=None),
) -> BaseResponse[dict]:
    if (
        not CONTENTFUL_WEBHOOK_SECRET
        or x_contentful_webhook_secret != CONTENTFUL_WEBHOOK_SECRET
    ):
        logger.warning(
            "Invalid Contentful webhook secret",
            action="webhook_rejected",
        )
        raise HTTPException(
            status_code=StatusCode.UNAUTHORIZED,
            detail=ErrorMessage.AUTHENTICATION_REQUIRED,
        )

    invalidate_content()

    logger.info(
        "Content cache invalidated by Contentful webhook",
        action="webhook_received",
    )

    return BaseResponse(
        success=True,
        status_code=StatusCode.OK,
        message=SuccessMessage.CONTENT,
        data={},
    )
