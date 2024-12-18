from __future__ import annotations

from abc import ABC, abstractmethod, ABCMeta
from typing import BinaryIO
from pathlib import Path

import struct as st


SerializableType = int | str


class FieldNotFound(Exception):
    pass


class FieldValidationError(Exception):
    pass


class Struct:
    def __init__(self, *fields: Field):
        self.fields = fields

    def read(self, in_stream: BinaryIO) -> None:
        for field in self.fields:
            field.value = field.type.read(in_stream)

    def write(self, out_stream: BinaryIO) -> int:
        for field in self.fields:
            field.type.write(out_stream, field.value)

    def set(self, name: str, value: SerializableType) -> None:
        for field in self.fields:
            if field.name == name:
                if field.type.verify(value):
                    field.value = value
                    return
                else:
                    raise FieldValidationError(
                        f"Field `{name}` have type {type(field.type)}. Value object have type {type(value)}."
                    )
        raise FieldNotFound(name)

    def get(self, name: str) -> SerializableType:
        for field in self.fields:
            if field.name == name:
                return field.value
        raise FieldNotFound(name)


class Field:
    def __init__(
        self, name: str, _type: Type | type[Type], default: SerializableType = None
    ):
        self.name: str = name
        self.type: Type = _type() if type(_type) == ABCMeta else _type
        self.value: SerializableType = default


class Type(ABC):
    @staticmethod
    @abstractmethod
    def verify(obj: SerializableType) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def read(stream: BinaryIO) -> SerializableType:
        pass

    @staticmethod
    @abstractmethod
    def write(stream: BinaryIO, obj: SerializableType) -> int:
        pass


class NumType(Type):
    @staticmethod
    @abstractmethod
    def read(stream: BinaryIO, endian: str = "<") -> int:
        pass

    @staticmethod
    @abstractmethod
    def write(stream: BinaryIO, number: int, endian: str = "<") -> int:
        pass


class StrType(Type):
    @staticmethod
    @abstractmethod
    def read(stream: BinaryIO, size: int, encoding: str = "utf-8") -> str:
        pass

    @staticmethod
    @abstractmethod
    def write(stream: BinaryIO, string: str, encoding: str = "utf-8") -> int:
        pass


class Int8(NumType):
    @staticmethod
    def verify(obj: SerializableType) -> bool:
        # TODO
        # Implement number range checking
        return type(obj) == int

    @staticmethod
    def read(stream: BinaryIO, endian: str = "<") -> int:
        fmt = f"{endian}b"
        return st.unpack(fmt, stream.read(st.calcsize(fmt)))[0]

    @staticmethod
    def write(stream: BinaryIO, number: int, endian: str = "<") -> int:
        return stream.write(st.pack(f"{endian}b", number))


class Int16(NumType):
    @staticmethod
    def verify(obj: SerializableType) -> bool:
        # TODO
        # Implement number range checking
        return type(obj) == int

    @staticmethod
    def read(stream: BinaryIO, endian: str = "<") -> int:
        fmt = f"{endian}h"
        return st.unpack(fmt, stream.read(st.calcsize(fmt)))[0]

    @staticmethod
    def write(stream: BinaryIO, number: int, endian: str = "<") -> int:
        return stream.write(st.pack(f"{endian}h", number))


class Int32(NumType):
    @staticmethod
    def verify(obj: SerializableType) -> bool:
        # TODO
        # Implement number range checking
        return type(obj) == int

    @staticmethod
    def read(stream: BinaryIO, endian: str = "<") -> int:
        fmt = f"{endian}i"
        return st.unpack(fmt, stream.read(st.calcsize(fmt)))[0]

    @staticmethod
    def write(stream: BinaryIO, number: int, endian: str = "<") -> int:
        return stream.write(st.pack(f"{endian}i", number))


class String(StrType):
    def __init__(self, length: int):
        self.length = length

    @staticmethod
    def verify(obj: SerializableType) -> bool:
        return type(obj) == str

    @staticmethod
    def read(stream: BinaryIO, size: int, encoding: str = "utf-8") -> str:
        return stream.read(size).decode(encoding)

    @staticmethod
    def write(stream: BinaryIO, string: str, encoding: str = "utf-8") -> int:
        return stream.write(string.encode(encoding))


def read_stream(path: Path | str) -> BinaryIO:
    return open(path, "rb")


def write_stream(path: Path | str) -> BinaryIO:
    return open(path, "wb")
