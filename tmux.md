# [TMUX](https://github.com/tmux/tmux/wiki)

 > tmux is a terminal multiplexer. It lets you switch easily between several programs in one terminal, detach them (they keep running in the background) and reattach them to a different terminal.

## Configuration

Save under ~/.tmux.conf

```conf
# shortcut for synchronize-panes toggle: Ctrl-b + Ctrl-s
bind C-s set-window-option synchronize-panes
set -g default-terminal "xterm-256color"
# set mouse scroll on
set -g mouse on

# set the scroll buffer size
set-option -g history-limit 50000

# Set the time in milliseconds for which tmux waits after an escape is input to determine if it is part of a function or meta key sequences
set-option -sg escape-time 10

# focus-events
set-option -g focus-events on

# split panes using | and -
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %
```


## Session Shortcuts

| Shortcut | Action |
| ------   | ------ |
| `tmux new -s name` | Creates new session |
| `Ctrl b + s` | switch from current session to different session |
| `tmux ls` | list existing sessions |
| `tmux a -t name` | Attach to session |

## Session commands

Use `Ctrl b + :` to enter the command

| Command | Action |
| ------  | ------ |
| `new -s session-name` | Creates new session with name as `session-name` |
| `capture-pane -S -<n> | Capture last n lines to buffer |
| `save-buffer filename.txt` | Save buffer to filename.txt |

## Pane Shortcuts

| Shortcut | Action |
| ------   | ------ |
| `Ctrl b + d`  | Dettach |
| `Ctrl b + Ctrl S` | Toggle send to all |
| `Ctrl b + \|` | Split vertical |
| `Ctrl b + -` | Split horizontal |
| `Ctrl b + z` | Zoom current pane |
| `Ctrl b + space` | Toggle Pane structure |
| `Ctrl b + arrow` | Move to different pane |
