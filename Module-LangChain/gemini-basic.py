from personal_tool import get_model

def main():
  model = get_model()
  result = model.invoke("Que es un LLM?")
  print(result)

if __name__ == '__main__':
  main()