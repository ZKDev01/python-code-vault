from RSA import RSA_from_Scratch
import random
import math
import hashlib
import base64
import json
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class RSAKey:
  """Estructura para almacenar claves RSA"""
  n: int
  e: Optional[int] = None  # Para pública
  d: Optional[int] = None  # Para privada
  p: Optional[int] = None  # Solo privada (opcional)
  q: Optional[int] = None  # Solo privada (opcional)

  def public_key(self) -> Tuple[int, int]:
    return (self.e, self.n)

  def private_key(self) -> Tuple[int, int]:
    return (self.d, self.n)


class OAEP:
  """Implementación de OAEP con MGF1 y SHA-256"""

  def __init__(self, hash_func=hashlib.sha256):
    self.hash = hash_func
    self.hLen = hash_func().digest_size  # 32 bytes para SHA-256

  def mgf1(self, seed: bytes, length: int) -> bytes:
    """MGF1 (Mask Generation Function) con SHA-256"""
    hLen = self.hLen
    T = b""
    counter = 0

    while len(T) < length:
      C = seed + counter.to_bytes(4, 'big')
      T += self.hash(C).digest()
      counter += 1

    return T[:length]

  def oaep_encode(self, message: bytes, n: int, label: bytes = b"") -> bytes:
    """
    Padding OAEP para cifrado RSA

    Args:
        message: Mensaje a cifrar
        n: Módulo RSA (para calcular tamaño de bloque)
        label: Etiqueta opcional (usualmente vacía)

    Returns:
        Mensaje con padding OAEP
    """
    # Tamaño del módulo en bytes
    k = (n.bit_length() + 7) // 8
    mLen = len(message)

    if mLen > k - 2 * self.hLen - 2:
      raise ValueError(f"Mensaje demasiado largo para OAEP. Máximo: {k - 2 * self.hLen - 2} bytes")

    # Paso 1: Calcular hash de la etiqueta
    lHash = self.hash(label).digest()

    # Paso 2: Generar PS (padding string) de ceros
    PS = b"\x00" * (k - mLen - 2 * self.hLen - 2)

    # Paso 3: Concatenar lHash || PS || 0x01 || message
    DB = lHash + PS + b"\x01" + message

    # Paso 4: Generar semilla aleatoria
    seed = random.randbytes(self.hLen)

    # Paso 5: dbMask = MGF(seed, k - hLen - 1)
    dbMask = self.mgf1(seed, k - self.hLen - 1)

    # Paso 6: maskedDB = DB ⊕ dbMask
    maskedDB = bytes(a ^ b for a, b in zip(DB, dbMask))

    # Paso 7: seedMask = MGF(maskedDB, hLen)
    seedMask = self.mgf1(maskedDB, self.hLen)

    # Paso 8: maskedSeed = seed ⊕ seedMask
    maskedSeed = bytes(a ^ b for a, b in zip(seed, seedMask))

    # Paso 9: EM = 0x00 || maskedSeed || maskedDB
    EM = b"\x00" + maskedSeed + maskedDB

    return EM

  def oaep_decode(self, encoded_message: bytes, n: int, label: bytes = b"") -> bytes:
    """
    Elimina padding OAEP para descifrado

    Args:
        encoded_message: Mensaje con padding OAEP
        n: Módulo RSA
        label: Etiqueta opcional (debe coincidir con cifrado)

    Returns:
        Mensaje original
    """
    # Tamaño del módulo en bytes
    k = (n.bit_length() + 7) // 8

    if len(encoded_message) != k:
      raise ValueError(f"Mensaje codificado incorrecto. Esperado: {k} bytes, recibido: {len(encoded_message)}")

    # Paso 1: Separar EM
    if encoded_message[0] != 0x00:
      raise ValueError("OAEP decoding error: Primer byte no es 0x00")

    maskedSeed = encoded_message[1:1 + self.hLen]
    maskedDB = encoded_message[1 + self.hLen:]

    # Paso 2: seedMask = MGF(maskedDB, hLen)
    seedMask = self.mgf1(maskedDB, self.hLen)

    # Paso 3: seed = maskedSeed ⊕ seedMask
    seed = bytes(a ^ b for a, b in zip(maskedSeed, seedMask))

    # Paso 4: dbMask = MGF(seed, k - hLen - 1)
    dbMask = self.mgf1(seed, k - self.hLen - 1)

    # Paso 5: DB = maskedDB ⊕ dbMask
    DB = bytes(a ^ b for a, b in zip(maskedDB, dbMask))

    # Paso 6: Verificar lHash
    lHash = self.hash(label).digest()

    if DB[:self.hLen] != lHash:
      raise ValueError("OAEP decoding error: Hash de etiqueta incorrecto")

    # Paso 7: Encontrar el 0x01 que separa PS del mensaje
    try:
      # Buscar el primer byte 0x01 después de lHash
      idx = DB[self.hLen:].index(b"\x01") + self.hLen
    except ValueError:
      raise ValueError("OAEP decoding error: Separador 0x01 no encontrado")

    # Paso 8: Extraer mensaje (todo después del 0x01)
    message = DB[idx + 1:]

    return message


class RSA_Enhanced(RSA_from_Scratch):
  """Implementación mejorada de RSA con OAEP y formato PEM"""

  def __init__(self):
    super().__init__()
    self.oaep = OAEP()

  def encrypt(self, plaintext: bytes, public_key: Tuple[int, int]) -> bytes:
    """
    Cifra datos usando RSA-OAEP

    Args:
        plaintext: Datos a cifrar (bytes)
        public_key: Tupla (e, n)

    Returns:
        Datos cifrados (bytes)
    """
    e, n = public_key
    k = (n.bit_length() + 7) // 8

    # Aplicar OAEP padding
    padded_data = self.oaep.oaep_encode(plaintext, n)

    # Convertir a entero para RSA
    m = int.from_bytes(padded_data, 'big')

    # Cifrar con RSA
    c = pow(m, e, n)

    # Convertir a bytes
    return c.to_bytes(k, 'big')

  def decrypt(self, ciphertext: bytes, private_key: Tuple[int, int]) -> bytes:
    """
    Descifra datos usando RSA-OAEP

    Args:
        ciphertext: Datos cifrados (bytes)
        private_key: Tupla (d, n)

    Returns:
        Datos originales (bytes)
    """
    d, n = private_key
    k = (n.bit_length() + 7) // 8

    if len(ciphertext) != k:
      raise ValueError(f"Ciphertext incorrecto. Esperado: {k} bytes")

    # Convertir a entero
    c = int.from_bytes(ciphertext, 'big')

    # Descifrar con RSA
    m = pow(c, d, n)

    # Convertir a bytes
    padded_data = m.to_bytes(k, 'big')

    # Eliminar padding OAEP
    return self.oaep.oaep_decode(padded_data, n)

  def encrypt_long_message(self, plaintext: bytes, public_key: Tuple[int, int]) -> bytes:
    """
    Cifra mensajes largos dividiéndolos en bloques

    Args:
        plaintext: Mensaje largo a cifrar
        public_key: Tupla (e, n)

    Returns:
        Lista de bloques cifrados concatenados
    """
    e, n = public_key
    k = (n.bit_length() + 7) // 8

    # Máximo tamaño de datos por bloque (considerando OAEP)
    max_data_len = k - 2 * self.oaep.hLen - 2

    if len(plaintext) <= max_data_len:
      return self.encrypt(plaintext, public_key)

    # Dividir en bloques
    cipher_blocks = []
    for i in range(0, len(plaintext), max_data_len):
      block = plaintext[i:i + max_data_len]
      cipher_block = self.encrypt(block, public_key)
      cipher_blocks.append(cipher_block)

    # Juntar todos los bloques
    return b''.join(cipher_blocks)

  def decrypt_long_message(self, ciphertext: bytes, private_key: Tuple[int, int]) -> bytes:
    """
    Descifra mensajes largos divididos en bloques

    Args:
        ciphertext: Mensaje cifrado (múltiples bloques)
        private_key: Tupla (d, n)

    Returns:
        Mensaje original
    """
    d, n = private_key
    k = (n.bit_length() + 7) // 8

    if len(ciphertext) % k != 0:
      raise ValueError(f"Ciphertext no es múltiplo del tamaño de bloque {k}")

    # Procesar cada bloque
    plaintext_blocks = []
    num_blocks = len(ciphertext) // k

    for i in range(num_blocks):
      block = ciphertext[i * k:(i + 1) * k]
      plain_block = self.decrypt(block, private_key)
      plaintext_blocks.append(plain_block)

    return b''.join(plaintext_blocks)

  def generate_rsa_key_object(self, bits: int = 2048) -> RSAKey:
    """
    Genera par de claves RSA devolviendo objeto estructurado

    Args:
        bits: Tamaño de clave (2048 recomendado mínimo)

    Returns:
        Objeto RSAKey con componentes
    """
    (e, n), (d, n) = self.generate_RSA_keys(bits)
    return RSAKey(n=n, e=e, d=d)

  def export_private_key_pem(self, rsa_key: RSAKey) -> str:
    """
    Exporta clave privada en formato PEM

    Args:
        rsa_key: Objeto RSAKey con componentes

    Returns:
        String en formato PEM
    """
    # Estructura simplificada (en realidad PKCS#1 es más complejo)
    key_data = {
        "n": rsa_key.n,
        "e": rsa_key.e,
        "d": rsa_key.d,
        "format": "RSA-PKCS1"
    }

    # Convertir a JSON y luego base64
    json_str = json.dumps(key_data, separators=(',', ':'))
    b64_key = base64.b64encode(json_str.encode()).decode()

    # Formato PEM
    pem = "-----BEGIN RSA PRIVATE KEY-----\n"
    # Dividir en líneas de 64 caracteres
    for i in range(0, len(b64_key), 64):
      pem += b64_key[i:i + 64] + "\n"
    pem += "-----END RSA PRIVATE KEY-----"

    return pem

  def export_public_key_pem(self, rsa_key: RSAKey) -> str:
    """
    Exporta clave pública en formato PEM

    Args:
        rsa_key: Objeto RSAKey con componentes

    Returns:
        String en formato PEM
    """
    key_data = {
        "n": rsa_key.n,
        "e": rsa_key.e,
        "format": "RSA-PKCS1"
    }

    json_str = json.dumps(key_data, separators=(',', ':'))
    b64_key = base64.b64encode(json_str.encode()).decode()

    pem = "-----BEGIN RSA PUBLIC KEY-----\n"
    for i in range(0, len(b64_key), 64):
      pem += b64_key[i:i + 64] + "\n"
    pem += "-----END RSA PUBLIC KEY-----"

    return pem

  def import_key_pem(self, pem_string: str) -> RSAKey:
    """
    Importa clave desde formato PEM

    Args:
        pem_string: String en formato PEM

    Returns:
        Objeto RSAKey
    """
    # Extraer contenido base64
    lines = pem_string.strip().split('\n')
    b64_content = ''.join(lines[1:-1])  # Saltar cabeceras
    json_str = base64.b64decode(b64_content).decode()
    key_data = json.loads(json_str)

    return RSAKey(
        n=key_data['n'],
        e=key_data.get('e'),
        d=key_data.get('d')
    )


def demo_enhanced():
  """Demostración de la implementación mejorada"""
  print("=== RSA Mejorado con OAEP y PEM ===")

  rsa = RSA_Enhanced()

  # 1. Generar claves
  print("\n1. Generando claves RSA-2048...")
  key_obj = rsa.generate_rsa_key_object(bits=2048)

  # 2. Exportar claves PEM
  print("\n2. Exportando claves en formato PEM...")
  private_pem = rsa.export_private_key_pem(key_obj)
  public_pem = rsa.export_public_key_pem(key_obj)

  print("Clave privada PEM (primeras 100 chars):")
  print(private_pem[:100] + "...")
  print("\nClave pública PEM (primeras 100 chars):")
  print(public_pem[:100] + "...")

  # 3. Importar claves
  print("\n3. Importando claves desde PEM...")
  imported_private = rsa.import_key_pem(private_pem)

  # 4. Cifrado/descifrado con OAEP
  print("\n4. Prueba de cifrado con OAEP...")
  mensaje = b"Este es un mensaje secreto que demuestra RSA-OAEP!"

  # Cifrar
  cifrado = rsa.encrypt(mensaje, key_obj.public_key())
  print(f"Mensaje original: {mensaje}")
  print(f"Cifrado (primeros 50 bytes): {cifrado[:50].hex()}...")

  # Descifrar
  descifrado = rsa.decrypt(cifrado, key_obj.private_key())
  print(f"Descifrado: {descifrado}")
  print(f"¿Coincide? {mensaje == descifrado}")

  # 5. Mensaje largo
  print("\n5. Prueba con mensaje largo...")
  mensaje_largo = b"X" * 1000  # 1000 bytes

  cifrado_largo = rsa.encrypt_long_message(mensaje_largo, key_obj.public_key())
  descifrado_largo = rsa.decrypt_long_message(cifrado_largo, key_obj.private_key())

  print(f"Mensaje largo original (primeros 50): {mensaje_largo[:50]}...")
  print(f"Descifrado largo (primeros 50): {descifrado_largo[:50]}...")
  print(f"¿Coinciden completos? {mensaje_largo == descifrado_largo}")

  # 6. Comparación con RSA "textbook" (peligroso)
  print("\n6. Demostración vulnerabilidad RSA sin OAEP...")
  test_msg = b"ATACAR"

  # Sin OAEP (solo para demostración)
  num_msg = int.from_bytes(test_msg, 'big')
  cifrado_sin = pow(num_msg, key_obj.e, key_obj.n)
  descifrado_sin = pow(cifrado_sin, key_obj.d, key_obj.n)

  print(f"Mensaje original: {test_msg}")
  print(f"Cifrado sin OAEP: {cifrado_sin}")
  print(f"Descifrado sin OAEP: {descifrado_sin}")

  # Mostrar que es determinístico
  cifrado_sin2 = pow(num_msg, key_obj.e, key_obj.n)
  print(f"Segundo cifrado mismo mensaje: {cifrado_sin2}")
  print(f"¿Son iguales? {cifrado_sin == cifrado_sin2} <- ¡PROBLEMA!")


if __name__ == "__main__":
  demo_enhanced()
