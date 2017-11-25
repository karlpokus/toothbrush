#!/usr/bin/python
import sys, tty, termios, subprocess, os

DIR_PATH = os.path.expanduser("~/Dropbox/toothbrush_notes")

def getch():
  # Return a single character from stdin.

  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def main_loop():
  # Wait for a key, build up the query string.

  notes = Notes()
  query_string = ''
  mode = 'search'
  while True:
    print '-' * 10
    print 'query: {}'.format(query_string)
    print '-' * 10
    print mode.upper()

    ch = getch()
    if ord(ch) == 3:  # ctrl+c
      raise KeyboardInterrupt
    elif ord(ch) == 127:  # backspace
      query_string = query_string[:-1]
    elif ord(ch) == 13:  # return
      notes.open_all()
      break
    else:
      query_string += ch
    notes.search(query_string)

class Notes:
  def __init__(self):
    self.dir_path = os.path.expanduser(DIR_PATH)
    self.files = {}
    for filename in os.listdir(self.dir_path):
      file_path = os.path.join(self.dir_path, filename)
      if os.path.isdir(file_path):
        continue
      with open(file_path) as f:
        self.files[filename] = f.read()

  def search(self, query_string):
    self.matched_filenames = []

    terms = set(query_string.split())
    for filename, content in self.files.iteritems():
      for term in terms:
        if term not in filename and term not in content:
          break
      else:
        self.matched_filenames.append(filename)

    for i, filename in enumerate(self.matched_filenames[:10]):
      prefix = '{}) '.format(i)
      print '{}{}'.format(prefix, filename)

    if not self.matched_filenames:
      print '~ nothing found ~'

  def open_all(self):
    for filename in self.matched_filenames[:10]:
      path = os.path.join(self.dir_path, filename)
      self.open_path(path)

  def open_path(self, path):
    print 'opening:', path
    os.system('open "{}"'.format(path))

  def new_note(self, query_string):
    new_path = os.path.join(DIR_PATH, query_string)
    with open(new_path, 'w') as f:
      f.write('')
    notes.open_path(new_path)

if __name__ == '__main__':
  main_loop()
