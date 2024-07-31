import noise
import numpy as np
from PIL import Image

def main():
  pass

def rgb_norm(world):
  world_min = np.min(world)
  world_max = np.max(world)
  norm = lambda x: (x-world_min/(world_max - world_min))*255
  return np.vectorize(norm)

def prep_world(world):
  norm = rgb_norm(world)
  world = norm(world)
  return world

def testing1():
  shape = (1024,1024)
  scale = 100
  octaves = 6
  persistence = 0.5
  lacunarity = 2.0
  seed = np.random.randint(0, 100)
  seed = 126

  world = np.zeros(shape)
  for i in range(shape[0]):
    for j in range(shape[1]):
      world[i][j] = noise.pnoise2(
        i/scale,
        j/scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=1024,
        repeaty=1024,
        base=seed)
  Image.fromarray(prep_world(world)).show()

if __name__ == '__main__':
  testing1()