<?php
/*
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

// Include utilities
include_once "ConfigIniUtils.php";

// Force the page to use SSL.
function forceSSL($use_sts = true) {
    // Use HTTP Strict Transport Security to force client to use secure
    // connections only

    // iis sets HTTPS to 'off' for non-SSL requests
    if ($use_sts && isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off') {
        header('Strict-Transport-Security: max-age=31536000');
    } elseif (!isset($_SERVER['HTTPS']) || $_SERVER['HTTPS'] == ''
            || $_SERVER['HTTPS'] == 'off') {
        header('Location: https://' . $_SERVER['HTTP_HOST']
            . $_SERVER['REQUEST_URI'], true, 301);
        // we are in cleartext at the moment, prevent further execution/output
        die();
    }
}

// Force the page to use SSL if mandated by the config.
function maybeSSL() {
    if (get_config_option('force_ssl') == '1') {
        forceSSL();
    }
}
?>
