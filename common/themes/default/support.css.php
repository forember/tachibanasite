<?php
/* vim: set filetype=css : */
header('Content-Type: text/css');
?>
/*
    File:   common/themes/default/support.css.php
    Author: Chris McKinney
    Edited: May 21 2016
    Editor: Chris McKinney

    Description:

    Support for theme for webpages. PHP for color arguments.

    Edit History:

    0.5.21  - Moved theme presets here from the standard page.
            - Made image URLs relative.

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
// Color presets.
$presets = array(
    'default' => array(
        'bbc' => '#808080',
        'cbc' => '#fff',
        'hbc' => '#000',
        'hfc' => '#fff',
        'nbc' => '#282828'
    ),
    'red' => array(
        'bbc' => '#866',
        'cbc' => '#fff',
        'hbc' => '#211',
        'hfc' => '#dff',
        'nbc' => '#453636'
    ),
    'green' => array(
        'bbc' => '#464',
        'cbc' => '#fff',
        'hbc' => '#121',
        'hfc' => '#ffd',
        'nbc' => '#364536'
    ),
    'teal' => array(
        'bbc' => '#446660',
        'cbc' => '#fff',
        'hbc' => '#122',
        'hfc' => '#ffd',
        'nbc' => '#364545'
    ),
    'blue' => array(
        'bbc' => '#668',
        'cbc' => '#fff',
        'hbc' => '#112',
        'hfc' => '#ffd',
        'nbc' => '#363645'
    ),
    'purple' => array(
        'bbc' => '#546',
        'cbc' => '#fff',
        'hbc' => '#212',
        'hfc' => '#ffd',
        'nbc' => '#453645'
    )
);

// Determine the preset to use.
if (array_key_exists('preset', $_GET)
        && array_key_exists($_GET['preset'], $presets)) {
    // A preset was specified in the URL.
    $presetName = $_GET['preset'];
    // Gets echoed into CSS comment.
    echo "Loaded $presetName preset.\n";
} else {
    // No preset was specified in the URL.
    $presetName = 'default';
    echo "Falling back to $presetName preset.\n";
}

function define_var(&$var, $name) {
    // Overwrite var if custom provided in URL.
    global $presets, $presetName;
    if (array_key_exists($name, $_GET)) {
        $var = $_GET[$name];
        echo "Custom var $name = $var\n";
    } else {
        $var = $presets[$presetName][$name];
        echo "Preset var $name = $var\n";
    }
}

// Load variables.
define_var($bodyBColor, 'bbc');
define_var($containerBColor, 'cbc');
define_var($headerBColor, 'hbc');
define_var($headerFColor, 'hfc');
define_var($navfillBColor, 'nbc');
?>*/

body {
    background-color: <?=$bodyBColor?>;
    background-image: url(images/body_grad.png);
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

#pageHeader, div.sideHeader:first-of-type, #footer {
    background-color: <?=$headerBColor?>;
    background-image: url(images/header_top_grad.png);
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
    color: <?=$headerFColor?>;
}
div.sideHeader {
    background-color: <?=$navfillBColor?>;
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
#navcontainer li a:hover:not(#current) {
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
