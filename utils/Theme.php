<?php
/*
    File:   utils/Theme.php
    Author: Chris McKinney
    Edited: Mar 01 2016
    Editor: Chris McKinney

    Description:

    Utility for getting colored theme URLs.

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

// Get a URL for the given color theme.
function theme_url($theme) {
    $installPath = realpath(__DIR__ . '/..');
    include_once "$installPath/utils/ConfigIniUtils.php";
    $installURL = get_config_option('install_url');
    $url = "$installURL/theme/support.css.php?";
    $first = True;
    foreach ($theme as $name => $value) {
        if ($first) {
            $first = False;
        } else {
            $url .= '&';
        }
        $url .= urlencode($name);
        $url .= '=';
        $url .= urlencode($value);
    }
    return $url;
}

?>
