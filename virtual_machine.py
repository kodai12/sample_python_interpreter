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

    def run_frame(self, frame):
      """Run a frame until it returns (somehow).
      Exceptions are raised, the return value is returned.
      """
      self.push_frame(frame)
      while True:
        byte_name, arguments = self.parse_byte_and_args()

        why = self.dispatch(byte_name, arguments)

        # Deal with any block management we need to do
        while why and frame.block_stack:
          why = self.manage_block_stack(why)

          if why:
            break

      self.pop_frame()

      if why == 'exception':
        exc, val, tb = self.last_exception
        e = exc(val)
        e.__traceback__ = tb
        raise e

      return self.return_value

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

  def parse_byte_and_args(self):
    f = self.frame
    opoffset = f.last_instruction
    byte_code = f.code_obj.co_code[opoffset]
    f.last_instruction += 1
    byte_name = dis.opname[byte_code]
    if byte_code >= dis.HAVE_ARGUMENT:
      # index into the bytecode
      arg = f.code_obj.co_code[f.last_instruction:f.last_instruction+2]
      f.last_instruction += 2   # advance the instruction pointer
      arg_val = arg[0] + (arg[1] * 256)
      if byte_code in dis.hasconst:   # Look up a constant
        arg = f.code_obj.co_consts[arg_val]
      elif byte_code in dis.hasname:  # Look up a name
        arg = f.code_obj.co_names[arg_val]
      elif byte_code in dis.haslocal: # Look up a local name
        arg = f.code_obj.co_varnames[arg_val]
      elif byte_code in dis.hasjrel:  # Calculate a relative jump
        arg = f.last_instruction + arg_val
      else:
        arg = arg_val
        argument = [arg]
    else:
      argument = []

    return byte_name, argument

  def dispatch(self, byte_name, argument):
    """ Dispatch by bytename to the corresponding methods.
    Exceptions are caught and set on the virtual machine."""
    why = None
    try:
      bytecode_fn = getattr(self, 'byte_%s' % byte_name, None)
      if bytecode_fn is None:
        if byte_name.startswith('UNARY_'):
          self.unaryOperator(byte_name[6:])
        elif byte_name.startswith('BINARY_'):
          self.binaryOperator(byte_name[7:])
        else:
          raise VirtualMachineError(
            "unsupported bytecode type: %s" % byte_name
          )
        else:
          why = bytecode_fn(*argument)
    except:
      # deal with exceptions encountered while executing the op.
      self.last_exception = sys.exc_info()[:2] + (None,)
      why = 'exception'

    return why
