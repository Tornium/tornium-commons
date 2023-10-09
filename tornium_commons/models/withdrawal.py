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
    DateTimeField,
    IntegerField,
    SmallIntegerField,
    UUIDField,
)

from .base_model import BaseModel


class Withdrawal(BaseModel):
    wid = IntegerField(primary_key=True)
    guid = UUIDField(index=True)
    faction_tid = IntegerField()
    amount = BigIntegerField()
    cash_request = BooleanField(default=True)
    requester = IntegerField()

    # Withdrawal status
    # 0: unfulfilled
    # 1: fulfilled
    # 2: cancelled
    # 3: cancelled by system
    status = SmallIntegerField()

    time_requested = DateTimeField()

    fulfiller = IntegerField()
    time_fulfilled = IntegerField()

    withdrawal_message = BigIntegerField()  # Discord message ID
