<?php
/*
    File:   utils/NavFilter.php
    Author: Chris McKinney
    Edited: Mar 01 2016
    Editor: Chris McKinney

    Description:

    Filter for the nav list. Also a utility for loading the page title.

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

// Import Markdown Utilities.
include_once "MarkdownUtils.php";

// Get the regex pattern for the <a> in the navlist for the current page.
/*
 *  Group 0 is the whole <a>...</a> element.
 *  Group 1 is "<a" and all the attributes.
 *  Group 2 is >..</a> (everything after group 1).
 *  Group 3 is the content between the tags.
 *  The pattern includes the opening and closing "/".
 */
function navlistAnchorPattern() {
    $hrefPtn = str_replace('/', '\\/', preg_quote(dirname($_SERVER['PHP_SELF'])));
    return '/(<a href="' . $hrefPtn . '\/?")(>(.*)<\/a>)/i';
}

// Load the navbar from the provided common override template.
function loadNav($navlistName) {
    $mdHtml = mdTplCommon($navlistName);
    return preg_replace(navlistAnchorPattern(), '$1 id="current"$2',
        $mdHtml);
}

// Load the title for the current page.
function loadTitle($navlistName, $siteTitle) {
    $mdHtml = mdTplCommon($navlistName);
    preg_match(navlistAnchorPattern(), $mdHtml, $matches);
    if ($matches[3]) {
        $title = $matches[3];
    } else if (file_exists('title.text')) {
        $title = file_get_contents('title.text');
    } else {
        return $siteTitle;
    }
    if ($siteTitle) {
        $title .= ' | ' . $siteTitle;
    }
    return $title;
}
?>
