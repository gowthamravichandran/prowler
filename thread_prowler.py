import subprocess
import os
import concurrent.futures
import threading

__dirname__ = os.path.dirname(os.path.abspath(__file__))

lock = threading.Lock()

# Actual call to the shell script to run a check with group id
# ./prowler -g group1
def execute_group_check(group_ID):

  result = ''

  if 'extra' in group_ID:
    result = subprocess.run(
      [os.path.join(__dirname__, 'prowler'), '-M', 'json', '-c', group_ID],
      text=True, 
      capture_output=True
    )
  else:  
    result = subprocess.run(
      [os.path.join(__dirname__, 'prowler'), '-M', 'json', '-g', group_ID],
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
  # groups = ["group1", "group2", "group3", "group4", "cislevel1", "cislevel2", "extras", "forensics-ready", "gdpr", "hipaa", "secrets", "apigateway", "rds"]
  # test_checks = ["check11", "check12"]
  default_groups = ["group1", "group2", "group3", "group4", "extra71","extra72","extra73","extra74","extra75","extra76","extra77","extra78","extra79","extra710","extra711","extra712","extra713","extra714","extra715","extra716","extra717","extra718","extra719","extra720","extra721","extra722","extra723","extra724","extra725","extra726","extra727","extra728","extra729","extra730","extra731","extra732","extra733","extra734","extra735","extra736","extra737","extra738","extra739","extra740","extra741","extra742","extra743","extra744","extra745","extra746","extra747","extra748","extra749","extra750","extra751","extra752","extra753","extra754","extra755","extra756","extra757","extra758","extra761","extra762"]

  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(execute_group_check, default_groups)


def process():
  execute_prowler()
  print('yes its executing all')
  subprocess.call('cat /tmp/prowler_output.json', shell=True)

if __name__ == '__main__':
  process()
