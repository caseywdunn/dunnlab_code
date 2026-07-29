# tmux Cheat Sheet

Matches `tmux.conf` in this directory (written against tmux 3.4). Lines marked **[cfg]**
are custom bindings from that file, not tmux defaults — they won't exist on a machine
where you haven't installed it.

Prefix is `Ctrl-b`. Written below as `C-b` — press it, release, then the key.

## Install

```bash
# Back up anything already there, then copy the config into place.
cp ~/.tmux.conf ~/.tmux.conf.bak 2>/dev/null
curl -o ~/.tmux.conf https://raw.githubusercontent.com/caseywdunn/dunnlab_code/main/assets/tmux/tmux.conf

# Already running tmux? Pick it up without restarting:
tmux source-file ~/.tmux.conf
```

Check your version with `tmux -V` first. Everything here works on 3.0+; on 2.x the
`-N3` wheel-scroll count and a few copy-mode commands are unavailable.

## Sessions (from the shell)

| Command | Does |
|---|---|
| `tmux` | Start an unnamed session |
| `tmux new -s work` | Start a session named `work` |
| `tmux ls` | List sessions |
| `tmux a` | Attach to the most recent session |
| `tmux a -t work` | Attach to `work` |
| `tmux kill-session -t work` | Kill `work` |
| `tmux kill-server` | Kill everything |

The main reason to use tmux on a cluster: start `tmux new -s job` on the login node,
launch long-running work, then `C-b d` and log out. The session survives the SSH
disconnect; reattach later with `tmux a -t job`.

## Sessions (from inside)

| Key | Does |
|---|---|
| `C-b d` | Detach (session keeps running) |
| `C-b s` | Interactive session list |
| `C-b $` | Rename current session |

## Windows (tabs)

Windows are numbered from **1**, and renumber themselves when one closes, so there are
never gaps. **[cfg]** — stock tmux starts at 0.

| Key | Does |
|---|---|
| `C-b c` | New window, in the current pane's directory **[cfg]** |
| `C-b n` / `C-b p` | Next / previous window |
| `C-b 1`–`9` | Jump to window by number |
| `C-b w` | Window picker |
| `C-b ,` | Rename window (names stick — `allow-rename` is off **[cfg]**) |
| `C-b &` | Kill window (confirms) |

## Panes (splits)

| Key | Does |
|---|---|
| `C-b \|` | Split side by side, inheriting current directory **[cfg]** |
| `C-b -` | Split stacked, inheriting current directory **[cfg]** |
| `C-b %` / `C-b "` | Stock splits — still bound, but start in the *home* directory |
| `Alt-<arrow>` | Move between panes, **no prefix needed** **[cfg]** |
| `C-b <arrow>` | Move between panes |
| `C-b o` | Cycle to next pane |
| `C-b q` | Show pane numbers (press one to jump) |
| `C-b z` | Zoom pane to full window (toggle) |
| `C-b H/J/K/L` | Resize by 5; hold the key to repeat **[cfg]** |
| `C-b x` | Kill pane (confirms) |
| `C-b space` | Cycle through layouts |
| `C-b !` | Break pane into its own window |

Prefer `|` and `-` over `%` and `"` — only the custom ones carry your working
directory into the new pane.

## Scrolling & copy mode

Mouse is on, scrollback is 100,000 lines, and copy mode uses vi keys.

| Key / action | Does |
|---|---|
| Wheel up | Enter copy mode and scroll, 3 lines per notch **[cfg]** |
| `C-b [` or `C-b Enter` **[cfg]** | Enter copy mode |
| `C-b /` | Enter copy mode and search backward **[cfg]** |
| `v` | Start selection |
| `C-v` | Toggle rectangle (column) selection |
| `y` | Copy selection and exit copy mode |
| `/` then `n` / `N` | Search backward, next / previous match |
| `g` / `G` | Top / bottom of scrollback |
| `q` or `Escape` | Leave copy mode |

Mouse selection: drag to select — on release the text is copied and **you stay in copy
mode at your scroll position** **[cfg]**. Stock tmux cancels copy mode and snaps back
to the prompt, losing your place. Double-click copies a word, triple-click copies a
line **[cfg]**.

## Copy & paste to the system clipboard

`set-clipboard on` sends copied text to your terminal via the OSC 52 escape sequence,
so it reaches the clipboard of the machine your **terminal** is running on — including
across SSH, with no X11 forwarding and no `xclip` needed. That's what makes this work
on a cluster login node.

Your local terminal has to allow it:

- **iTerm2** — Preferences ▸ General ▸ Selection ▸ "Applications in terminal may access clipboard"
- **kitty, WezTerm, Alacritty, Windows Terminal, VS Code** — allowed by default
- **GNOME Terminal** — not supported; see the fallback comment at the bottom of `tmux.conf`

To paste **into** tmux, use your terminal's normal paste (`Cmd-V` / `Ctrl-Shift-V`).

`C-b ]` pastes tmux's own internal buffer, which is a **separate register** from the
system clipboard — a common source of confusion. `C-b =` lists those internal buffers.

## Config

| Key | Does |
|---|---|
| `C-b r` | Reload `~/.tmux.conf` and flash a confirmation **[cfg]** |

From the shell instead: `tmux source-file ~/.tmux.conf`.

Other things the config sets that have no keybinding: `escape-time 0` (no lag on Esc in
vim), `focus-events on`, `aggressive-resize on`, and activity flags on background
windows with the bell silenced.

## Handy one-liners

```bash
tmux new -s dev -d                    # create detached, don't attach
tmux send-keys -t dev 'htop' Enter    # run a command in a session
tmux rename-session -t 0 work         # name that accidental unnamed session
tmux list-keys -T copy-mode-vi        # see every copy-mode binding in effect
```
