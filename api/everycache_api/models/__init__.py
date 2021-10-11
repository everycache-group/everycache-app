from everycache_api.models.cache import Cache
from everycache_api.models.cache_comment import CacheComment
from everycache_api.models.cache_visit import CacheVisit
from everycache_api.models.token import Token
from everycache_api.models.user import User

__all__ = ["Cache", "CacheComment", "CacheVisit", "Token", "User"]

# assign _hashids_model_id for each db model except Token
for i, model in enumerate([Cache, CacheComment, CacheVisit, User]):
    model._hashids_model_id = i
