"""Clase Cliente con encapsulación y validaciones estrictas."""
import re

from entidades import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError

_email = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(Entidad):
    def __init__(self, nombre=None, documento=None, email=None, telefono=None):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    @staticmethod
    def _requerido(valor, campo):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError(f"Falta el parámetro obligatorio: {campo}")
        return str(valor).strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._requerido(valor, "nombre")
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'")
        self._nombre = valor.title()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = self._requerido(valor, "documento")
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(f"Documento inválido: '{valor}'")
        self._documento = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        valor = self._requerido(valor, "email")
        if not _email.match(valor):
            raise ClienteInvalidoError(f"Email inválido: '{valor}'")
        self._email = valor.lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._requerido(valor, "telefono")
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'")
        self._telefono = valor

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} (Doc: {self.documento}, {self.email})"
