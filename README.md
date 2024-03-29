# i3pie

i3wm ipc library for python.

## Installation

```
pip install i3pie
```

## Usage

```python
>>> import i3pie
>>> with i3pie.Connection() as i3:
...     tree = i3.get_tree()
...     tree._pprint()
...
type='root' name='root'
├─ type='output' name='HDMI-A-0'
│  ├─ type='dockarea' name='bottomdock'
│  ├─ type='con' name='content'
│  │  ├─ type='workspace' name='2'
│  │  │  └─ type='con'
│  │  │     └─ window=50331658 type='con' class='Nemo'
│  │  └─ type='workspace' name='1'
│  │     └─ type='con'
│  │        ├─ window=37748745 type='con' class='URxvt'
│  │        └─ window=25165827 type='con' class='firefox'
│  └─ type='dockarea' name='topdock'
│     └─ window=23068674 type='con' class='Polybar'
└─ type='output' name='__i3'
   └─ type='con' name='content'
      └─ type='workspace' name='__i3_scratch'
         └─ type='floating_con'
            └─ window=44040194 type='con' class='mpv'
```

### Sending commands
```python
>>> import i3pie
>>> i3 = i3pie.Connection()
>>> tree = i3.get_tree()

>>> focused = tree.focused_window()
>>> focused.command('move to workspace 2')
CommandReply(success=True)

>>> windows = list(tree.current_workspace().windows())
>>> i3.command('kill', windows)
CommandReply(success=True)
```

### Working with the tree
```python
>>> import i3pie
>>> i3 = i3pie.Connection()
>>> tree = i3.get_tree()

>>> focused = tree.focused_window()
>>> print(focused)
<Container type='con' class='URxvt'>

>>> focused.workspace()
Container(type='workspace', name='1')

>>> focused.output()
Container(type='output', name='HDMI-A-0')

>>> tree = focused.root()
>>> print(tree)
<Container type='root' name='root'>

>>> list(tree.workspaces())
[Container(type='workspace', name='1'), Container(type='workspace', name='2')]

>>> list(tree.workspaces(scratchpad=True))
[Container(type='workspace', name='__i3_scratch'), Container(type='workspace', name='1'), Container(type='workspace', name='2')]

>>> scratchpad = tree.scratchpad()
>>> print(scratchpad)
<Container type='workspace' name='__i3_scratch'>

>>> list(scratchpad.windows())
[Container(window=44040194, type='con', class='mpv')]

>>> print(list(scratchpad.windows()))
[Container(window=44040194, type='con', class='mpv')]

>>> list(tree.outputs())
[Container(type='output', name='HDMI-A-0')]

>>> tree.find_window(fn=lambda con: 'Firefox' in con.name)
Container(window=25165827, type='con', class='firefox')

>>> tree.find_workspace(fn=lambda w: w.num == 2)
Container(type='workspace', name='2')

>>> for win in tree.windows():
...     if win.window_class == 'URxvt':
...             print(win)
...
<Container type='con' class='URxvt'>

>>> list(tree.filter(fn=lambda con: con.is_window and con.window_class == 'mpv'))
[]

>>> list(tree.filter(fn=lambda con: con.is_window and con.window_class == 'mpv', i3=True))
[Container(window=44040194, type='con', class='mpv')]
```

### Getting workspaces and outputs
```python
>>> import i3pie
>>> i3 = i3pie.Connection()
>>> for workspace in i3.get_workspaces():
...     print(workspace.name)
...
1
2

>>> for output in i3.get_outputs():
...     print(output.name)
...
HDMI-A-0
xroot-0
```

### Getting marks and binding modes
```python
>>> import i3pie
>>> i3 = i3pie.Connection()

>>> print(i3.get_marks())
<MarksReply ['a', '_mark']>

>>> print(i3.get_binding_modes())
<BindingModesReply ['open', 'i3', 'default']>
```

### Subscribe to events
```python
from i3pie import Event, Connection

def callback(self, conn, event, data):
    window = data['container']
    if data['change'] != 'new' or not window:
	     return
    window.command('floating enable')

with Connection() as i3:
    i3.subscribe(Event.WINDOW, callback)
    i3.listen()
```

### Examples

#### Cycling workspaces
```python
import i3pie, argparse

def main(i3):

    parser = argparse.ArgumentParser(description="Cycle i3 workspaces")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-next", action="store_true", help="focus next workspace")
    group.add_argument("-prev", action="store_true", help="focus previous workspace")
    args = parser.parse_args()

    tree = i3.get_tree()
    workspaces = list(tree.workspaces())
    current = tree.current_workspace()

    idx = workspaces.index(current)
    direction = 1 if args.next else -1
    target = workspaces[(idx + direction) % len(workspaces)]
    i3.command(f'workspace "{target.name}"')

if __name__ == "__main__":
    with i3pie.Connection() as i3:
        main(i3)
```

## License

See [LICENSE.txt](LICENSE.txt).
