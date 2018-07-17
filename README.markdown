Server software for <https://tachibanatech.com/> and <http://afrl.cse.sc.edu/>.

Documentation at <https://tachibanatech.com/ts/>.

# Install via AutoTS

**WARNING:** AutoTS is still *very* alpha. For a traditional install, see
<https://tachibanatech.com/ts/install/>.

Go into the directory where you want your site, and run:

```bash
curl -O https://raw.githubusercontent.com/NighttimeDriver50000/tachibanasite/master/_install_ts.sh
sh _install_ts.sh
```

Then follow the on-screen instructions.

# TODO

-   Redo theme CSS
-   Update documentation
-   Improve AutoTS
-   Finally doing caching
-   Upgrade to Python 3

# Version History

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

![Pre-1.8.8 version history](oldchanges.markdown)
