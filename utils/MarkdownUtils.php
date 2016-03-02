<?php
/*
    File:   utils/MarkdownUtils.php
    Author: Chris McKinney
    Edited: Mar 01 2016
    Editor: Chris McKinney

    Description:

    Utilities for working with Markdown and template files.

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

// Include PHP Markdown Extra
$installPath = realpath(__DIR__ . '/..');
include_once "$installPath/php-markdown/Michelf/MarkdownExtra.inc.php";
use \Michelf\MarkdownExtra;

// Process some text as Markdown.
function mdText($text) {
    return MarkdownExtra::defaultTransform($text);
}

// Process a file as Markdown.
function md($filename) {
    return mdText(file_get_contents($filename));
}

// Get a common override file path
function pathCommon($filename) {
    $sitePath = realpath(__DIR__ . '/../..');
    $installPath = realpath(__DIR__ . '/..');
    if (file_exists($filename)) {
        return $filename;
    } else if (file_exists("$sitePath/common/$filename")) {
        return "$sitePath/common/$filename";
    } else {
        return "$installPath/common/$filename";
    }
}

// Process a common override file as Markdown, with fallback.
function mdCommon($filename) {
    return md(pathCommon($filename));
}

// Process a file as a Markdown SimpleTemplate.
function mdTpl($filename) {
    $installPath = realpath(__DIR__ . '/..');
    $arg1 = escapeshellarg("$installPath/utils/template.py");
    $arg2 = escapeshellarg(json_encode($_GET));
    $arg3 = escapeshellarg("$filename.template");
    echo "<!-- python $arg1 $arg2 $arg3 -->";
    return mdText(shell_exec("python $arg1 $arg2 $arg3"));
}

// Process a common override file as a Markdown SimpleTemplate, with
// fallback.
function mdTplCommon($filename) {
    if (file_exists("$filename.template")) {
        return mdTpl($filename);
    } else {
        return mdCommon($filename);
    }
}
?>
