import typing
import SimulationState
import abc


class SimulationBase(abc.ABC):
    @abc.abstractmethod
    def simulate(
        self,
        stopCallback: typing.Callable[[], None],
        simulationState: SimulationState,
        tickers: typing.List[str],
    ) -> None:
        ...
