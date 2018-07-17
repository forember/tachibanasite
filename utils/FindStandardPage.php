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

// Include utilitues.
include_once 'Theme.php';
// Change to the directory of the current page.
chdir(dirname($_SERVER['SCRIPT_FILENAME']));
// Find the standard page.
$stdPagePath = get_theme_path_wfallback('StandardPage.php');
// Include the standard page.
include "$stdPagePath";
?>
