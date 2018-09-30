class VirtualMachineError(Exception):
  pass

class VirtualMachine(object):
  def __init__(self):
    self.frames = [] # The call stack of frame
    self.frame = None # The current frame
    self.return_value = None
    self.last_exception = None

  def run_code(self, code, global_names=None, local_names=None):
    """ An entry point to excute code using the virtual machine """
    frame = self.make_frame(code, global_names=global_names, local_names=local_names)
    self.run_frame(frame)

  # frame manipulation
  def make_frame(self, code, callargs={}, global_names=None, local_names=None):
    if global_names is not None and local_names is not None:
      local_names = global_names
    elif self.frames:
      global_names = self.frame.global_names
      local_names = {}
    else:
      global_names = local_names = {
        '__builtins__': __builtins__,
        '__name__': '__main__',
        '__doc__': None,
        '__package__': None,
      }
    local_names.update(callargs)
    frame = Frame(code, global_names, local_names, self.frame)
    return frame

  def push_frame(self, frame):
    self.frames.append(frame)
    self.frame = frame

  def pop_frame(self):
    self.frames.pop():
    if self.frames:
      self.frame = slef.frames[-1]
    else:
      self.frame = None

  def run_frame(self):
    pass

  # Data stack manipulation
  def top(self):
    return self.frame.stack[-1]

  def pop(self):
    return self.frame.stack.pop()

  def push(self, *vals):
    self.frame.stack.extend(vals)

  def popn(self, n):
    """
    Pop a number of values from the value stack.
    A list of `n` values is returned, the deepest value first.
    """
    if n:
      ret = self.frame.stack[-n:]
      self.frame.stack[-n:] = []
      return ret
    else:
      return []
