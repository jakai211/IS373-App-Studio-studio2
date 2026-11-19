"""Browser and JSON account flows using the prepared session protections."""

from urllib.parse import parse_qs

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app import security
from app.schemas import LoginInput, PublicUser, SignupInput

router = APIRouter()


def _page(request, name, context=None, status_code=200, headers=None):
    """Render a form with CSRF state without ever returning a password."""
    cookie_response = Response()
    token = security.csrf_token(request, cookie_response)
    response = request.app.state.templates.TemplateResponse(
        request=request,
        name=name,
        context={**(context or {}), "csrf_token": token},
        status_code=status_code,
        headers=headers,
    )
    for key, value in cookie_response.raw_headers:
        if key.lower() == b"set-cookie":
            response.raw_headers.append((key, value))
    return response


async def _form(request):
    """Bound form input and reject duplicate or non-text fields."""
    if request.headers.get("content-type", "").split(";")[0] != (
        "application/x-www-form-urlencoded"
    ):
        raise HTTPException(415, "Use the form on this page.")
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > 8192:
            raise HTTPException(413, "The submitted form is too large.")
    try:
        fields = parse_qs(
            body.decode("utf-8"),
            keep_blank_values=True,
            max_num_fields=4,
            encoding="utf-8",
            errors="strict",
        )
    except (UnicodeError, ValueError) as error:
        raise HTTPException(422, "Please check the form and try again.") from error
    if any(len(values) != 1 for values in fields.values()):
        raise HTTPException(422, "Please submit each field once.")
    values = {key: items[0] for key, items in fields.items()}
    security.require_csrf(request, values.pop("csrf_token", None))
    return values


@router.get("/api/csrf")
def api_csrf(request: Request, response: Response):
    """Supply a same-origin client with the session's synchronizer token."""
    return {"csrf_token": security.csrf_token(request, response)}


@router.post("/api/signup", response_model=PublicUser, status_code=201)
def api_signup(request: Request, credentials: SignupInput):
    """Create only a member using normalized, validated credentials."""
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))
    security.limit_signup(request)
    return security.signup(
        request.app.state.settings, credentials.username, credentials.password
    )


@router.post("/api/login", response_model=PublicUser)
def api_login(request: Request, response: Response, credentials: LoginInput):
    """Issue an HttpOnly session cookie; never return its token in JSON."""
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))
    return security.login(request, response, credentials.username, credentials.password)


@router.get("/api/me", response_model=PublicUser)
def api_me(request: Request):
    """Require a current, non-revoked session for private identity."""
    return security.require_user(request)


@router.post("/api/logout")
def api_logout(request: Request, response: Response):
    """Revoke server state as well as clearing the cookie."""
    security.require_user(request)
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))
    security.logout(request, response)
    return {"message": "Logged out."}


@router.get("/signup", include_in_schema=False)
def signup_page(request: Request):
    """Show the account form, or the dashboard for an existing member."""
    if security.authenticate(request):
        return RedirectResponse("/dashboard", status_code=303)
    return _page(request, "account.html", {"signup": True})


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    """Offer login without accepting external redirect destinations."""
    if security.authenticate(request):
        return RedirectResponse("/dashboard", status_code=303)
    return _page(request, "account.html", {"signup": False})


async def _submit(request, signup):
    """Use the same guarded services as JSON routes, with recoverable errors."""
    username = ""
    try:
        values = await _form(request)
        model = SignupInput if signup else LoginInput
        credentials = model.model_validate(values)
        username = credentials.username
        response = RedirectResponse(
            "/login" if signup else "/dashboard", status_code=303
        )
        if signup:
            security.limit_signup(request)
            security.signup(request.app.state.settings, username, credentials.password)
        else:
            security.login(request, response, username, credentials.password)
        return response
    except ValidationError:
        error_text = (
            "Use a username of 3–32 letters, numbers or underscores and a "
            "password of 15–128 characters."
            if signup
            else "Enter your username and password within the shown limits."
        )
        status_code, headers = 422, None
    except HTTPException as error:
        error_text, status_code, headers = (
            error.detail,
            error.status_code,
            error.headers,
        )
    return _page(
        request,
        "account.html",
        {"signup": signup, "username": username, "error": error_text},
        status_code,
        headers,
    )


@router.post("/signup", include_in_schema=False)
async def signup_form(request: Request):
    """Validate a public form without accepting a caller-selected role."""
    return await _submit(request, True)


@router.post("/login", include_in_schema=False)
async def login_form(request: Request):
    """Keep only a validated username when credentials are rejected."""
    return await _submit(request, False)


@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request):
    """Redirect anonymous visitors before rendering any private content."""
    user = security.authenticate(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return _page(request, "dashboard.html", {"user": user})


@router.post("/logout", include_in_schema=False)
async def logout_form(request: Request):
    """Require the live form token and revoke the session before redirecting."""
    await _form(request)
    response = RedirectResponse("/login", status_code=303)
    security.logout(request, response)
    return response
