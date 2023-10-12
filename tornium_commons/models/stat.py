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

from peewee import BooleanField, DateTimeField, ForeignKeyField, IntegerField

from .base_model import BaseModel
from .user import User


class Stat(BaseModel):
    tid = ForeignKeyField(User, index=True)
    battlescore = IntegerField()
    time_added = DateTimeField()
    added_tid = IntegerField()
    added_faction_tid = IntegerField(null=True)
    global_stat = BooleanField(default=True)
