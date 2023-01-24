from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.models import Account
from src.auth.service import get_jwt_user_active

from src.database import get_db
from src.emails.forwards.schemas import ForwardResponse, ForwardCreate, ForwardUpdate, ForwardsResponse
from src.emails.forwards import service
from src.emails.proxy import service as proxy_service

router = APIRouter()


@router.post("", response_model=ForwardResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_jwt_user_active)])
def create(forward_in: ForwardCreate, db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    forward = service.get_by_source_n_destination(
        db, forward_in=forward_in, account_id=account.id)
    if forward:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Forward already exist"
        )
    return service.create(db, forward_in, account.id)


@router.get("", response_model=List[ForwardsResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def get_all(db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    return service.get_forwards(db, account.id)


@router.get("/active", response_model=List[ForwardsResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def get_forwards_active(db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    return service.get_forwards_by_status(db, account.id, True)


@router.get("/deactivate", response_model=List[ForwardsResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def get_forwards_deactivate(db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    return service.get_forwards_by_status(db, account.id, False)


@router.get("/{forward_id}", response_model=ForwardResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def get(forward_id: str, db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    alias = service.get_by_id(db, forward_id=forward_id, account=account)
    if not alias:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Forward {forward_id} not found"
        )
    return alias


@router.put("/{forward_id}", response_model=ForwardResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def update(forward_id: str, forward_in: ForwardUpdate, db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    forward = service.get_by_id(db, forward_id=forward_id, account=account)
    if not forward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Forward {forward_id} not found"
        )
    return service.update(db, alias=forward, alias_in=forward_in)


@router.post("/{forward_id}/deactivate", response_model=ForwardResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def deactivate(forward_id: str, db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    forward = service.get_by_id(db, forward_id=forward_id, account=account)
    if not forward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Forward {forward_id} not found"
        )
    return service.deactivate(db, forward=forward)


@router.post("/{forward_id}/activate", response_model=ForwardResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def activate(forward_id: str, db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    forward = service.get_by_id(db, forward_id=forward_id, account=account)
    if not forward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Forward {forward_id} not found"
        )
    return service.activate(db, forward=forward)


@router.delete("/{forward_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_jwt_user_active)])
def delete(forward_id: str, db: Session = Depends(get_db), account: Account = Depends(get_jwt_user_active)):
    forward = service.get_by_id(db, forward_id=forward_id, account=account)
    if not forward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Forward {forward_id} not found"
        )
    return service.delete(db, forward=forward)
