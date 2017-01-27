<?php
/*
    File:   common/themes/default/StandardPageBody.php
    Author: Chris McKinney
    Edited: May 21 2016
    Editor: Chris McKinney

    Description:

    The body for the default standard page for a TachibanaSite webpage.

    Edit History:

    0.5.21  - Created. Moved content from standard page.

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
// Import utilities.
include_once "$installPath/utils/MarkdownUtils.php";
include_once "$installPath/utils/NavFilter.php";
include_once "$installPath/utils/ConfigIniUtils.php";
?>

<div id="container"><!-- Start container -->
    <div id="pageHeader"><!-- Start page header -->
        <?=mdTplCommon('header.markdown')?>
    </div><!-- End page header -->
    <div id="middleContainer"><!-- Start middle -->
        <div id="navcontainer"><!-- Start navigation -->
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
            <div id="content" class="markdown-content"><!-- Start content -->
                <?=mdTplCommon('index.markdown')?>
            </div><!-- End content -->
        </div><!-- End main content wrapper -->
    </div> <!-- End middle -->
    <div class="clearer"></div>
    <div id="footer"><!-- Start Footer -->
        <div style="float:right;">
            <p><a href="https://tachibanatech.com/ts/">TachibanaSite</a>
                v<?=get_config_option('version')?></p>
        </div>
        <?=mdTplCommon('copyright.markdown')?>
        <div id="breadcrumbcontainer"><!-- Start the breadcrumb wrapper -->
            <?=mdTplCommon('breadcrumb.markdown')?>
        </div><!-- End breadcrumb -->
    </div><!-- End Footer -->
</div><!-- End container -->
