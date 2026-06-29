# from fastapi import APIRouter

# router = APIRouter()
# info = APIRouter()

# @router.get("/health")
# def health_check():
#     return {
#         "status": "healthy",
#         "service": "Revio API",
#         "version": "0.1.0",
#     }

# @info.get("/information")
# def inform() : {
#     "name": "Revio",
#     "description": "AI-powered learning platform",
#     "author": "Vedansh Garg"
# }
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Revio API",
        "version": "0.1.0",
    }


@router.get("/info")
def info():
    return {
        "name": "Revio",
        "description": "AI-powered learning platform",
        "author": "Vedansh Garg",
    }