/*
    File:   ./common/themes/barebones/theme.js
    Author: Chris McKinney
    Edited: Jul 14 2016
    Editor: Chris McKinney

    Description:

    Javascript for default theme.

    Edit History:

    1.7.14  - Created. Moved content from default.

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
window.resizeActions.push(function() {
    // Set the height of the content iframe.
    var contentIFrame = document.getElementById('content-iframe');
    if (contentIFrame != null) {
        contentIFrame.height = 1;
        contentIFrame.height =
            contentIFrame.contentWindow.document.body.scrollHeight;
    }
})
