<?php
/* vim: set filetype=css : */
header('Content-Type: text/css');
?>
/*
    File:   ./common/themes/coloredpencil/support.css.php
    Author: Chris McKinney
    Edited: Jul 14 2017
    Editor: Chris McKinney

    Description:

    Support for theme for webpages. PHP for color arguments.

    Edit History:

    1.7.14  - Created.

    License:

    Copyright 2016 Chris McKinney

    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License.  You may obtain a copy
    of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
 */
/*<?php
$bg = '#eee';
$text = '#111';
$link = '#33c';
$head = '#555';
?>*/

@import url('https://fonts.googleapis.com/css?family=Slabo+13px');
@import url('https://fonts.googleapis.com/css?family=Slabo+27px');

body {
    color: <?=$text?>;
    background-color: <?=$bg?>;
    font-family: 'Slabo 13px', serif;
}
h1, h2, h3, h4, h5, h6 {
    color: <?=$head?>;
    font-family: 'Slabo 27px', serif;
}
#container {
    position: relative;
    top: 50px;
}
div.sideHeader {
    border-top: solid black 2pt;
    padding: 5px;
}
#footer {
    padding-top: 5px;
    padding-bottom: 0px;
    padding-left: 10px;
    padding-right: 10px;
    font-size: 85%;
}
#navcontent {
    border-right: solid black 2pt;
}
#navcontent ul {
    list-style: none;
    padding: 5px;
    text-align: right;
}
#navcontent a {
    color: black;
}
#navcontent a:hover {
    color: black;
    background-color: inherit;
    font-weight: bold;
}
#current {
    font-weight: bold;
}
footer.well {
    background-image: linear-gradient(to bottom,
        rgba(0, 0, 0, <?=1 - 0xe8/255.0?>) 0px,
        rgba(0, 0, 0, <?=1 - 0xf5/255.0?>) 100%);
}

/* Link behavior. */
a, a:link {
    color: <?=$link?>;
    text-decoration: none;
}
a:hover {
    color: <?=$link?>;
    background-color: rgba(0, 0, 0, 0);
    text-decoration: underline;
}

/* Markdown text. */
.markdown-content p, .markdown-content li, .markdown-content blockquote,
.markdown-content code, .markdown-content pre {
    color: <?=$text?>;
}
