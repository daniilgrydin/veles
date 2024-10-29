# Veles

Veles is a Python-based tool designed to introduce custom syntax to Markdown (MD) and HTML, simplifying the production process. With Veles, you can easily manage file inclusion, templating, and content organization using a straightforward configuration system.

## Features

- **Custom Syntax**: Utilize tags to include files, wrap content, and manage metadata.
- **Flexible Configuration**: Define how files and folders are included in the build using `config.json`.
- **Folder Organization**: Maintain a clear structure for your source files, templates, and styles.

## Getting Started

### Installation

To get started with Veles, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/veles.git
cd veles
pip install -r requirements.txt
```

### Configuration

Edit the config.json file to specify how files and folders should be included in the build:
```json
{
    "blog/example.html": "public/blog.html",
    "blogs/": "blog_files/",
    "/": "root/*",
    "buss-website/": "https://github.com/daniilgrydin/buss-website.git"
}
```


| config.json | Explanation |
| ----------- | ----------- |
| `"blog/example.html": "public/blog.html"` | copy `source/public/blog.html` to `build/blog/example/html` |
| `"blogs/": "blog_files/"` | copy html, md, and files referenced from `source/blog_files/` to `build/blogs/` |
| `"/": "root/*"` | copy all contents from `source/root/` to `build/` |
| `"buss-website/": "https://github.com/daniilgrydin/buss-website.git"` | pull buss-website repository from github to `build/buss-website/` |

> Please note that you can use both HTML and Markdown (MD) files. However, if you choose to use Markdown, you must specify the wrapper file.

### Custom Tags

To perform actions within your files, use the following custom tags:

| Tag | Action |
| --- | ------ |
| `<INCLUDE src="styles/example.css"/>` | include contents of the file in the place of the tag |
| `<WRAP type="template"/>` | wraps the contents of the file in `source/templates/`*`template`*`.html` |
| `<CONTENT/>` | indicates where the wrapper should include the contents |
| `<META key="value" key1="value2"/>` | for content. save `value` in `key` for later access in wrapper |
| `<PARAM type="key"/>` | for wrapper. accessing `value` from content file |

### Source Folders

Maintain an organized structure for your source files with the following folders:

| Folder | Purpose |
| ------ | ------- |
| `root/` | all contents are directly copied to the root of the build |
| `templates/` | templates/wrappers storage |
| `styles/` | general css storage |
| `utils/` | reusable elements of the application |

## Usage

To build your project, run the following command:

```bash
python build.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements or bugs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.