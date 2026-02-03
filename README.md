# Terminal Widget (PyQt5)

A reusable PyQt5 terminal-style widget

Designed to be embedded inside other PyQt applications as a normal widget.

---

## 📦 Installation (as Git submodule)

Add this repository as a submodule inside your project:

```bash
git submodule add https://github.com/<yourname>/terminal_widget.git
git submodule update --init --recursive
```

## 🚀 Usage

```python
from terminal_widget import TerminalWidget

self.terminal = TerminalWidget()
layout.addWidget(self.terminal)
```

## 📝 TODO

- Add signals/slots for input/output handling