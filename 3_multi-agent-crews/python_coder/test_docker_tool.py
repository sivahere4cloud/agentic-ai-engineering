from python_coder.docker_tool import RunPythonInDocker

code = """
import hashlib, sys
print(hashlib.sha256(b"siva-test-123").hexdigest())
print(sys.version)
"""

print(RunPythonInDocker().run(code=code))
