---
layout: project
title:  "Acoustic Room Geometry Reconstruction"
image: "/img/projects/synesthesia.jpg"
priority: 3
---
Understanding the location of acoustically reflective surfaces in a room is a critical
component in advanced sound processing.  For example, intelligent speakers can use a room's
acoustic geometry to improve playback quality, source separation accuracy, and speech recognition.
In this paper, we present Synesthesia, a system for capturing the acoustic properties of a room
using a single fixed speaker and a mobile phone that records audio at multiple locations.
Using the arrival time of echoes, the system is able to reconstruct the position of reflective surfaces
like walls and then estimate properties like surface absorption.

In this project, we introduce a new approach that performs RIR imaging using a mobile phone that tracks its
location with visual inertial odometry (VIO) to record a dense set of samples albeit with noise in their
locations. We present a new approach that is able to relax several key assumptions on RIR and show through
both experimentation and simulation that even with 20cm of uncertainty in the microphone locations provided by
VIO, we are still able to reconstruct the room geometry with accurate shape and dimensions.  We demonstrate
this capability by prototyping a tool for acoustic engineers, that allows a user to view a room's estimated
geometry and absorption overlaid on the actual sensed space with augmented reality.
