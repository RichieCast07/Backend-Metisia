from fastapi import APIRouter, Depends, Query
from app.presentation.dependencies import get_current_user, get_sale_repository, get_expense_repository
from app.presentation.schemas.report import DailySalesReportResponse, SalesByPaymentMethodResponse, TopProductsResponse
from app.application.use_cases.report_use_cases import DailySalesReport, SalesByPaymentMethod, TopProducts
from app.domain.entities.user import User
from datetime import date

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/daily", response_model=DailySalesReportResponse)
async def daily_report(
    day: date = Query(default_factory=date.today),
    sale_repo=Depends(get_sale_repository),
    expense_repo=Depends(get_expense_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = DailySalesReport(sale_repo, expense_repo)
    return await use_case(current_user.id, day)


@router.get("/payment-methods", response_model=SalesByPaymentMethodResponse)
async def payment_methods_report(
    start: date = Query(...),
    end: date = Query(...),
    sale_repo=Depends(get_sale_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = SalesByPaymentMethod(sale_repo)
    data = await use_case(current_user.id, start, end)
    return {"data": data}


@router.get("/top-products", response_model=TopProductsResponse)
async def top_products_report(
    start: date = Query(...),
    end: date = Query(...),
    limit: int = Query(default=10, ge=1, le=50),
    sale_repo=Depends(get_sale_repository),
    current_user: User = Depends(get_current_user),
):
    use_case = TopProducts(sale_repo)
    products = await use_case(current_user.id, start, end, limit)
    return {"products": products}
