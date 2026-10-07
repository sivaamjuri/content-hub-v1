from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from search import views as search_views

# ── Wagtail Headless API v2 ───────────────────────────────────────────────
api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)

urlpatterns = [
    # Django admin
    path("django-admin/", admin.site.urls),

    # Wagtail CMS admin panel
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    # ── JWT Authentication endpoints ──────────────────────────────────────
    # POST /api/token/          → { access, refresh }
    # POST /api/token/refresh/  → { access }
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ── Custom DRF endpoints (JWT protected) ──────────────────────────────
    # GET  /api/articles/          → public, no auth needed
    # GET  /api/categories/        → IsAuthenticated
    # POST /api/categories/        → IsAdminUser
    # GET/PUT/DELETE /api/categories/<id>/  → IsAuthenticated / IsAdminUser
    path("api/", include("content.urls")),

    # ── Wagtail API v2 (Headless CMS) ────────────────────────────────────
    # GET /api/v2/pages/?type=content.ArticlePage&fields=title,body,category
    # GET /api/v2/pages/<id>/
    # GET /api/v2/pages/find/?html_path=/articles/my-slug/
    # GET /api/v2/images/
    path("api/v2/", api_router.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include(wagtail_urls)),
]
