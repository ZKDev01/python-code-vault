import random
import math
from typing import Tuple


class RSA_from_Scratch:
  "Implementación Sencilla del Algoritmo RSA"

  def __init__(self):
    self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

  def is_prime(self, n: int) -> bool:
    "Verifica si un número es primo"
    if n < 2:
      return False
    for i in range(2, int(math.sqrt(n)) + 1):
      if n % i == 0:
        return False
    return True

  def gcd(self, a: int, b: int) -> int:
    "Calcula el Máximo Común Divisor usando el algoritmo de Euclides"
    while b != 0:
      a, b = b, a % b
    return a

  def inverse_modular(self, e: int, phi: int) -> int:
    "Calcula el inverso modular d tal que (e * d) % phi = 1"
    # Algoritmo extendido de Euclides
    m0, x0, x1 = phi, 0, 1

    if phi == 1:
      return 0

    while e > 1:
      # q es el cociente
      q = e // phi
      t = phi

      # mcd ahora está en e y phi
      phi, e = e % phi, t
      t = x0
      x0 = x1 - q * x0
      x1 = t

    # Asegurar que x1 es positivo
    if x1 < 0:
      x1 += m0

    return x1

  def generate_RSA_keys(self, bits: int = 16) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Genera un par de claves RSA.

    Args:
      bits: tamaño de los primos

    Returns: (Clave Pública, Clave Privada) donde:
      - Clave Pública = (e, n)
      - Clave Privada = (d, n)
    """
    # Paso 1: Elegir dos primos grandes
    # Esto en la práctica es más complejo y se usa tests de primalidad
    p = self.primes[random.randint(5, len(self.primes) - 1)]
    q = self.primes[random.randint(5, len(self.primes) - 1)]

    # Asegurar que p y q son diferentes
    while p == q:
      q = self.primes[random.randint(5, len(self.primes) - 1)]

    # Paso 2: Calcular n = p * q
    n = p * q
    # Paso 3: Calcular phi(n) = (p-1)*(q-1)
    phi = (p - 1) * (q - 1)

    # Paso 4: Elegir e (exponente público): e debe ser coprimo con phi(n) y 1 < e < phi(n)
    for i in range(3, phi):
      if self.gcd(i, phi) == 1:
        e = i
        break

    # Paso 5: Calcular d (exponente privado)
    d = self.inverse_modular(e, phi)

    return (e, n), (d, n)

  def encrypt_number(self, m: int, public_key: Tuple[int, int]) -> int:
    """Cifra un número usando RSA: C = M^e mod n

    Args:
      m: mensaje como número (debe ser < n)
      public_key: tupla (e, n)

    Returns:
      Texto cifrado como número
    """
    e, n = public_key

    if m >= n:
      raise ValueError(f"Mensaje {m} debe ser menor que n={n}")

    # Usar exponenciación modular para manejar números grandes
    c = pow(m, e, n)
    return c

  def decipher_number(self, c: int, private_key: Tuple[int, int]) -> int:
    """Descifra un número usando RSA: M = C^d mod n

    Args:
        c: Texto cifrado como número
        clave_privada: Tupla (d, n)

    Returns:
        Mensaje original como número
    """
    d, n = private_key

    # Usar exponenciación modular para manejar números grandes
    m = pow(c, d, n)
    return m

  def text_to_number(self, text: str) -> list:
    """Convierte texto a lista de números (códigos ASCII).

    Args:
      texto: Cadena de texto

    Returns:
      Lista de códigos numéricos
    """
    return [ord(caracter) for caracter in text]

  def number_to_text(self, numbers: list) -> str:
    """Convierte lista de números a texto (códigos ASCII).

    Args:
      numeros: Lista de códigos numéricos

    Returns:
      Cadena de texto
    """
    return ''.join(chr(number) for number in numbers)


def main() -> None:
  encrypt = RSA_from_Scratch()

  # 1. Generar claves
  public_key, private_key = encrypt.generate_RSA_keys()
  print(f"Clave Pública: {public_key}")
  print(f"Clave Privada: {private_key}")

  e, n = public_key
  d, n = private_key

  # Mensaje para cifrar/descifrar
  text = "Hello World!"
  number = encrypt.text_to_number(text)
  print(f"Texto original: {text}")
  print(f"Texto como números: {number}")

  # Cifrar cada número
  text_encrypted = [encrypt.encrypt_number(m, public_key) for m in number]
  print(f"Texto cifrado: {text_encrypted}")

  # Descifrar cada número
  text_decrypted = [encrypt.decipher_number(c, private_key) for c in text_encrypted]
  print(f"Números descifrados: {text_decrypted}")

  # Convertir números de vuelta a texto
  text_recovered = encrypt.number_to_text(text_decrypted)
  print(f"Texto recuperado: {text_recovered}")


if __name__ == "__main__":
  main()
