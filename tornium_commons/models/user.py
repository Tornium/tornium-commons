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
    FloatField,
    ForeignKeyField,
    IntegerField,
    SmallIntegerField,
    TextField,
)
from playhouse.postgres_ext import ArrayField

from .base_model import BaseModel
from .faction import Faction
from .faction_position import FactionPosition


class User(BaseModel):
    # Basic data
    tid = IntegerField(primary_key=True)
    name = CharField(max_length=15)
    level = SmallIntegerField()
    key = CharField(max_length=16, index=True)
    discord_id = BigIntegerField(index=True)

    # Battle stats
    battlescore = FloatField()
    strength = BigIntegerField()
    defense = BigIntegerField()
    speed = BigIntegerField()
    dexterity = BigIntegerField()

    # Faction data
    faction_id = ForeignKeyField(Faction, index=True)
    faction_aa = BooleanField()
    faction_position = ForeignKeyField(FactionPosition)

    # User status
    status = TextField()
    last_action = DateTimeField()

    # Internal data
    last_refresh = DateTimeField()
    last_attacks = DateTimeField()
    battlescore_update = DateTimeField()

    # Security data
    security = SmallIntegerField(default=0)
    otp_secret = TextField()
    otp_backups = ArrayField(TextField, index=False)
