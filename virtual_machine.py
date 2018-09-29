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
