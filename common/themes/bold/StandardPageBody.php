<?php
/*
    Copyright 2018 Chris McKinney

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

<div id="top"></div>

<div class="navbar sticky-top theme-inverted">
    <nav id="inner-nav" class="navbar navbar-expand-sm theme-inverted p-0 m-auto">
        <a class="navbar-brand" href="#top">
            <?=mdTplCommon('header.markdown')?>
        </a>
        <button class="navbar-toggler" type="button"
                data-toggle="collapse" data-target="#navbar"
                aria-controls="navbar" aria-expanded="false"
                aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div id="navbar" class="navbar-collapse collapse">
            <?php
            $string = rtrim(mdTplCommon('navlist.markdown'));
            $string = substr($string, 0, strrpos($string, "\n"));
            ?>
            <?=$string?>
                <li class="dropdown">
                    <a class="dropdown-toggle" href="#" id="navbarDropdown"
                            role="button" data-toggle="dropdown"
                            aria-haspopup="true" aria-expanded="false">Links</a>
                    <div class="dropdown-menu theme-inverted" aria-labelledby="navbarDropdown">
                        <?=mdTplCommon('sidebar.markdown')?>
                    </div>
                </li>
            </ul>
        </div>
        <script type="text/javascript">
            window.loadActions.push(function() {
                $("#navbar > ul").addClass("navbar-nav mr-auto")
                $("#navbar > ul li").addClass("nav-item");
                $("#navbar > ul a").addClass("nav-link");
                $("#current").parent().addClass("active")
                $("#navbar > ul > .dropdown > .dropdown-menu > ul > li").addClass("dropdown-item");
            });
        </script>
    </nav>
</div>

<main id="container" class="container" role="main">
    <div class="row">
        <div class="col col-xl-10 col-lg-11 mx-lg-auto">
            <div style="clear:both;"></div>
            <div id="content" class="markdown-content"
                    data-spy="scroll" data-target="#navbar" data-offset="0"><!-- Start content -->
                <?=mdTplCommon('index.markdown')?>
            </div><!-- End content -->
            <div style="clear:both; height:5px;"></div>
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
