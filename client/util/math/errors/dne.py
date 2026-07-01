class DoesNotExistError(Exception):
  def __init__(self, message):
    super().__init__(f"Does not exist: {message}")