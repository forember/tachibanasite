<?php
/* vim: set filetype=css : */
header('Content-Type: text/css');
?>
/*
    File:   theme/support.css.php
    Author: Chris McKinney
    Edited: Mar 01 2016
    Editor: Chris McKinney

    Description:

    Support for theme for webpages. PHP for color arguments.

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
function define_var(&$var, $name, $default) {
    if (array_key_exists($name, $_GET)) {
        $var = $_GET[$name];
    } else {
        $var = $default;
    }
}

define_var($bodyBColor, 'bbc', '#808080');
define_var($containerBColor, 'cbc', '#fff');
define_var($headerBColor, 'hbc', '#000');
define_var($headerFColor, 'hfc', '#fff');
define_var($navfillBColor, 'nbc', '#282828');

$installPath = realpath(__DIR__ . '/..');
include_once "$installPath/utils/ConfigIniUtils.php";
$installURL = get_config_option('install_url');
?>*/

body {
    background-color: <?=$bodyBColor?>;
    background-image: url(<?=$installURL?>/theme/images/body_grad.png);
    background-repeat: repeat-x;
    font-family: sans-serif;
    font-size: 12pt;
}

#container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background-color: <?=$containerBColor?>;
    margin: 24px 24px 0 24px;
}

#middleContainer {
    margin: 0;
    padding: 0;
    overflow: hidden;
}

#pageHeader, div.sideHeader, #footer {
    background-color: <?=$headerBColor?>;
    background-image: url(<?=$installURL?>/theme/images/header_top_grad.png);
    background-size: auto 40pt;
    background-repeat: repeat-x;
    color: <?=$headerFColor?>;
}

#pageHeader {
    padding: 1pt 1em;
}
/* Allows the page header to be selected. */
#pageHeader h1 {
    z-index: 100;
}

#content {
    margin: 0 1em 0 128pt;
}
#content p {
    margin: 0;
    padding: 1ex 0;
}
#content li p:first-child {
    padding-top: 0;
}
#content li p:last-child {
    padding-bottom: 0;
}

#content pre {
    font-size: 12pt;
}

.sideHeader {
    font-variant: small-caps;
    padding: 4pt;
    margin: 0;
    text-decoration: underline;
}
div.sideHeader {
    transform: scaleY(-1);
}
div.sideHeader * {
    transform: scaleY(-1);
}

#navcontainer {
    float: left;
    width: 120pt;
    margin-right: 8pt;
    background-color: <?=$headerBColor?>;
    color: <?=headerFColor?>;
}

#navcontainer ul, #sidebarContainer ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
#navcontainer li, #sidebarContainer li {
    display: block;
    margin: 0;
    padding: 0;
}
#navcontainer li a, #sidebarContainer li a {
    color: <?=$headerFColor?>;
    text-decoration: none;
    display: block;
    padding: 1ex;
    text-align: right;
}
#navcontainer li a:link:not(#current), #sidebarContainer li a:link {
    background-color: <?=$bodyBColor?>;
}
#current {
    background-color: <?=$headerBColor?>;
    font-weight: bold;
}
#navcontainer li a:hover {
    background-color: <?=$headerBColor?>;
}
#sidebarContainer li a:hover {
    background-color: <?=$navfillBColor?>;
}

#navfill {
    background-color: <?=$navfillBColor?>;
}

.clearer {
    clear: both;
}

#footer {
    margin: 0;
    padding: 1pt 1em;
    font-size: 9pt;
}
