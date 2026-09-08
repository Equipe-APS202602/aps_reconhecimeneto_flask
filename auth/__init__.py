# auth/__init__.py

from .facial import reconhecer_rosto
from .permissions import (
    PERMISSOES,
    possui_permissao,
    login_required,
    permission_required
)