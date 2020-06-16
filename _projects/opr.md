---
layout: project
title:  "Opportunistic Packet Recovery in LoRa Wireless Networks"
image: "/img/projects/opr.png"
priority: 2
---
Conventional wireless communication systems are typically de-signed assuming a single transmitter-receiver pair for each link.In Low-Power Wide-Area Networks (LP-WANs), this one-to-onedesign paradigm is often overly pessimistic in terms of link budget because client packets are frequently detected by multiple gateways(i.e. one-to-many). In this project, we explore the potential of using multiple receivers at the MAC and link layer where these performance gains are often neglected. We present an approach called Opportunistic Packet Recovery (OPR) that targets the most likely corrupt bits across a setof packets that suffered failed CRCs at multiple LoRa LP-WAN base-stations.  We see that bit errors are often disjoint across receivers, which aids in collaborative error detection. OPR leverages this to provide increasing gain in error recovery as a function of the number of receiving gateways. Since LP-WAN networks can easily offload packet processing to the cloud, there is ample computetime per packet (order of seconds) to search for bit permutations that would restore packet integrity. Link layer corrections have the advantage of being immediately applicable to the millions of already deployed LP-WAN systems without additional hardware orexpensive RF front-ends. 

[MobiSys 2020](http://users.ece.cmu.edu/~agr/resources/publications/mobisys_20_opr.pdf)  
