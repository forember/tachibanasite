<?php
/*
    File:   common/StandardPage.php
    Author: Chris McKinney
    Edited: Mar 01 2016
    Editor: Chris McKinney

    Description:

    The default standard page for a TachibanaSite webpage.

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

$installPath = realpath(__DIR__ . '/..');
// Change to the directory of the current page.
chdir(dirname($_SERVER['SCRIPT_FILENAME']));
// Import utilities.
include_once "$installPath/utils/ForceSSL.php";
maybeSSL();
include_once "$installPath/utils/MarkdownUtils.php";
include_once "$installPath/utils/NavFilter.php";
include_once "$installPath/utils/Theme.php";
include_once "$installPath/utils/ConfigIniUtils.php";
$installURL = get_config_option('install_url');
$redTheme = array(
    'bbc' => '#866',
    'cbc' => '#fff',
    'hbc' => '#211',
    'hfc' => '#dff',
    'nbc' => '#453636'
);
$greenTheme = array(
    'bbc' => '#464',
    'cbc' => '#fff',
    'hbc' => '#121',
    'hfc' => '#ffd',
    'nbc' => '#364536'
);
$tealTheme = array(
    'bbc' => '#446660',
    'cbc' => '#fff',
    'hbc' => '#122',
    'hfc' => '#ffd',
    'nbc' => '#364545'
);
$blueTheme = array(
    'bbc' => '#668',
    'cbc' => '#fff',
    'hbc' => '#112',
    'hfc' => '#ffd',
    'nbc' => '#363645'
);
$purpleTheme = array(
    'bbc' => '#546',
    'cbc' => '#fff',
    'hbc' => '#212',
    'hfc' => '#ffd',
    'nbc' => '#453645'
);
?>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title><?=loadTitle('navlist.markdown',
                get_config_option('site_title'))?></title>
        <link rel="stylesheet" type="text/css"
                href="<?=$installURL?>/theme/markdown-content.css" />
        <link rel="stylesheet" type="text/css"
                href="<?=theme_url($purpleTheme)?>" />
        <script type="text/javascript"
                src="<?=$installURL?>/utils/utils.js"></script>
        <script type="text/javascript">
            window.onresize = windowResizeAction;
            window.onload = windowLoadAction;
        </script>
        <link rel="stylesheet"
                href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.1.0/styles/default.min.css"
                />
        <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.1.0/highlight.min.js">
        </script>
    </head>
    <body>
        <div id="container"><!-- Start container -->
            <div id="pageHeader"><!-- Start page header -->
                <?=mdTplCommon('header.markdown')?>
            </div><!-- End page header -->
            <div id="middleContainer">
                <div id="navcontainer"><!-- Start Navigation -->
                    <div id="navcontent">
                        <?=loadNav('navlist.markdown')?>
                        <div id="sidebarContainer"><!--Start Sidebar wrapper-->
                            <div id="sidebar"><!-- Start sidebar content -->
                                <?=mdTplCommon('sidebar.markdown')?>
                            </div><!-- End sidebar content -->
                        </div><!-- End sidebar wrapper -->
                    </div>
                    <div id="navfill"></div>
                </div><!-- End navigation -->
                <div id="contentContainer"><!-- Start main content wrapper -->
                    <div id="content" class="markdown-content">
                                                        <!-- Start content -->
                        <?=mdTplCommon('index.markdown')?>
                    </div><!-- End content -->
                </div><!-- End main content wrapper -->
            </div>
            <div class="clearer"></div>
            <div id="footer"><!-- Start Footer -->
                <?=mdTplCommon('copyright.markdown')?>
                <div id="breadcrumbcontainer">
                                        <!-- Start the breadcrumb wrapper -->
                    <?=mdTplCommon('breadcrumb.markdown')?>
                </div><!-- End breadcrumb -->
            </div><!-- End Footer -->
        </div><!-- End container -->
    </body>
</html>
