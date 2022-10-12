from seamapi.types import SeamAPIException
import sentry_sdk

"""
A decorator for model methods that will report errors to Sentry (if enabled).
Expects that the model has a `seam` attribute that is a `Seam` instance.
"""
def report_error(f):
  def wrapper(self, *args):
    try:
      return f(self, *args)
    except Exception as error:
      if self.seam.should_report_exceptions and type(error) is not SeamAPIException:
        sentry_sdk.capture_exception(error)

      raise error
  return wrapper
