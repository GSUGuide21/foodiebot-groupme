class DomainError(Exception):
  def __init__(self, message):
    super().__init__(f"Domain error: {message}")