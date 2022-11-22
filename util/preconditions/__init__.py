from .base import Precondition
from .admin_only import AdminOnly
from .owner_only import OwnerOnly

preconditions: dict[str, Precondition] = {
	"admin_only": AdminOnly(),
	"owner_only": OwnerOnly()
}