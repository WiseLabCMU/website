---
layout: project
title:  "Distributed Runtime for WebAssembly (Silverline)"
image: "/img/projects/silverline.png"
priority: 1
---

A paradigm shift in how we design distributed computing systems is almost inevitable. With advanced compute,
networking, sensing, and actuation, Edge devices are increasingly capable. At the same time, there is a desire
to expand some of the cloud infrastructure to the edge.

Figure 1 depicts the framework's scope: it spans off-perm cloud to an on-perm edge that includes server-class
devices as well as devices with more reduced compute capabilities (edge and micro-edge devices). Silverline
leverages a common execution runtime that supports isolation and resource monitoring across compute classes -
from small embedded devices to edge servers - to manage workloads spanning the cloud and edge. It is distinct
from several previous frameworks for managing distributed computing by focusing on adaptation to changing resources
and support for highly heterogeneous distributed systems found at the edge.
