from injection_manager.managers import InjectionManager, EventInjectionManager
from injection_manager.typeclass import Injectable

from starcraft_data_orm.warehouse.config import SessionLocal
from starcraft_data_orm.warehouse.base import WarehouseBase
from starcraft_data_orm.warehouse import initialize_warehouse
from sc2reader import load_replay
from asyncio import run

async def main():
    async with SessionLocal() as session:
        initialize_warehouse()

        replay = load_replay("examples/example_5.SC2Replay")
        _prepare(replay)

        await InjectionManager(WarehouseBase).inject(replay, session)

def _prepare(replay):
    """Prepare replay by organizing events."""
    from collections import defaultdict
    replay.events_dictionary = defaultdict(list)
    for event in replay.events:
        replay.events_dictionary[event.name].append(event)
    del replay.events


if __name__ == "__main__":
    run(main())
