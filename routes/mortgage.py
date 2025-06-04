from fastapi import APIRouter, HTTPException, Depends
from models.mortgage_models import FormData
from models.user_models import User
from models.applicants_model import Applicant
from schemas.user_auth import get_current_user
from config.database import  mortgage_form, applicants
from typing import List
import uuid

router = APIRouter(prefix="/mortgage")

@router.post("/applicants")
async def add_applicant(applicant: Applicant, current_user: User=Depends(get_current_user)):
    applicant_dict = applicant.dict()
    applicant_dict["_id"] = str(uuid.uuid4())
    applicant_dict["UserId"] = current_user.userId

    result = await applicants.insert_one(applicant_dict)
    if result.inserted_id:
        return {"message": "Applicant added successfully", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to insert")
    

@router.get("/applicants")
async def get_applicants(current_user: User=Depends(get_current_user)):
    applicants_list = await applicants.find({"UserId": current_user.userId}).to_list(length=None)
    return applicants_list


@router.post("/save-form-data")
async def save_form_data(form_data: FormData, current_user:User=Depends(get_current_user)):
    try:
        await mortgage_form.update_one(
            {
                "formName": form_data.formName,
                "UserId": current_user.userId,
                "ApplicantId": form_data.applicantId
            },
            {"$set": {"data": form_data.data}},
            upsert=True,
        )

        return {"message": "Form data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-form-data/{form_name}/{applicantId}")
async def get_form_data(form_name: str, applicantId: str, current_user:User=Depends(get_current_user)):
    try:
        result = await mortgage_form.find_one({"formName": form_name, "UserId": current_user.userId, "ApplicantId": applicantId}, {"_id": 0})
        if result:
            return result["data"]
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))