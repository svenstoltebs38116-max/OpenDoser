"""Role registry for OpenDoser."""

from .roles import Role


class RoleRegistry:
    """Stores the mapping between roles and entity IDs."""

    def __init__(self) -> None:
        self._roles: dict[Role, str] = {}

    def set(self, role: Role, entity_id: str) -> None:
        """Assign an entity to a role."""
        self._roles[role] = entity_id

    def get(self, role: Role) -> str | None:
        """Return the entity assigned to a role."""
        return self._roles.get(role)

    def remove(self, role: Role) -> None:
        """Remove a role assignment."""
        self._roles.pop(role, None)

    def exists(self, role: Role) -> bool:
        """Check whether a role has been assigned."""
        return role in self._roles

    def all(self) -> dict[Role, str]:
        """Return all assignments."""
        return dict(self._roles)