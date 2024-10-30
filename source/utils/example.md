<WRAP type="template"/>
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
| `<INLUDE src="style/``example``.css"/>` | include contents of the file in the place of the tag |
| `<WRP type="`*`template`*`"/>` | wraps the contents of the file in `source/templates/`*`template`*`.html` |
| `<CONENT/>` | indicates where the wrapper should include the contents |
| `<MEA key="value" key1="value2"/>` | for content. save `value` in `key` for later access in wrapper |
| `<PAAM type="key"/>` | for wrapper. accessing `value` from content file |

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

### Running Example

To see Veles in action, follow these steps to build a simple example project:

#### 1. Build the Project

Run the following command in your terminal:

```bash
python build.py
```

#### 2. Project Structure

After running the build command, the following components will be generated:

- robots.txt: This file is located in the root/ folder and is copied to the build output.
- index.html: This file is generated in the build/ directory and includes content from `utils/``example``.md`.

#### 3. Template and Styling

- Template Usage: The build/index.html is created using the source/templates/template.html wrapper.
- Styling: The template utilizes the <INCLUDE> tag to insert styles from `styles/``example``.css`, ensuring the final HTML file is properly styled.

#### 4. Output

After the build process, your build/ directory will contain:

- index.html
- robots.txt

You can open build/index.html in your browser to view the result!

### Starting new project

If you want to start a scratch project, you can delete the following files:

- Any existing files in the root/ folder (except robots.txt if you want to keep it).
- All files in the utils/ folder.
- Any templates in the templates/ folder you don’t need.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements or bugs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.