import os

value = os.environ.get("SENTRY_DSN", "None")
if value != "None":
  value = f'"{value}"'

f = open("seamapi/utils/get_sentry_dsn.py", "w")
f.write(f"""
def get_sentry_dsn():
  return {value}
""")
