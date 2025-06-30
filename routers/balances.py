from fastapi import APIRouter

router = APIRouter()

@router.get("/groups/{group_id}/balances")
def get_group_balances(group_id: int):
    # Here you’d calculate who owes whom
    return {"message": "Balance calculation not implemented yet"}
