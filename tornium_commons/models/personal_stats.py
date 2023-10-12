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

from peewee import BigIntegerField, DateTimeField, IntegerField
from playhouse.postgres_ext import JSONField

from .base_model import BaseModel


class PersonalStats(BaseModel):
    #### pstat_id ####
    # tid = bin(tid << 8)
    # timestamp = bin(timestamp)
    # pstat_id = int(tid, 2) + int(timestamp, 2)
    ##################

    pstat_id = BigIntegerField(primary_key=True)
    tid = IntegerField()
    timestamp = DateTimeField()

    # Uses jsonb as size of values is not known beyond "int"
    ps_data = JSONField(index=False)
