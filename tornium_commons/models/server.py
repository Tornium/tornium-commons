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
    ForeignKeyField,
    IntegerField,
    TextField,
)
from playhouse.postgres_ext import ArrayField, JSONField

from .base_model import BaseModel
from .faction import Faction
from .user import User


class Server(BaseModel):
    # Basic data
    sid = BigIntegerField(primary_key=True)
    name = TextField()
    admins = ArrayField(ForeignKeyField(User))
    icon = TextField()  # hash of Discord server icon

    # Faction data
    factions = ArrayField(ForeignKeyField(Faction))

    # Verification configuration
    verify_enabled = BooleanField(default=False)
    verify_template = TextField(default="{{ name }} [{{ tid }}]")
    verified_roles = ArrayField(BigIntegerField)
    exclusion_roles = ArrayField(BigIntegerField)
    faction_verify = JSONField()
    verify_log_channel = BigIntegerField(default=0)

    # Retal configuration
    retal_config = JSONField()

    # Banking configuration
    banking_config = JSONField()

    # Armory tracking configuration
    # per faction: {
    #     str(faction_id): {
    #         "enabled": bool(false default)
    #         "channel": int(channel_id)
    #         "roles": [list of int(roles)]
    #         "items": {
    #             str(item_id): int(minimum_quantity)
    #         }
    #     }
    # }
    armory_enabled = BooleanField(default=False)
    armory_config = JSONField()

    # Assist configuration
    assist_channel = BigIntegerField(default=0)
    assist_factions = ArrayField(IntegerField)  # List of factions that can send assists to the server
    assist_smoker_roles = ArrayField(BigIntegerField)
    assist_tear_roles = ArrayField(BigIntegerField)
    assist_l0_roles = ArrayField(BigIntegerField)  # 500m+
    assist_l1_roles = ArrayField(BigIntegerField)  # 1b+
    assist_l2_roles = ArrayField(BigIntegerField)  # 2b+
    assist_l3_roles = ArrayField(BigIntegerField)  # 5b+

    # OC configuration
    oc_config = JSONField()

    # Stocks configuration
    # TODO: rework this schema before this feature is released
    stocks_channel = BigIntegerField(default=0)
    stocks_config = JSONField
