# Copyright (C) 2021-2023 tiksan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from peewee import (
    BigIntegerField,
    BooleanField,
    CharField,
    DateTimeField,
    DeferredForeignKey,
    IntegerField,
)
from playhouse.postgres_ext import ArrayField, JSONField

from .base_model import BaseModel
from .faction_position import FactionPosition


class Faction(BaseModel):
    # Basic data
    tid = IntegerField(primary_key=True)
    name = CharField(max_length=25, null=True)
    tag = CharField(max_length=4, null=True)
    respect = IntegerField(null=True)
    capacity = IntegerField(null=True)
    leader = DeferredForeignKey("User", null=True)
    coleader = DeferredForeignKey("User", null=True)

    # API keys
    # TODO: Switch to key db (#188)
    aa_keys = ArrayField(CharField, field_kwargs={"max_length": 15}, default=[])

    # Guild data
    guild = DeferredForeignKey("Server", null=True)  # noqa: F712

    # Configuration data
    stats_db_enabled = BooleanField(default=True)  # noqa: F712
    stats_db_global = BooleanField(default=True)  # noqa: F712

    # OD data
    od_channel = BigIntegerField(null=True)
    od_data = JSONField(null=True)

    # Internal data
    last_members = DateTimeField(null=True)
    last_attacks = DateTimeField(null=True)

    def get_bankers(self):
        from .user import User

        banker_positions = FactionPosition.select(FactionPosition.pid).where(
            (FactionPosition.faction_tid == self.tid)
            & (
                (FactionPosition.give_money == True)  # noqa: E712
                | (FactionPosition.give_points == True)  # noqa: E712
                | (FactionPosition.adjust_balances == True)  # noqa: E712
            )
        )
        bankers = set()

        _position: FactionPosition
        for _position in banker_positions:
            bankers.update([user.tid for user in User.select(User.tid).where(User.faction_position == _position.pid)])

        if self.leader != 0:
            bankers.add(self.leader)
        if self.coleader != 0:
            bankers.add(self.coleader)

        return bankers
