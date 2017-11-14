<?php
/*
    File:   ./common/themes/bootstrap/StandardPageBody.php
    Author: Chris McKinney
    Edited: July 14 2017
    Editor: Chris McKinney

    Description:

    The body for the default standard page for a TachibanaSite webpage.

    Edit History:

    1.7.14  - Created.

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

<nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed"
                    data-toggle="collapse" data-target="#navbar"
                    aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <?=mdTplCommon('header.markdown')?>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <?php
            $string = rtrim(loadNav('navlist.markdown'));
            $string = substr($string, 0, strrpos($string, "\n"));
            ?>
            <?=$string?>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"
                            role="button" aria-haspopup="true" aria-expanded="false"
                            >Links <span class="caret"></span></a>
                    <ul class="dropdown-menu">
                        <?=mdTplCommon('sidebar.markdown')?>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
<div id="container" class="container" role="main">
    <div id="content" class="markdown-content"><!-- Start content -->
        <?=mdTplCommon('index.markdown')?>
    </div><!-- End content -->
    <div style="clear:both;"></div>
    <div id="footer" class="well">
        <div style="float:right;">
            <p><a href="https://tachibanatech.com/ts/">TachibanaSite</a>
                v<?=get_config_option('version')?></p>
        </div>
        <?=mdTplCommon('copyright.markdown')?>
    </div>
    <?=mdTplCommon('breadcrumb.markdown')?>
</div>
