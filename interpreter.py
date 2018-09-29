class Interpreter():
  def __init__(self):
    self.stack = []

  def LOAD_VALUE(self, number):
    self.stack.append(number)

  def PRINT_ANSWER(self):
    answer = self.stack.pop()
    print(answer)

  def ADD_TWO_VALUES(self):
    first = self.stack.pop()
    second = self.stack.pop()
    total = first + second
    self.stack.append(total)

  def run_code(self, what_to_excute):
    instructions = what_to_excute["instructions"]
    numbers = what_to_excute["numbers"]
    for each_step in instructions:
      instruction, argument = each_step
      if instruction == "LOAD_VALUE":
        number = numbers[argument]
        self.LOAD_VALUE(number)
      elif instruction == "ADD_TWO_VALUES":
        self.ADD_TWO_VALUES()
      elif instruction == "PRINT_ANSWER":
        self.PRINT_ANSWER()
