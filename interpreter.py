class Interpreter():
  def __init__(self):
    self.stack = []
    self.environment = {}

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

  def STORE_NAME(self, name):
    val = self.stack.pop()
    self.environment[name] = val

  def LOAD_NAME(self, name):
    val = self.environment[name]
    self.stack.append(val)

  def parse_argument(self, instruction, argument, what_to_excute):
    """ understand what the argument to each instruction means """
    numbers = ["LOAD_VALUE"]
    names = ["LOAD_NAME", "STORE_NAME"]

    if instruction in numbers:
      argument = what_to_excute["numbers"][argument]
    elif instruction in names:
      argument = what_to_excute["names"][argument]

    return argument

  def execute(self, what_to_excute):
    instructions = what_to_excute["instructions"]
    numbers = what_to_excute["numbers"]
    for each_step in instructions:
      instruction, argument = each_step
      argument = self.parse_argument(instruction, argument, what_to_excute)
      bytecode_method = getattr(self, instruction)

      if argument is None:
        bytecode_method()
      else:
        bytecode_method(argument)
