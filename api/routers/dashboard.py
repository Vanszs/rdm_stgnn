from fastapi import APIRouter, HTTPException

from api.schemas import DashboardLiveSnapshot
from api.services.inference_service import generate_live_dashboard_snapshot

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("/live", response_model=DashboardLiveSnapshot)
def get_live_dashboard() -> DashboardLiveSnapshot:
    """Mengembalikan snapshot cuaca real-time dan inferensi RDM-STGNN (Skenario 3).

    Mencakup:
    - Observasi 5 node kanonik (MAIN, UP, DOWN, LEFT, RIGHT)
    - Nowcasting probabilistik T+1 jam (50 sampel stokastik difusi, mean, p10-p90)
    - Top-3 analog historis riil dari indeks FAISS IndexFlatL2
    """
    try:
        return generate_live_dashboard_snapshot()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal menghasilkan inferensi dashboard live: {exc}",
        ) from exc

