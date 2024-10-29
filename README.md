# Name of the project

add folders and 

| config.json | explanation |
| ----------- | ----------- |
| "blog/example.html": "public/blog.html" | copy `source/public/blog.html` to `build/blog/example/html` |
| "blogs/": "blog_files/" | copy html, md, and files referenced from `source/blog_files/` to `build/blogs/` |
| "/": "root/*" | copy all contents from `source/root/` to `build/` |
| "example/buss-website/": "https://github.com/daniilgrydin/buss-website.git" | pull buss-website repository from github to `example/buss-website/` |