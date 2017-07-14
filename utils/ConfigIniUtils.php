<?php
/*
    File:   utils/ConfigIniUtils.php
    Author: Chris McKinney
    Edited: Jul 14 2017
    Editor: Chris McKinney

    Description:

    Utilities for working with the config.ini files.

    Edit History:

    0.5.21  - Added section parsing.

    1.7.14  - Fixed bug when key not found in section when file exists.

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

// Read an option from a file.
function get_config_file_option($filename, $key, $section = false) {
    if (file_exists($filename)
            && ($config = parse_ini_file($filename, !!$section))) {
        if ($section) {
            if (array_key_exists($section, $config)
                    && array_key_exists($key, $config[$section])) {
                return $config[$section][$key];
            } else {
                return false;
            }
        } else {
            if (array_key_exists($key, $config)) {
                return $config[$key];
            } else {
                return false;
            }
        }
    } else {
        return false;
    }
}

// Read an option from the usual files.
function get_config_option($key, $section = false) {
    $sitePath = realpath(__DIR__ . '/../..');
    $installPath = realpath(__DIR__ . '/..');
    if (false !== ($val = get_config_file_option('config.ini', $key,
            $section))) {
        return $val;
    } else if (false !== ($val = get_config_file_option(
            "$sitePath/common/config.ini", $key, $section))) {
        return $val;
    } else if (false !== ($val = get_config_file_option(
            "$installPath/common/config.ini", $key, $section))) {
        return $val;
    } else {
        return false;
    }
}
?>
