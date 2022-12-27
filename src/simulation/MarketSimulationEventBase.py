import typing
import simulation.SimulationState as SimulationState
import abc


class MarketSimulationEvent(abc.ABC):
    @abc.abstractmethod
    def event(
        self,
        stopCallback: typing.Callable[[], None],
        simulationState: SimulationState,
        tickers: typing.List[str],
    ) -> None:
        ...
