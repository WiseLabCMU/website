---
title: Home
---

<div class="container">
    <div class="row  mb-4">
        <div class="col">
            <p>
                Wireless Sensing and Embedded Systems Lab is a systems research group in the Electrical and Computer
                Engineering Department at Carnegie Mellon University that focuses on the platforms, protocols and
                processing techniques that support networked embedded systems. We are interested in a broad range of
                topics including: operating system design, wireless networking, sensing technologies, real-time
                scheduling, time synchronization and localization. We apply our work to applications such as building
                energy management, micro-grid management, critical infrastructure monitoring, large-scale environmental
                sensing and mobile computing.
            </p>
        </div>
    </div>
    <div class="row mb-5">
    <a name="projects"></a>
    {% assign projects = site.projects | sort: 'priority' %}
    {% for project in projects %}
        <div class="col-md-4">
            <div class="project-item boxed">
                <a href="{{ base.url }}{{ project.url }}">
                    <img alt="{{ project.title }} image" src="{{ project.image }}"/>
                    <div class="project-title">
                        {{ project.title }}
                    </div>
                </a>
            </div>
        </div>
    {% endfor %}
    </div>
    <div class="row">
        <div class="col" markdown="1" id="news-container">{% include news.md %}
</div>
    </div>
</div>
