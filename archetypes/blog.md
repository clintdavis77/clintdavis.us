---
title: "{{ replace .File.ContentBaseName "-" " " | strings.Title }}"
description: ""
date: {{ .Date }}
draft: true
tags: []
# youtube: ""            # video ID only, e.g. dQw4w9WgXcQ — renders an embed under the title
# image: /images/x.png   # optional social card override (1200x630)
# kicker: ""             # optional label above the title, defaults to "Writing"
---

Opening paragraph. This is the text that appears in the blog list teaser only if
`description:` above is filled in — the list shows the description, not this.
