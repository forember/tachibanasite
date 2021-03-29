Server software for <https://tachibanatech.com/> and <https://afrl.cse.sc.edu/>.

Documentation at <https://ttech.click/old-ts-docs/>.

# Install via AutoTS

**WARNING:** AutoTS is still *very* alpha. For a traditional install, see
<https://ttech.click/old-ts-docs/install>.

Go into the directory where you want your site, and run:

```bash
curl -O https://raw.githubusercontent.com/forember/tachibanasite/master/_install_ts.sh
sh _install_ts.sh
```

Then follow the on-screen instructions.

# TODO for 2.0

-   Implement in pure Python 3 with [CGI][]
-   Switch from Bottle SimpleTemplate to Jinja 2
-   Redo theme CSS with templating
-   Improved and graphical AutoTS
-   Update documentation
    -   Document modules
    -   Provide examples
    -   Document themes
-   Theme preview
-   Embedded python on all eligible files
-   Smarter default navlist and breadcrumb
-   Syntax extension modules (e.g. KaTeX &dollar;)
-   Move from INI to TOML
-   Recursive config loading
-   Finally doing caching

[CGI]: https://help.dreamhost.com/hc/en-us/articles/217297307-CGI-overview

# Version History

## 1.10.1

-   Compatibility in some instances with [tachi][]'s `_FORM` global.

[tachi]: https://github.com/forember/tachi

## 1.10.0

**The only site that will actually be maintained with TachibanaSite is
[afrl.cse.sc.edu](https://afrl.cse.sc.edu/). TachibanaTech is going to be split
into multiple smaller sites, and will use a different framework. As such,
these 1.10.x versions will be maintenance releases specifically to support the
currently-installed AFRL pages.**

-   Disabled all contact forms.

## 1.9.1

-   Removed those silly file headers
-   Updated Bootstrap to 4.1.2 from 4.0.0-beta2
-   Pulled php-markdown submodule

## 1.9.0

**WARNING:** The 1.9.x versions are going to be a run-up to a 2.0 release. They
are going to change a lot of things, so unless you want to come on this ride
with me, stick with 1.8.8 for now.

-   Default theme is now Colored Pencil
-   Templates enabled by default
-   Bootstrap 4 and full highlight.js now enabled by default
-   Removed `theme.js` support from themes (may be re-added in the future)
-   Removed the following themes: bootstrap, default, and paper
-   Removed the Bootstrap 3 and Bootstrapify modules
-   `markdown_content.css` and `support.css.php` now fall back to coloredpencil

## 1.8.8

-   Fixed SSL Forcing
-   Updated KaTeX and highlight.js
-   Added a (default disabled) module with all the highlight.js languages

[Pre-1.8.8 version history](oldchanges.markdown)
