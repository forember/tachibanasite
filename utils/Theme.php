<?php
/*
    File:   ./utils/Theme.php
    Author: Chris McKinney
    Edited: May 21 2016
    Editor: Chris McKinney

    Description:

    Utility for getting colored theme URLs.

    Edit History:

    0.5.21  - Added theme URL to config file.
            - Added utilities for locating the theme.
            - Added utilities for loading theme options.

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
include_once 'MarkdownUtils.php';

// Get the active theme name.
function get_theme_name() {
    return get_config_option('theme_name');
}

// Get a file path in the active theme.
function get_theme_path($name) {
    $themeName = get_config_option('theme_name');
    return pathCommon("themes/$themeName/$name");
}

// Get a file path in the active theme, loading from default if not found.
function get_theme_path_wfallback($name, $defaultThemeName = 'default') {
    $path = get_theme_path($name);
    if (!file_exists($path)) {
        $path = pathCommon("themes/$defaultThemeName/$name");
    }
    return $path;
}

// Get a URL in the active theme.
function get_theme_url($name) {
    $themeName = get_config_option('theme_name');
    return urlCommon("themes/$themeName/$name");
}

// Get a URL for the given color theme.
function theme_support_url($theme) {
    $url = get_theme_url('support.css.php') . '?';
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

function update_theme_from_config(&$themeConfig, $configFile) {
    if (file_exists($configFile)
            && ($config = parse_ini_file($configFile, true))
            && (array_key_exists('Theme', $config))) {
        $srcTheme = $config['Theme'];
        foreach ($srcTheme as $key => $value) {
            $themeConfig[$key] = $value;
        }
    }
}

// Load the theme from the config.
function load_theme_config() {
    $themeConfig = array();
    $defaultPath = realpath(__DIR__ . '/..');
    $defaultFile = "$defaultPath/common/config.ini";
    $sitePath = realpath(__DIR__ . '/../..');
    $siteFile = "$sitePath/common/config.ini";
    $localFile = 'config.ini';
    update_theme_from_config($themeConfig, $defaultFile);
    update_theme_from_config($themeConfig, $siteFile);
    update_theme_from_config($themeConfig, $localFile);
    return $themeConfig;
}

?>
