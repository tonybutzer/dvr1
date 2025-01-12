import subprocess
import json

def read_json_to_dict(file_path):
  """
  Reads a JSON file and returns its contents as a Python dictionary.

  Args:
    file_path: The path to the JSON file.

  Returns:
    A Python dictionary containing the data from the JSON file.
  """
  with open(file_path, 'r') as f:
    data = json.load(f)
  return data


def run_command(command):
  """
  Runs a command and captures its output.

  Args:
    command: The command to be executed (e.g., "ls -l").

  Returns:
    A tuple containing:
      - The output of the command as a string.
      - The return code of the command.
  """
  try:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.returncode
  except subprocess.CalledProcessError as e:
    return e.output, e.returncode