<?php
/*
    File:   utils/LoadsJavascript.php
    Author: Chris McKinney
    Edited: May 21 2016
    Editor: Chris McKinney

    Description:

    Utilities to load javascript for the whole site.

    Edit History:

    0.5.21  - Created to handle new spread-out js.

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

function get_js_url_array() {
    $installURL = get_config_option('install_url');
    $urls = array(
        200 => "$installURL/utils/utils.js",
        800 => get_theme_url('theme.js')
    );
    return $urls;
}

function echo_script_tags() {
    foreach (get_js_url_array() as $i => $url) {
        echo "<script type='text/javascript' src='$url'></script>\n";
    }
}

?>
