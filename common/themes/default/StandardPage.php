<?php
/*
    File:   common/themes/default/StandardPage.php
    Author: Chris McKinney
    Edited: Aug 10 2016
    Editor: Chris McKinney

    Description:

    The default standard page for a TachibanaSite webpage.

    Edit History:

    0.4.6   - Added jQuery support.
            - Added version.

    0.5.21  - Moved theme presets into theme (support.css.php).
            - Added theme URL to config file.
            - Moved standard page into theme and separated head and body.

    0.6.22  - Added favicon.

    0.8.10  - Moved some features into modules.

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

$installPath = realpath(__DIR__ . '/../../..');
// Change to the directory of the current page.
chdir(dirname($_SERVER['SCRIPT_FILENAME']));
// Import utilities.
include_once "$installPath/utils/ForceSSL.php";
maybeSSL();
include_once "$installPath/utils/MarkdownUtils.php";
include_once "$installPath/utils/NavFilter.php";
include_once "$installPath/utils/ConfigIniUtils.php";
include_once "$installPath/utils/Theme.php";
include_once "$installPath/utils/LoadJavascript.php";
$installURL = get_config_option('install_url');
$theme = load_theme_config();
?>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title><?=loadTitle('navlist.markdown',
                get_config_option('site_title'))?></title>
        <?php echo_link_tags() ?>
        <link rel="stylesheet" type="text/css"
                href="<?=theme_support_url($theme)?>" />
        <link rel="icon" type="image/png"
                href="<?=urlCommon('favicon.png')?>" />
        <?php echo_script_tags() ?>
        <script type="text/javascript">
            window.onresize = windowResizeAction;
            window.onload = windowLoadAction;
        </script>
    </head>
    <body>
        <?php
            $bodyPage = get_theme_path_wfallback('StandardPageBody.php');
            include "$bodyPage";
        ?>
    </body>
</html>