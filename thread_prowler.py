import subprocess
import os
import concurrent.futures
import threading

__dirname__ = os.path.dirname(os.path.abspath(__file__))

lock = threading.Lock()

# Actual call to the shell script to run a check with group id
# ./prowler -g group1
def execute_group_check(group_ID):

  result = subprocess.run(
    [os.path.join(__dirname__, 'prowler'), '-M', 'json', '-c', group_ID],
    text=True, 
    capture_output=True
  )

  if result.stderr:
    print('error', result.stderr)

  with lock:
    filename = '/tmp/prowler_output.json'
    if os.path.exists(filename):
      append_write = 'a'
    else:
      append_write = 'w'
    with open(filename, append_write) as output_file:
      output_file.write(result.stdout)

def execute_prowler():
  # all group ids
  groups = ["group1", "group2", "group3", "group4", "cislevel1", "cislevel2", "extras", "forensics-ready", "gdpr", "hipaa", "secrets", "apigateway", "rds"]
  default_groups = ["group1", "group2", "group3", "group4", "extras"]
  checks = ["check11", "check12"]
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # executor.map(execute_group_check, default_groups)
    executor.map(execute_group_check, checks)


def process():
  execute_prowler()
  print('yes its executing all')
  subprocess.call('cat /tmp/prowler_output.json', shell=True)

if __name__ == '__main__':
  process()
