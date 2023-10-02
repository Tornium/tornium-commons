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

import pathlib
import secrets
import typing

from pydantic import (
    AnyUrl,
    BaseModel,
    CockroachDsn,
    Field,
    MySQLDsn,
    PostgresDsn,
    RedisDsn,
)

from .altjson import dump, load


class Settings(BaseModel):
    bot_token: str = Field()
    bot_application_id: int = Field()
    bot_application_public: str = Field()

    flask_secret: str = Field()
    flask_domain: str = Field()
    flask_admin_passphrase: str = Field()

    db_type: typing.Literal["pg", "mysql", "oracle", "cockroach", "sqlite"] = Field(default="pg")
    db_dsn: typing.Union[PostgresDsn, CockroachDsn, MySQLDsn, AnyUrl] = Field()

    redis_dsn: RedisDsn = Field()

    # Internal Data
    _file: typing.Optional[pathlib.Path] = None
    _loaded = False

    @classmethod
    def from_json(cls, file: typing.Union[pathlib.Path, str] = "settings.json", disable_cache=False):
        if not disable_cache:
            from .redisconnection import rds

        file: pathlib.Path
        if type(file) != pathlib.Path:
            file = pathlib.Path(file)
        elif not file.exists():
            raise FileNotFoundError

        loaded_data: dict = load(file)

        for data_key, data_value in loaded_data.items():
            if type(data_value) == bool:
                data_value = int(data_value)

            if not disable_cache:
                rds().set(f"tornium:settings:{data_key}", data_value)

        self = cls(**loaded_data)
        self._file = file
        self._loaded = True

        return self

    def __getitem__(self, item, disable_cache=False):
        if not disable_cache:
            from .redisconnection import rds

        if self._loaded:
            return getattr(self, item)

        if not disable_cache:
            cached_value = rds().get(f"tornium:settings:{item}")
        else:
            cached_value = None

        if cached_value is not None:
            return cached_value

        self.load()

        if self._loaded:
            return getattr(self, item)

        raise ValueError("Settings unable to be loaded")

    def __setitem__(self, key, value, disable_cache=False):
        if not disable_cache:
            from .redisconnection import rds

        if self._file is None:
            raise ValueError("File is not set")

        setattr(self, key, value)

        if type(value) == bool:
            value = int(value)

        if not disable_cache:
            rds().set(key, value)

        self.save()

    def load(self, disable_cache=False):
        if not disable_cache:
            from .redisconnection import rds

        if not self._file.exists():
            raise FileNotFoundError

        loaded_data: dict = load(self._file)

        for data_key, data_value in loaded_data.items():
            if type(data_value) == bool:
                data_value = int(data_value)

            if not disable_cache:
                rds().set(f"tornium:settings:{data_key}", data_value)

            setattr(self, data_key, data_value)

        self._loaded = True
        return self

    def save(self):
        if not self._file.exists():
            raise FileNotFoundError

        with open(self._file, "w") as f:
            f.write(self.model_dump_json(indent=4))

        return self

    def regen_secret(self, nbytes: int = 32):
        self.__setitem__("flask_secret", secrets.token_hex(nbytes))
        return self.__getitem__("flask_secret")

    def __iter__(self):
        key: str
        for key, value in super().__iter__():
            if key.startswith("_"):
                continue

            yield key, value
