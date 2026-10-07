"""Validator for ai-physician"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
class ValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await call_next(request)
