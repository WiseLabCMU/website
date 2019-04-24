# website
Static Bootstrap 4 site generated by Jekyll

## Local Development
[Install Jekyll](https://jekyllrb.com/docs/installation/) and preview changes
with `jekyll serve` at http://localhost:4000

## Making Updates
Modify content pages and push commit. Changes to `master` branch will automatically
be deployed to the live server (in about 60s) unless a `skip` keyword is included in
commit message, e.g. 

```
Update README

[skip ci] 
```

### Projects
Add projects to the `_projects` directory.

Specify the following metatags in header:
* `layout: project`
* `title:` [title]
* `image:` "/img/projects/[filename]"
* `priority:` [int]

The body is markdown-enabled description of the project.  
Images should be 3:2 ratio, ideally 510px * 340px.

### Team Members
Add team members to the `_team` directory.

Specify the following metatags in header:
* `firstname:` [firstname]
* `lastname:` [lastname]
* `priority:` [int]
* `title:` [title]
* `affiliation:` [department/school]
* `website:` [url]
* `image:` "/img/team/[filename]"

Images should be square, ideally 450px * 450px.  
Team member display is sorted first by priority, then by last name.
