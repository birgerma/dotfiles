#!/bin/python3
# Source: https://eioki.eu/2021/01/12/tmux-and-fzf-fuzzy-tmux-session-window-pane-switcher
#
# customizable
# LIST_DATA="#{window_name} #{pane_title} #{pane_current_path} #{pane_current_command}"
import subprocess
import os
from pyfzf import FzfPrompt
import time

DEBUG = False
DEBUG = True
LOG_PATH = os.getenv("HOME")+'/.local/bin/log.txt'
SCRIPT_PATH = os.path.abspath(__file__)

PROJECT_FOLDERS = ["~/projects", "~/.config/dotfiles"]

tmux_sessions, tmuxinator_sessions, local_tmuxinator_paths, project_folders = [],[],[],[]

def debug(msg):
  if DEBUG:
    with open(LOG_PATH, 'a') as f:
      f.write(msg)
      f.write('\n')
# List current tmux sessions:
def get_tmux_sessions():
  res = os.popen("tmux list-sessions").read()
  res = res.split("\n")
  sessions = []
  for r in res:
    r = r.split(" ")
    name = r[0][:-1]
    if name=='':
      continue
    windows = " ".join(r[1:3])
    created = " ".join(r[3:])
    sessions.append({'name':name, 'win':windows, 'created':created})

  return sessions

def get_tmuxinator_sessions(tmux_sessions=None):
  tmux_sessions = [session['name'] for session in tmux_sessions]
  res = os.popen("tmuxinator list").read()
  debug("tmux sessions res 1:"+str(res))
  res = res.split("\n")[1:]

  debug("tmux sessions res:"+str(res))
  sessions = []
  for line in res:
    sessions+=line.split(' ')
    
  sessions = list(filter(lambda x: x!='', sessions))
    
  debug("session names:"+str(sessions))
    
  debug("All tmuxinator sessions:"+str(sessions))
  if tmux_sessions:
    filtered = []
    for session in sessions:
      # debug("fiter tmux sessions:"+str(session))
      if session not in tmux_sessions:
        filtered.append(session)
    sessions = filtered
  return sessions

def get_local_tmuxinator():
  results = []
  for folder in PROJECT_FOLDERS:
    cmd = "fd -H .tmuxinator.yml "+folder
    res = os.popen(cmd).read()
    res = res.split("\n")[:-1]
    results+=res

  home = os.getenv("HOME")
  for i in range(len(results)):
    results[i]= results[i].replace(home, '~')
    results[i] = results[i].replace('.tmuxinator.yml', '')
  return results

def get_project_folders():
  results = []
  folders = " ".join(PROJECT_FOLDERS)
  cmd = "fd . " + folders +" -t d --min-depth 0 --max-depth 3"
  results = os.popen(cmd).read().split('\n')[:-1]
  for f in PROJECT_FOLDERS:
    results.append(f)
  home = os.getenv("HOME")
  for i in range(len(results)):
    results[i]= results[i].replace(home, '~')
    results[i] = results[i].replace('.tmuxinator.yml', '')
  return results

def is_tmux_session(session, tmux_sessions):
  for s in tmux_sessions:
    if s['name']==session:
      return True
  return False

def is_tmuxinator_session(session, tmuxinator_sessions):
  for s in tmuxinator_sessions:
    if s==session:
      return True
  return False

def is_local_tmuxinator_session(session, local_tmuxinator_sessions):
  for s in local_tmuxinator_sessions:
    if s==session:
      return True
  return False

def is_folder(arg):
  # print(arg)
  home = os.getenv("HOME")
  path = arg.replace('~',home)

  # path = os.path.abspath(arg)
  # print(path)
  return os.path.isdir(path)

def is_in_tmux():
  TERM = os.getenv("TERM", default="None")
  TMUX = os.getenv("TMUX", default="None")

  debug("TERM="+TERM + " TMUX="+TMUX)

  return (TERM.startswith('screen') or TERM.startswith('tmux')) and TMUX is not None

def open_tmux_session(selected):
  if is_in_tmux():
    debug("Is in tmux session, switch")
    cmd = 'tmux switch -t ' + selected
  else:
    debug("Is not in tmux session, attach")
    cmd = 'tmux attach -t ' + selected
  os.system(cmd)
    
def create_tmux_session(name, path=None):
  cmd = 'tmux new -ds '+name
  if path:
    cmd+=' -c ' + path
  subprocess.Popen(cmd, shell=True)
  time.sleep(.01)

def open_tmuxinator_session(selected, local=False):
  # print("Open tmuxinator session")
  if local:
    home = os.getenv("HOME")
    path = selected.replace('~',home)
    os.chdir(path)
    cmd = 'tmuxinator local'
  else:
    cmd = 'tmuxinator ' + selected
  os.system(cmd)
  # subprocess.Popen(cmd, shell=True)
  
def get_all_session_names():
  global tmux_sessions, tmuxinator_sessions, local_tmuxinator_paths, project_folders
  tmux_sessions = get_tmux_sessions()
  # print("Tmux sessions:", tmux_sessions)
  tmuxinator_sessions = get_tmuxinator_sessions(tmux_sessions)
  # print("tmuxinator_sessions:", tmuxinator_sessions)
  debug("get all sesson names, tmuxinator sessons:" + str(tmuxinator_sessions))

  local_tmuxinator_paths = get_local_tmuxinator()

  project_folders= get_project_folders()

  session_names = []
  for s in tmux_sessions:
    session_names.append(s['name'])

  session_names+=tmuxinator_sessions
  session_names+=local_tmuxinator_paths
  session_names+=project_folders
  return session_names

def preview_function(arg):
  debug("Preview function arg:"+str(arg))
  debug("Tmuxinator sessons:"+str(tmuxinator_sessions))
  if is_tmux_session(arg, tmux_sessions):
    subprocess.Popen('tmux capture-pane -pet '+arg, shell=True)
  elif is_tmuxinator_session(arg, tmuxinator_sessions):
    debug("Preview tmuxinator")
    conf = os.getenv("XDG_CONFIG_HOME", '~/.config') + '/tmuxinator/' + arg + '.yml'
    debug("Conf dir:"+str(conf))
    subprocess.Popen('bat --color always '+ conf, shell=True)
  elif is_local_tmuxinator_session(arg, local_tmuxinator_paths):
    conf = arg + '.tmuxinator.yml'
    subprocess.Popen('bat --color always '+ conf, shell=True)
  elif is_folder(arg): 
    subprocess.Popen('tree -C -L 5 '+ arg, shell=True)
  else:
    print(tmuxinator_sessions)
    print("Unknown preview")

def select_session_name(session_names):
  fzf = FzfPrompt()
  selected = fzf.prompt(session_names, fzf_options="--print-query --preview='" + SCRIPT_PATH + " {}' --header '<End with space to force create new session>'")
  if len(selected)==0:
    return False
  if selected[0].endswith(' '):
    return selected[0].strip()
  return selected[-1]

def go_to_session(selected):
  global tmux_sessions, tmuxinator_sessions, local_tmuxinator_paths, project_folders

  if is_tmux_session(selected, tmux_sessions):
    debug("Is tmux session")
    open_tmux_session(selected)
  elif selected in tmuxinator_sessions:
    debug("Is tmuxinator session")
    open_tmuxinator_session(selected)
  elif selected in local_tmuxinator_paths:
    debug("Is local tmuxinator session")
    open_tmuxinator_session(selected, local=True)
  elif selected in project_folders:
    path = selected
    name = list(filter(None, selected.split('/')))[-1]
    create_tmux_session(name, path)
    open_tmux_session(name)
  else:
    debug("Session does not exist, create")
    create_tmux_session(selected)
    open_tmux_session(selected)


def fuzzy_find_session(session_names):
  selected = select_session_name(session_names)
  if selected:
    debug("Selected:"+selected)
    go_to_session(selected)
  else:
    debug("Nothing selected")

def main(args):
  debug("tmux-fzf.py called")
  session_names = get_all_session_names()
  if len(sys.argv)<2:
    fuzzy_find_session(session_names)
  else:
    debug("Preview argument:"+str(args[1]))
    preview_function(args[1])

import sys
if __name__=='__main__':
  # folders = get_project_folders()
  # print(folders)
  # exit(0)
  # try:
  # print("Args:", sys.argv)
  args = sys.argv
  main(args)
  # except Exception as e:
    # print("Caught exception:", e)
    # debug(str(e))

exit(0)
