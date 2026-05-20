from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock

from injection_manager import InjectionManager


class FakeSession:
    def __init__(self):
        self.flush = AsyncMock()
        self.commit = AsyncMock()
        self.rollback = AsyncMock()


class RecordingInjectable:
    calls = []

    @classmethod
    async def process(cls, data, session):
        cls.calls.append((cls.__tablename__, data, session))


class FailingInjectable:
    @classmethod
    async def process(cls, data, session):
        raise ValueError("boom")


def make_base(sorted_tables, injectables):
    return SimpleNamespace(
        metadata=SimpleNamespace(sorted_tables=sorted_tables),
        injectable=injectables,
    )


def make_table(schema, name):
    return SimpleNamespace(schema=schema, name=name)


def make_recording_injectable(table_name):
    return type(
        f"{table_name.title()}Injectable",
        (RecordingInjectable,),
        {"__tablename__": table_name},
    )


class InjectionManagerTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        RecordingInjectable.calls = []

    async def test_inject_processes_matching_tables_in_sorted_order(self):
        data = object()
        session = FakeSession()
        first_table = make_table("warehouse", "players")
        skipped_table = make_table("warehouse", "missing")
        second_table = make_table("warehouse", "matches")
        base = make_base(
            [first_table, skipped_table, second_table],
            {
                "warehouse.players": make_recording_injectable("players"),
                "warehouse.matches": make_recording_injectable("matches"),
            },
        )

        await InjectionManager(base).inject(data, session)

        self.assertEqual(
            RecordingInjectable.calls,
            [("players", data, session), ("matches", data, session)],
        )
        self.assertEqual(session.flush.await_count, 2)
        session.commit.assert_awaited_once()
        session.rollback.assert_not_awaited()

    async def test_inject_rolls_back_and_reraises_when_process_fails(self):
        data = object()
        session = FakeSession()
        table = make_table("warehouse", "players")
        base = make_base(
            [table],
            {"warehouse.players": FailingInjectable},
        )

        with self.assertRaisesRegex(ValueError, "boom"):
            await InjectionManager(base).inject(data, session)

        session.flush.assert_not_awaited()
        session.commit.assert_not_awaited()
        session.rollback.assert_awaited_once()

    async def test_inject_commits_when_no_tables_are_injectable(self):
        session = FakeSession()
        table = make_table("warehouse", "players")
        base = make_base([table], {})

        await InjectionManager(base).inject(object(), session)

        session.flush.assert_not_awaited()
        session.commit.assert_awaited_once()
        session.rollback.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
