import random
import math
import hashlib
import base64
import json
import time
from typing import Tuple, Optional, List
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

    # Para módulos muy pequeños, ajustar
    if k < 2 * self.hLen + 2:
      raise ValueError(f"Módulo demasiado pequeño para OAEP. Mínimo: {2 * self.hLen + 2} bytes")

    mLen = len(message)
    max_msg_len = k - 2 * self.hLen - 2

    if mLen > max_msg_len:
      raise ValueError(f"Mensaje demasiado largo para OAEP. Máximo: {max_msg_len} bytes")

    # Paso 1: Calcular hash de la etiqueta
    lHash = self.hash(label).digest()

    # Paso 2: Generar PS (padding string) de ceros
    PS = b"\x00" * (max_msg_len - mLen)

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


class RSA_Enhanced:
  """Implementación mejorada de RSA con OAEP y formato PEM"""

  def __init__(self):
    self.oaep = OAEP()
    self.small_primes = self._generate_small_primes(1000)

  def _generate_small_primes(self, limit: int) -> List[int]:
    """Genera primos pequeños hasta el límite usando criba de Eratóstenes"""
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]

    for i in range(2, int(limit**0.5) + 1):
      if sieve[i]:
        sieve[i * i:limit + 1:i] = [False] * len(sieve[i * i:limit + 1:i])

    return [i for i, is_prime in enumerate(sieve) if is_prime]

  def _is_probable_prime(self, n: int, k: int = 5) -> bool:
    """
    Test de primalidad de Miller-Rabin optimizado

    Args:
        n: Número a testear
        k: Número de iteraciones

    Returns:
        True si probablemente primo, False si compuesto
    """
    if n < 2:
      return False
    if n in (2, 3):
      return True
    if n % 2 == 0:
      return False

    # Escribir n-1 como 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
      d //= 2
      s += 1

    # Testigo fijo para mejor rendimiento
    test_bases = [2, 3, 5, 7, 11, 13, 17]
    if n < 341550071728321:
      test_bases = [2, 3, 5, 7, 11, 13, 17]
    elif n < 3825123056546413051:
      test_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    else:
      # Para números muy grandes, usar bases aleatorias
      test_bases = [random.randint(2, n - 2) for _ in range(k)]

    for a in test_bases:
      if a >= n:
        continue

      x = pow(a, d, n)
      if x == 1 or x == n - 1:
        continue

      for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
          break
      else:
        return False

    return True

  def generate_large_prime(self, bits: int) -> int:
    """
    Genera un número primo grande de aproximadamente 'bits' bits

    Args:
        bits: Tamaño en bits del primo deseado

    Returns:
        Un número primo probable
    """
    if bits < 8:
      raise ValueError("El tamaño mínimo es 8 bits")

    # Límites para el rango
    min_val = 1 << (bits - 1)  # 2^(bits-1)
    max_val = (1 << bits) - 1  # 2^bits - 1

    attempts = 0
    max_attempts = 10000

    while attempts < max_attempts:
      attempts += 1

      # Generar candidato impar
      candidate = random.randint(min_val, max_val)
      candidate |= 1

      # Filtrar con divisibilidad por primos pequeños
      divisible = False
      for prime in self.small_primes:
        if candidate % prime == 0 and candidate != prime:
          divisible = True
          break

      if divisible:
        continue

      # Test de primalidad
      if self._is_probable_prime(candidate, k=10 if bits <= 512 else 5):
        # Verificación final más rigurosa
        if self._is_probable_prime(candidate, k=20):
          return candidate

    raise ValueError(f"No se pudo generar un primo de {bits} bits después de {max_attempts} intentos")

  def gcd(self, a: int, b: int) -> int:
    """Algoritmo de Euclides para MCD"""
    while b != 0:
      a, b = b, a % b
    return a

  def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
    """Algoritmo extendido de Euclides"""
    if b == 0:
      return a, 1, 0
    gcd, x1, y1 = self.extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

  def mod_inverse(self, a: int, m: int) -> int:
    """Inverso modular usando algoritmo extendido de Euclides"""
    gcd, x, _ = self.extended_gcd(a, m)
    if gcd != 1:
      raise ValueError(f"{a} no tiene inverso módulo {m}")
    return x % m

  def generate_keys(self, bits: int = 2048) -> RSAKey:
    """
    Genera par de claves RSA

    Args:
        bits: Tamaño de clave (recomendado: 2048 o más)

    Returns:
        Objeto RSAKey con claves pública y privada
    """
    if bits < 512:
      raise ValueError("Para RSA con OAEP, se recomienda mínimo 512 bits")

    print(f"Generando claves RSA de {bits} bits...")
    start_time = time.time()

    # Generar dos primos grandes
    prime_bits = bits // 2

    print(f"Generando primer primo de ~{prime_bits} bits...")
    p = self.generate_large_prime(prime_bits)
    print(f"Primer primo generado: {p.bit_length()} bits")

    print(f"Generando segundo primo de ~{prime_bits} bits...")
    q = self.generate_large_prime(prime_bits)
    print(f"Segundo primo generado: {q.bit_length()} bits")

    # Asegurar que p y q son diferentes
    while p == q:
      q = self.generate_large_prime(prime_bits)

    # Calcular n y φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    print(f"n = p * q = {n.bit_length()} bits")

    # Elegir e (exponente público)
    e = 65537  # Valor común y seguro

    # Verificar que e es coprimo con φ(n)
    if self.gcd(e, phi) != 1:
      # Buscar un e alternativo
      e = 3
      while self.gcd(e, phi) != 1:
        e += 2

    # Calcular d (exponente privado)
    d = self.mod_inverse(e, phi)

    elapsed = time.time() - start_time
    print(f"Claves generadas en {elapsed:.2f} segundos")

    return RSAKey(n=n, e=e, d=d, p=p, q=q)

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

    # Aplicar OAEP padding
    padded_data = self.oaep.oaep_encode(plaintext, n)

    # Convertir a entero
    m = int.from_bytes(padded_data, 'big')

    # Cifrar con RSA
    c = pow(m, e, n)

    # Convertir a bytes
    k = (n.bit_length() + 7) // 8
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
      raise ValueError(f"Ciphertext debe tener {k} bytes")

    # Convertir a entero
    c = int.from_bytes(ciphertext, 'big')

    # Descifrar con RSA
    m = pow(c, d, n)

    # Convertir a bytes
    padded_data = m.to_bytes(k, 'big')

    # Eliminar padding OAEP
    return self.oaep.oaep_decode(padded_data, n)

  def encrypt_long(self, plaintext: bytes, public_key: Tuple[int, int]) -> List[bytes]:
    """
    Cifra mensajes largos dividiéndolos en bloques

    Args:
        plaintext: Mensaje largo a cifrar
        public_key: Tupla (e, n)

    Returns:
        Lista de bloques cifrados
    """
    e, n = public_key
    k = (n.bit_length() + 7) // 8

    # Máximo tamaño de datos por bloque (considerando OAEP)
    max_data_len = k - 2 * self.oaep.hLen - 2

    if len(plaintext) <= max_data_len:
      return [self.encrypt(plaintext, public_key)]

    # Dividir en bloques
    cipher_blocks = []
    for i in range(0, len(plaintext), max_data_len):
      block = plaintext[i:i + max_data_len]
      cipher_block = self.encrypt(block, public_key)
      cipher_blocks.append(cipher_block)

    return cipher_blocks

  def decrypt_long(self, cipher_blocks: List[bytes], private_key: Tuple[int, int]) -> bytes:
    """
    Descifra mensajes largos divididos en bloques

    Args:
        cipher_blocks: Lista de bloques cifrados
        private_key: Tupla (d, n)

    Returns:
        Mensaje original
    """
    plaintext_blocks = []
    for block in cipher_blocks:
      plain_block = self.decrypt(block, private_key)
      plaintext_blocks.append(plain_block)

    return b''.join(plaintext_blocks)

  def export_private_key_pem(self, rsa_key: RSAKey) -> str:
    """
    Exporta clave privada en formato PEM simplificado

    Args:
        rsa_key: Objeto RSAKey

    Returns:
        String en formato PEM
    """
    key_data = {
        "version": "1.0",
        "n": rsa_key.n,
        "e": rsa_key.e,
        "d": rsa_key.d,
        "p": rsa_key.p,
        "q": rsa_key.q,
        "timestamp": int(time.time())
    }

    json_str = json.dumps(key_data, separators=(',', ':'))
    b64_key = base64.b64encode(json_str.encode()).decode()

    # Formato PEM
    pem_lines = ["-----BEGIN RSA PRIVATE KEY-----"]
    for i in range(0, len(b64_key), 64):
      pem_lines.append(b64_key[i:i + 64])
    pem_lines.append("-----END RSA PRIVATE KEY-----")

    return "\n".join(pem_lines)

  def export_public_key_pem(self, rsa_key: RSAKey) -> str:
    """
    Exporta clave pública en formato PEM simplificado

    Args:
        rsa_key: Objeto RSAKey

    Returns:
        String en formato PEM
    """
    key_data = {
        "version": "1.0",
        "n": rsa_key.n,
        "e": rsa_key.e,
        "timestamp": int(time.time())
    }

    json_str = json.dumps(key_data, separators=(',', ':'))
    b64_key = base64.b64encode(json_str.encode()).decode()

    # Formato PEM
    pem_lines = ["-----BEGIN RSA PUBLIC KEY-----"]
    for i in range(0, len(b64_key), 64):
      pem_lines.append(b64_key[i:i + 64])
    pem_lines.append("-----END RSA PUBLIC KEY-----")

    return "\n".join(pem_lines)

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
    if len(lines) < 3:
      raise ValueError("Formato PEM inválido")

    b64_content = ''.join(lines[1:-1])  # Saltar cabeceras
    json_str = base64.b64decode(b64_content).decode()
    key_data = json.loads(json_str)

    return RSAKey(
        n=int(key_data['n']),
        e=int(key_data.get('e', 0)),
        d=int(key_data.get('d', 0)) if 'd' in key_data else None,
        p=int(key_data.get('p', 0)) if 'p' in key_data else None,
        q=int(key_data.get('q', 0)) if 'q' in key_data else None
    )


def demo_completa():
  """Demostración completa de RSA con OAEP"""
  print("=" * 60)
  print("DEMOSTRACIÓN RSA CON OAEP Y FORMATO PEM")
  print("=" * 60)

  rsa = RSA_Enhanced()

  # 1. Generar claves
  print("\n1. GENERANDO CLAVES RSA")
  print("-" * 40)

  # Para demostración rápida, usar 1024 bits (en producción usar 2048+)
  key_obj = rsa.generate_keys(bits=1024)

  print(f"\nClave generada:")
  print(f"  n: {key_obj.n.bit_length()} bits")
  print(f"  e: {key_obj.e}")
  print(f"  d: {key_obj.d}")

  # 2. Exportar/importar claves
  print("\n2. EXPORTACIÓN/IMPORTACIÓN PEM")
  print("-" * 40)

  private_pem = rsa.export_private_key_pem(key_obj)
  public_pem = rsa.export_public_key_pem(key_obj)

  print("Clave privada PEM:")
  print(private_pem[:100] + "..." if len(private_pem) > 100 else private_pem)

  print("\nClave pública PEM:")
  print(public_pem[:100] + "..." if len(public_pem) > 100 else public_pem)

  # Importar claves
  imported_private = rsa.import_key_pem(private_pem)
  imported_public = rsa.import_key_pem(public_pem)

  print(f"\nClaves importadas correctamente: {imported_private.n == key_obj.n}")

  # 3. Cifrado/descifrado básico
  print("\n3. CIFRADO/DESCIFRADO BÁSICO")
  print("-" * 40)

  mensajes = [
      b"Hola Mundo!",
      b"RSA con OAEP es seguro",
      b"1234567890",
      b"Clave: AES-256-GCM"
  ]

  for i, mensaje in enumerate(mensajes, 1):
    print(f"\nMensaje {i}: {mensaje}")

    try:
      # Cifrar
      cifrado = rsa.encrypt(mensaje, key_obj.public_key())
      print(f"  Cifrado: {cifrado[:20].hex()}... ({len(cifrado)} bytes)")

      # Descifrar
      descifrado = rsa.decrypt(cifrado, key_obj.private_key())
      print(f"  Descifrado: {descifrado}")
      print(f"  Correcto: {mensaje == descifrado}")
    except ValueError as e:
      print(f"  Error: {e}")

  # 4. Mensaje largo
  print("\n4. MENSAJE LARGO")
  print("-" * 40)

  mensaje_largo = b"Este es un mensaje mas largo que necesita ser dividido en bloques para el cifrado RSA con OAEP. " * 5

  print(f"Mensaje original: {len(mensaje_largo)} bytes")

  # Cifrar mensaje largo
  bloques_cifrados = rsa.encrypt_long(mensaje_largo, key_obj.public_key())
  print(f"Bloques cifrados: {len(bloques_cifrados)}")

  # Descifrar
  mensaje_descifrado = rsa.decrypt_long(bloques_cifrados, key_obj.private_key())
  print(f"Mensaje descifrado: {len(mensaje_descifrado)} bytes")
  print(f"Correcto: {mensaje_largo == mensaje_descifrado}")

  # 5. Propiedades de seguridad
  print("\n5. PROPIEDADES DE SEGURIDAD")
  print("-" * 40)

  # Mostrar que el mismo mensaje cifrado dos veces da resultados diferentes
  mensaje = b"Texto confidencial"
  cifrado1 = rsa.encrypt(mensaje, key_obj.public_key())
  cifrado2 = rsa.encrypt(mensaje, key_obj.public_key())

  print(f"Mismo mensaje cifrado dos veces:")
  print(f"  Cifrado 1: {cifrado1[:16].hex()}...")
  print(f"  Cifrado 2: {cifrado2[:16].hex()}...")
  print(f"  ¿Son iguales? {cifrado1 == cifrado2} (debería ser False)")

  # Verificar que ambos se pueden descifrar
  descifrado1 = rsa.decrypt(cifrado1, key_obj.private_key())
  descifrado2 = rsa.decrypt(cifrado2, key_obj.private_key())
  print(f"  Descifrado 1: {descifrado1}")
  print(f"  Descifrado 2: {descifrado2}")
  print(f"  Ambos correctos: {descifrado1 == descifrado2 == mensaje}")

  # 6. Límites y validaciones
  print("\n6. LÍMITES Y VALIDACIONES")
  print("-" * 40)

  k = (key_obj.n.bit_length() + 7) // 8
  max_len = k - 2 * rsa.oaep.hLen - 2
  print(f"Para clave de {key_obj.n.bit_length()} bits:")
  print(f"  Tamaño de bloque (k): {k} bytes")
  print(f"  Hash (hLen): {rsa.oaep.hLen} bytes (SHA-256)")
  print(f"  Máximo mensaje por bloque: {max_len} bytes")

  # Intentar cifrar mensaje muy largo
  mensaje_muy_largo = b"X" * (max_len + 100)
  print(f"\nIntentando cifrar mensaje de {len(mensaje_muy_largo)} bytes...")
  try:
    bloques = rsa.encrypt_long(mensaje_muy_largo, key_obj.public_key())
    print(f"  Requeriría {len(bloques)} bloques")
  except ValueError as e:
    print(f"  Error esperado: {e}")

  print("\n" + "=" * 60)
  print("DEMOSTRACIÓN COMPLETADA")
  print("=" * 60)


def demo_rapida():
  """Demostración rápida con claves pequeñas para desarrollo"""
  print("DEMOSTRACIÓN RÁPIDA RSA (768 bits)")
  print("-" * 40)

  rsa = RSA_Enhanced()

  # Generar claves más pequeñas para desarrollo rápido
  print("Generando claves RSA de 768 bits...")
  key_obj = rsa.generate_keys(bits=768)

  print(f"\nClave generada:")
  print(f"  n: {key_obj.n.bit_length()} bits")

  # Mensaje de prueba
  mensaje = b"Prueba RSA-OAEP"
  print(f"\nMensaje: {mensaje}")

  # Cifrar
  cifrado = rsa.encrypt(mensaje, key_obj.public_key())
  print(f"Cifrado: {cifrado[:20].hex()}...")

  # Descifrar
  descifrado = rsa.decrypt(cifrado, key_obj.private_key())
  print(f"Descifrado: {descifrado}")
  print(f"Correcto: {mensaje == descifrado}")

  # Exportar
  print("\nClave pública PEM:")
  print(rsa.export_public_key_pem(key_obj)[:80] + "...")


if __name__ == "__main__":
  import sys

  if len(sys.argv) > 1 and sys.argv[1] == "rapida":
    demo_rapida()
  else:
    demo_completa()
