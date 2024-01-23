from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(prefix="/full", tags=["full"] )
