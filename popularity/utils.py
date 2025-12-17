from django.core.validators import validate_ipv46_address
from django.contrib.contenttypes.models import ContentType

try:
    from popularity.tasks import viewtrack as viewtrack_task
except ImportError:
    viewtrack_task = None  # Celery wasn't found
from django.core.exceptions import ValidationError


def _unwrap(obj):
    # lazy_object_proxy.Proxy
    getter = getattr(obj, "_get_current_object", None)
    if callable(getter):
        try:
            return getter()
        except Exception:
            return None
    # Django SimpleLazyObject/LazyObject
    try:
        if hasattr(obj, "_wrapped"):
            w = obj._wrapped
            if w is not None:
                return w
    except Exception:
        return None
    return obj


def viewtrack(request, instance):
    if viewtrack_task is None:
        raise Exception("You must install celery to use this templatetag")

    request = _unwrap(request)
    if request is None or not hasattr(request, "META"):
        return  # no request context (celery/template render/etc)

    ct = ContentType.objects.get_for_model(instance)

    meta = _unwrap(request.META) or {}
    ip = meta.get("HTTP_X_FORWARDED_FOR") or meta.get("REMOTE_ADDR")

    if not ip:
        return

    # take FIRST public-facing IP from XFF
    ip = ip.split(",")[0].strip()

    try:
        validate_ipv46_address(ip)
    except (ValidationError, ValueError, TypeError):
        return

    viewtrack_task.apply_async(args=[ct.pk, instance.pk, ip])
