/*
    File:   ./common/themes/default/theme.js
    Author: Chris McKinney
    Edited: Aug 10 2016
    Editor: Chris McKinney

    Description:

    Javascript for default theme.

    Edit History:

    0.8.10  - Moved mobile stuff to mobiletext module.
            - Moved people stuff to people module.

    0.5.21  - Created. Moved content from utils.js.
            - Added email (de)obfuscation.

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

var containerMarginTop = null;

window.resizeActions.push(function() {
    // Set the height of the content iframe.
    var contentIFrame = document.getElementById('content-iframe');
    if (contentIFrame != null) {
        contentIFrame.height = 1;
        contentIFrame.height =
            contentIFrame.contentWindow.document.body.scrollHeight;
    }
    // Fill out the sidebar.
    document.getElementById('navfill').style.height = '0';
    var middleHeight = document.getElementById('middleContainer').offsetHeight;
    var navHeight = document.getElementById('navcontent').offsetHeight;
    var newHeight = ((middleHeight - navHeight) + 1) + 'px';
    document.getElementById('navfill').style.height = newHeight;
    // Push page up if not enough room.
    var container = document.getElementById('container');
    if (containerMarginTop == null) {
        containerMarginTop = container.style.marginTop;
    } else {
        container.style.marginTop = containerMarginTop;
    }
    var cFullHeight = container.offsetHeight + container.offsetTop;
    if (window.innerHeight < cFullHeight) {
        var chdiff = window.innerHeight - container.offsetHeight;
        if (chdiff < 0) {
            chdiff = 0;
        }
        container.style.marginTop = chdiff + 'px';
    }
})
