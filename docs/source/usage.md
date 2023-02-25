# Usage

## Installation

Install PygameYaGUI using pip:

```console
$ pip install pygameyagui
```
```{admonition} About Python version
This package was developed and tested using Python 3.8. Users with other Python versions, please be aware of unforeseen consequences.
```

Also, you can download the zip package of [Pygame-YaGUI.](https://github.com/alxndremaciel/pygameyagui/archive/refs/heads/main.zip)

## Importing

Rename the folder `pygameyagui-main` to `pygameyagui` and put this folder in the same directory of your project. In your project you need to add the following:

```{eval-rst}
.. code-block:: python
    :linenos:

    import sys
    import pygame
    import pygameyagui as ya

    pygame.init()
```

You are all set to use the Pygame-YaGUI environment. You will need to create an interface ({py:class}`pygameyagui.Interface`) that is necessary for hosting (any amount of) toolboxes ({py:class}`pygameyagui.Toolbox`). Each toolbox can have (any amount of) your widgets. Have fun!

## Creating an Interface

Create an {py:class}`pygameyagui.Interface` object with:
```python
interface = ya.Interface()
```
## Creating a Toolbox

Create a {py:class}`pygameyagui.Toolbox` object with:

```python
toolbox = ya.Toolbox(interface, 'This is a Toolbox')
```
 
```{eval-rst}
.. autoclass:: pygameyagui.Toolbox
``` 
## Creating a Widget

A Widget object can be of two types: _output_ and _input_