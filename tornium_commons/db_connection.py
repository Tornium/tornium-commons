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

from functools import wraps

from playhouse.postgres_ext import PostgresqlExtDatabase

from .config import Settings

_db = None


def db():
    global _db

    if _db is not None:
        return _db

    _s = Settings.from_cache()
    _db = PostgresqlExtDatabase("Tornium", host=_s.db_dsn)

    return _db


def requires_db_connection(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        _inner_db = db()
        _inner_db.connect()

        _inner = f(database=_inner_db, *args, **kwargs)

        _inner_db.close()
        return _inner

    return wrapper
