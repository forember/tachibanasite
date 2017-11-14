<?php
/*
    File:   ./utils/LoadJavascript.php
    Author: Chris McKinney
    Edited: Jul 14 2017
    Editor: Chris McKinney

    Description:

    Utilities to load javascript and CSS for the whole site.

    Edit History:

    0.5.21  - Created to handle new spread-out js.

    0.8.10  - Added module support.
            - Added CSS loading.

    1.7.14  - Added the ability to disable modules.

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

include_once 'ConfigIniUtils.php';

function get_url_array($iniPrefix, $urls) {
    $installURL = get_config_option('install_url');
    $installPath = realpath(__DIR__ . '/..');
    $moduleDirs = scandir("$installPath/modules");
    foreach ($moduleDirs as $mname) {
        if (get_config_option("${mname}_disabled", 'Modules')) {
            continue;
        }
        if ($mname != '.' && $mname != '..') {
            $mdir = "$installPath/modules/$mname";
            $mini = "$mdir/module.ini";
            $priority = get_config_file_option($mini, $iniPrefix . '_priority');
            if ($priority !== false) {
                $file = get_config_file_option($mini, $iniPrefix . '_file');
                if ($file) {
                    $url = "$installURL/modules/$mname/$file";
                } else {
                    $url = get_config_file_option($mini, $iniPrefix . '_url');
                }
                $urls[$priority] = $url;
            }
        }
    }
    ksort($urls);
    return $urls;
}

function get_js_url_array() {
    $installURL = get_config_option('install_url');
    $urls = array(
        100 => 'https://code.jquery.com/jquery-1.12.0.min.js',
        200 => "$installURL/utils/utils.js",
        800 => get_theme_url('theme.js')
    );
    return get_url_array('js', $urls);
}

function echo_script_tags() {
    foreach (get_js_url_array() as $i => $url) {
        echo "<script type='text/javascript' src='$url'></script>\n";
    }
}

function get_css_url_array() {
    $urls = array(
        400 => get_theme_url('markdown-content.css'),
    );
    return get_url_array('css', $urls);
}

function echo_link_tags() {
    foreach (get_css_url_array() as $i => $url) {
        echo "<link rel='stylesheet' type='text/css' href='$url' />\n";
    }
}

?>
