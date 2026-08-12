from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared rate limiter, keyed by client IP. Kept in its own module (rather
# than defined in app.main) to avoid a circular import: app.main imports the
# endpoint routers, and endpoints like auth.py/users.py need to import
# `limiter` to decorate their routes with @limiter.limit(...).
limiter = Limiter(key_func=get_remote_address)
