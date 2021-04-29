from __future__ import absolute_import

from functools import wraps

from django.http import HttpResponse

from JCoder_django_ratelimit import ALL, UNSAFE
from JCoder_django_ratelimit.core import is_ratelimited
from JCoder_django_ratelimit.exceptions import Ratelimited

__all__ = ['ratelimit']


def ratelimit(group=None, key=None, rate=None, method=ALL, block=False, callback=None):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                # raise Ratelimited()
                if callback:
                    return callback
                return HttpResponse(status=403, content='Too Many Times')
            return fn(request, *args, **kw)

        return _wrapped

    return decorator


def async_ratelimit(group=None, key=None, rate=None, method=ALL, block=False, callback=None):
    def decorator(fn):
        @wraps(fn)
        async def _wrapped(request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                if callback:
                    return callback
                # raise Ratelimited()
                return HttpResponse(status=403, content='Too Many Times')
            return await fn(request, *args, **kw)

        return _wrapped

    return decorator


ratelimit.ALL = ALL
ratelimit.UNSAFE = UNSAFE
