""" Routes associating each http request with a specific path for this endpoint."""

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

# Local imports
from .crud import (create_popular, delete_popular, read_popular,
                   read_popular_index, update_popular)
from .models import (ErrorResponseModel, PopularModel, ResponseModel,
                     UpdatePopularModel)

# Instanciate a router for this endpoint
router = APIRouter()


@router.get(
    "/",
    response_description="Index of popular articles retrieved",
    # response_model=PopularModel,
)
async def list_populars():
    populars = await read_popular_index()
    if populars:
        return ResponseModel(
            populars,
            "Index of group of popular articles retrieved successfully",
        )
    return ResponseModel(
        populars,
        "Empty list returned",
    )


@router.get(
    "/{id}",
    response_description="Popular articles retrieved",
    # response_model=PopularModel,
)
async def show_popular(id):
    popular = await read_popular(id)
    if popular:
        return ResponseModel(
            popular,
            "Group of popular articles retrieved successfully",
        )
    return ErrorResponseModel(
        "An error occurred.",
        404,
        "Group of popular articles doesn't exist.",
    )


# FIXME: POST request is broken but it's not required in this endpoint.
@router.post(
    "/",
    response_description="Popular articles added",
    #  response_model=PopularModel,
)
async def add_popular(popular: PopularModel = Body(...)):
    popular = jsonable_encoder(popular)
    created_popular = await create_popular(popular)
    return ResponseModel(
        created_popular,
        "Group of popular articles added successfully.",
    )


@router.put("/{id}", response_description="Popular articles updated")
async def modify_popular(id: str, req: UpdatePopularModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_popular = await update_popular(id, req)
    if updated_popular:
        return ResponseModel(
            "Group of popular articles with ID: {0} update is successful".format(id),
            "Group of popular articles updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the group of popular articles.",
    )


@router.delete("/{id}", response_description="Popular articles deleted")
async def remove_popular(id: str):
    deleted_popular = await delete_popular(id)
    if deleted_popular:
        return ResponseModel(
            "Group of popular articles with ID: {0} removed".format(id),
            "Group of popular articles deleted successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "Group of popular articles with id {0} doesn't exist".format(id),
    )
