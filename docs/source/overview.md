# Overview

## Introduction

**Pygame-YaGUI** is a tool to help developers using _Pygame_ as a plataform for creating Graphical Physics simulations. It can be used to control several aspects of a simulation by the means of graphical controls like icons, buttons and others input widgets. Also, output widgets can be used to display information either numerically or in the form of charts.

Another feature of the package is the ability to easily control the flow of time in the simulation by starting, pausing, resuming and resetting the simulation clock.

## A simple example

The image below shows an example of **Pygame-YaGUI** in action. The program is a 2D simulation of a disc (blue circle) confined in a region of space (blue rectangle) obeying simple cinematics rules with a downwards gravity, elastic collision with the confinement walls and no friction. The red arrow represens the disc velocity and the green arrow represents the disc acceleration.

**Pygame-YaGUI** is responsible for providing the small windows with its widgets, the controls at the top right corner and the status bar at the bottom. Nothing related to the drawing of the disc, confinement and arrows is supported by **Pygame-YaGUI** (yet!) and it is implemented by the rest of the simulation.

```{image} pygame-yagui-example.png
:alt: Pygame-YaGUI Example
:width: 700px
:align: center
```

The power of **Pygame-YaGUI** comes from the ability to alter any simulation parameter during runtime (or while the simulation is in idle mode) without having to cancel the simulation and edit the code.

For example, one can use the slider in the _Body Parameters Toolbox_ to have the radius of the disc changed or the dimensions and position of the confinement altered by entering the numbers directly on the fields at the _Box Settings Toolbox_. This are what we call _input widgets_.

In addition to control the simulation parameters, we can use _output widgets_ to display information. One example is at the _Energy Toolbox_ where it is located three charts showing the values for different kinds of energy calculated and updated in real time.

The controls at the top right corner can be used to pause/resume (first icon) or restart (second icon) the simulation. The third icon (hamburger style icon) will open a menu of options to handle the display of the toolboxes.

At the bottom one can see the status bar with information about the IPS (Iterations/s) and FPS (Frames/s) at the left and the simulation time in seconds at the right.

## How it works

Your program will be divided in two parts: Your **Simulation** and the **{ref}`Interface <Creating an Interface>`**. Consider the flowchart below.

[![](https://mermaid.ink/img/pako:eNqNk99rwjAQx_-VkKcJKvjrpQ-Dbb7sYeBQNjY7yrW5aiBNSkymTvzfl1qSVbHb7umu30_zvQu5A80UQxrRXKhttgZtyGIaS-JiY9OVhnJN9srqpNTKVcXyzRVkVhcfNXgGb3hhBRiuZI3OQ92gqyjBnYAGdTK4eQHNIRVIZp02aPgDPTcglOxKE1y6X3LIcPnoswv3gBqlRKp2CSwXdUbuL9Aqtpyt0LhOX08JGZMeUdaU1nRa4aGHRw7m8ld25Nlh28Fng16dIA0T3LVPMPZGg5am_vbJgs9Du8_E-0z-NVAoTknjafT65BOERfJF-r1bf1ux9Hcc9F1DnwR9HPR9Qx-06Y3nRru0QF0AZ245DlVzMTVrLDCmkUsZ5mCFiWksjw4Fa9R8LzMaGW2xS23JwOCUQ7UmNMpBbNxXZNwo_VQv3GnvurQE-a6UZ47fYdsWNA?type=png)](https://mermaid.live/edit#pako:eNqNk99rwjAQx_-VkKcJKvjrpQ-Dbb7sYeBQNjY7yrW5aiBNSkymTvzfl1qSVbHb7umu30_zvQu5A80UQxrRXKhttgZtyGIaS-JiY9OVhnJN9srqpNTKVcXyzRVkVhcfNXgGb3hhBRiuZI3OQ92gqyjBnYAGdTK4eQHNIRVIZp02aPgDPTcglOxKE1y6X3LIcPnoswv3gBqlRKp2CSwXdUbuL9Aqtpyt0LhOX08JGZMeUdaU1nRa4aGHRw7m8ld25Nlh28Fng16dIA0T3LVPMPZGg5am_vbJgs9Du8_E-0z-NVAoTknjafT65BOERfJF-r1bf1ux9Hcc9F1DnwR9HPR9Qx-06Y3nRru0QF0AZ245DlVzMTVrLDCmkUsZ5mCFiWksjw4Fa9R8LzMaGW2xS23JwOCUQ7UmNMpBbNxXZNwo_VQv3GnvurQE-a6UZ47fYdsWNA)

The **Simulation** might have many variables that are either parameters (fixed or not) and calculated values. Here we represent only two of those variables by _Variable P_ and _Variable Q_.

The **{ref}`Interface <Creating an Interface>`** can provide {ref}`Toolboxes <Creating a Toolbox>` which behave like small floating windows that can be populated with {ref}`Widgets <Creating a Widget>`.

Each {ref}`Widget <Creating a Widget>` can be either of type _input_ or _output_ such that the _input_ ones can have their values changed by the user during runtime both by graphical interaction or programatically. In other hand, _output_ {ref}`Widgets <Creating a Widget>` can only have their value altered programatically.

The value of any _input_ {ref}`Widget <Creating a Widget>` can be used to set any variable of the **Simulation** or any value of a _output_ {ref}`Widget <Creating a Widget>`. Also, any variable of the **Simulation** can set the value of any {ref}`Widget <Creating a Widget>` (_input_ or _output_)

The {ref}`Interface <Creating an Interface>` will also be responsible for initialize several aspects of _Pygame_, keep track and control the flow of the **Simulation** time. 
