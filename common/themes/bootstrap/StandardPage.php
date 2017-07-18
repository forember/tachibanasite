<?php
/*
    File:   common/themes/bootstrap/StandardPage.php
    Author: Chris McKinney
    Edited: Jul 14 2017
    Editor: Chris McKinney

    Description:

    The default standard page for a TachibanaSite webpage.

    Edit History:

    1.7.14  - Copied from default and added meta tags.

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

// Get path to tachibanasite directory.
$installPath = realpath(__DIR__ . '/../../..');
// Change to the directory of the current page.
chdir(dirname($_SERVER['SCRIPT_FILENAME']));
// Import utilities.
include_once "$installPath/utils/ForceSSL.php";
maybeSSL(); // Force SSL if option set.
include_once "$installPath/utils/MarkdownUtils.php";
include_once "$installPath/utils/NavFilter.php";
include_once "$installPath/utils/ConfigIniUtils.php";
include_once "$installPath/utils/Theme.php";
include_once "$installPath/utils/LoadJavascript.php";
// Load useful values.
$installURL = get_config_option('install_url');
$theme = load_theme_config();
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title><?=loadTitle('navlist.markdown',
                get_config_option('site_title'))/*Generate title*/?></title>
        <?php echo_link_tags()/*Load CSS*/?>
        <link rel="stylesheet" type="text/css"
                href="<?=theme_support_url($theme)/*Load support.css.php*/?>"/>
        <link rel="icon" type="image/png"
                href="<?=urlCommon('favicon.png')/*Load favicon*/?>" />
        <?php echo_script_tags()/*Load Javascript*/?>
        <script type="text/javascript">
            // Set window actions to allow for registration.
            window.onresize = windowResizeAction;
            window.onload = windowLoadAction;
        </script>
    </head>
    <body>
        <?php
            // Load the body of the standard page.
            $bodyPage = get_theme_path_wfallback('StandardPageBody.php');
            include "$bodyPage";
        ?>
    </body>
</html>
