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

// Get path to tachibanasite directory.
$installPath = realpath(__DIR__ . '/../../..');
// Import utilities.
include_once "$installPath/utils/MarkdownUtils.php";
include_once "$installPath/utils/NavFilter.php";
include_once "$installPath/utils/ConfigIniUtils.php";
?>

<main id="container" class="container" role="main">
    <div class="row row-offcanvas row-offcanvas-left">
        <div id="sidebar" class="col-6 col-md-2 sidebar-offcanvas"
            style="display: inline-block; min-width: 10em; max-width: 12em">
            <div class="list-group">
                <div id="navcontent">
                    <?=loadNav('navlist.markdown')?>
                    <div id="sidebarContainer"><!--Start Sidebar wrapper-->
                        <div id="sidebar"><!-- Start sidebar content -->
                            <?=mdTplCommon('sidebar.markdown')?>
                        </div><!-- End sidebar content -->
                    </div><!-- End sidebar wrapper -->
                </div>
            </div>
        </div>
        <div class="col-12 col-md-9">
            <div id="pageHeader"><!-- Start page header -->
                <h1><div class="float-left d-md-none"
                    style="font-size: 0; margin-right: 10px">
                    <button type="button" class="btn btn-primary btn-sm"
                        data-toggle="offcanvas">&#8801;</button>
                </div></h1>
                <?=mdTplCommon('header.markdown')?>
            </div><!-- End page header -->
            <div style="clear:both;"></div>
            <div id="content" class="markdown-content"><!-- Start content -->
                <?=mdTplCommon('index.markdown')?>
            </div><!-- End content -->
            <div style="clear:both;"></div>
            <footer id="footer" class="well">
                <div style="float:right;">
                    <p><a href="https://tachibanatech.com/ts/">TachibanaSite</a>
                        v<?=get_config_option('version')?></p>
                </div>
                <?=mdTplCommon('copyright.markdown')?>
            </footer>
            <?=mdTplCommon('breadcrumb.markdown')?>
        </div>
    </div>
</main>
