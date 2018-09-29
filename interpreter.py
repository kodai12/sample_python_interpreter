class Interpreter():
  def __init__(self):
    self.stack = []

  def LOAD_VALUE(self, number):
    self.stack.append(number)

  def PRINT_ANSWER(self):
    answer = self.stack.pop()
    print(answer)

  def ADD_TWO_VALUE(self):
    first = self.stack.pop()
    second = self.stack.pop()
    total = first + second
    self.stack.append(total)
