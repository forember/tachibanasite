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

<?=mdTplCommon('header.markdown')?>
<?=loadNav('navlist.markdown')?>
<div id="sidebar"><!-- Start sidebar content -->
    <?=mdTplCommon('sidebar.markdown')?>
</div><!-- End sidebar content -->
<div id="content" class="markdown-content"><!-- Start content -->
    <?=mdTplCommon('index.markdown')?>
</div><!-- End content -->
<?=mdTplCommon('copyright.markdown')?>
<p><a href="https://tachibanatech.com/ts/">TachibanaSite</a>
    v<?=get_config_option('version')?></p>
<?=mdTplCommon('breadcrumb.markdown')?>
