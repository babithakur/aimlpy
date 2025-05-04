"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/11/2024
"""
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Health"])


@router.get("/hc", status_code=200)
async def health_check():
    """
    Simple health check endpoint
    Returns current server status and timestamp
    """
    return JSONResponse(content={
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@router.get("/", status_code=200)
async def health_check():
    """
    Simple health check endpoint
    Returns current server status and timestamp
    """
    return JSONResponse(content={
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })
