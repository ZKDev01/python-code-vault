### Ejemplo de Salida

```
============================================================
DEMOSTRACIÓN RSA CON OAEP Y FORMATO PEM
============================================================

1. GENERANDO CLAVES RSA
----------------------------------------
Generando claves RSA de 1024 bits...
Generando primer primo de ~512 bits...
Primer primo generado: 512 bits
Generando segundo primo de ~512 bits...
Segundo primo generado: 512 bits
n = p * q = 1024 bits
Claves generadas en 0.09 segundos

Clave generada:
  n: 1024 bits
  e: 65537
  d: 41358690628181005846890685958342702241483210915542627283214462070544935021259180833745075486995575026896116541192809666360890153352735709495300905834345339977824511795409760174958368893742589910476523612349786632962858
379168433816237513688205626333860799271296596360832272093507284618843768240325327238846977
2. EXPORTACIÓN/IMPORTACIÓN PEM
----------------------------------------
Clave privada PEM:
-----BEGIN RSA PRIVATE KEY-----
eyJ2ZXJzaW9uIjoiMS4wIiwibiI6OTE5MTk1Nzc3MTYzMjg2Mjc5MjI4MDUwMzU0
NjA...

Clave pública PEM:
-----BEGIN RSA PUBLIC KEY-----
eyJ2ZXJzaW9uIjoiMS4wIiwibiI6OTE5MTk1Nzc3MTYzMjg2Mjc5MjI4MDUwMzU0
NjAy...

Claves importadas correctamente: True

3. CIFRADO/DESCIFRADO BÁSICO
----------------------------------------

Mensaje 1: b'Hola Mundo!'
  Cifrado: 43a468fde72d204ae9fc5b19f07ad5daa7bcfa11... (128 bytes)
  Descifrado: b'Hola Mundo!'
  Correcto: True

Mensaje 2: b'RSA con OAEP es seguro'
  Cifrado: 147bb1e2172b117bdf0b2ceccb24de6932bb7255... (128 bytes)
  Descifrado: b'RSA con OAEP es seguro'
  Correcto: True

Mensaje 3: b'1234567890'
  Cifrado: 4f5a79ec993d46c8c83d320667d60b0c370dac59... (128 bytes)
  Descifrado: b'1234567890'
  Correcto: True

Mensaje 4: b'Clave: AES-256-GCM'
  Cifrado: 5d40e00d0bb51fd20470d838252313017f9e415b... (128 bytes)
  Descifrado: b'Clave: AES-256-GCM'
  Correcto: True

4. MENSAJE LARGO
----------------------------------------
Mensaje original: 480 bytes
Bloques cifrados: 8
Mensaje descifrado: 480 bytes
Correcto: True

5. PROPIEDADES DE SEGURIDAD
----------------------------------------
Mismo mensaje cifrado dos veces:
  Cifrado 1: 0bb81531c6bbad53df8dea87b58b79df...
  Cifrado 2: 53adef5a4858a6ae5213c1252794981e...
  ¿Son iguales? False (debería ser False)
  Descifrado 1: b'Texto confidencial'
  Descifrado 2: b'Texto confidencial'
  Ambos correctos: True

6. LÍMITES Y VALIDACIONES
----------------------------------------
Para clave de 1024 bits:
  Tamaño de bloque (k): 128 bytes
  Hash (hLen): 32 bytes (SHA-256)
  Máximo mensaje por bloque: 62 bytes

Intentando cifrar mensaje de 162 bytes...
  Requeriría 3 bloques

============================================================
DEMOSTRACIÓN COMPLETADA
============================================================
```
