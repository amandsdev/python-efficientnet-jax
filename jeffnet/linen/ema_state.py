import flax
import flax.serialization as serialization
import flax.struct as struct
import jax

from typing import Any


@struct.dataclass
class EmaState:
    decay: float = struct.field(pytree_node=False, default=0.)
    variables: flax.core.FrozenDict[str, Any] = None

    @staticmethod
    def create(decay, variables):
        """Initialize ema state"""
        if decay == 0.:
            # default state == disabled
            return EmaState()
        ema_variables = jax.tree_map(lambda x: x, variables)
        return EmaState(decay, ema_variables)

    def update(self, new_variables):
        if self.decay == 0.:
            return self.replace(variables=None)
        new_ema_variables = jax.tree_multimap(
            lambda ema, p: ema * self.decay + (1. - self.decay) * p, self.variables, new_variables)
        return self.replace(variables=new_ema_variables)
