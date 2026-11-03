from fastapi import APIRouter, HTTPException

from api.schemas import DashboardLiveSnapshot
from api.services.inference_service import generate_live_dashboard_snapshot

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("/live", response_model=DashboardLiveSnapshot)
def get_live_dashboard() -> DashboardLiveSnapshot:
    """Mengembalikan snapshot prakiraan dari arsip ERA5 minimal 7 hari lalu.

    Mencakup:
    - 5 petak kanonik (MAIN, UP, DOWN, LEFT, RIGHT)
    - Prakiraan probabilistik 1 jam berikutnya (30 kemungkinan)
    - 3 pola serupa terdekat dari data latih
    """
    try:
        return generate_live_dashboard_snapshot()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal menghasilkan inferensi dashboard live: {exc}",
        ) from exc

