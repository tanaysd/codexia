from fastapi import APIRouter, Query

from ..schemas import BriefResult
from ..core.config import Settings
from ..services import compute_brief

EXAMPLES_DIR = "packages/backend/data/examples/claims"

router = APIRouter(prefix="/v1", tags=["rcm"])


@router.get("/brief", response_model=BriefResult)
def brief(user_id: str = Query(...), date: str = Query(...)) -> BriefResult:
    vec_dir = Settings().VECTOR_PATH
    res = compute_brief(user_id, date, vec_dir, EXAMPLES_DIR)
    return BriefResult.model_validate(res)
