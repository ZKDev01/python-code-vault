from personal_tool import get_model, prompt_template_QA

def testing_1():
  model = get_model()
  result = model.invoke("Que es un LLM?")
  print(result)

def testing_2():
  model = get_model()
  result = prompt_template_QA("Que es la Heuristica", 4, model)
  print(result)

if __name__ == '__main__':
  testing_2()