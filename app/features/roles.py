"""Small admin boundary enforced using current server-side permissions."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app import security

router = APIRouter()


@router.get("/api/admin")
def admin_api(request: Request):
    """Authorize each direct request before returning protected content."""
    user = security.require_admin(request)
    return {"message": "Admin access confirmed.", "username": user["username"]}


@router.get("/admin", include_in_schema=False)
def admin_page(request: Request):
    """Distinguish missing login from an authenticated member's denied access."""
    try:
        user = security.require_admin(request)
    except HTTPException as error:
        if error.status_code == 401:
            return RedirectResponse("/login", status_code=303)
        if error.status_code != 403:
            raise
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="admin_denied.html",
            context={},
            status_code=403,
        )
    return request.app.state.templates.TemplateResponse(
        request=request, name="admin.html", context={"user": user}
    )
