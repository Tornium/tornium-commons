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
    ForeignKeyField,
    IntegerField,
)
from playhouse.postgres_ext import ArrayField, JSONField

from .base_model import BaseModel
from .server import Server


class Faction(BaseModel):
    # Basic data
    tid = IntegerField(primary_key=True)
    name = CharField(max_length=25)
    tag = CharField(max_length=4)
    respect = IntegerField()
    capacity = IntegerField()
    leader = DeferredForeignKey("User")
    coleader = DeferredForeignKey("User")

    # API keys
    # TODO: Switch to key db (#188)
    aa_keys = ArrayField(CharField(max_length=15))

    # Guild data
    guild = ForeignKeyField(Server)

    # Configuration data
    stats_db_enabled = BooleanField(default=True)
    stats_db_global = BooleanField(default=True)

    # OD data
    od_channel = BigIntegerField()
    od_data = JSONField()

    # Internal data
    last_members = DateTimeField()
    last_attacks = DateTimeField()
