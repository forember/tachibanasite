/*
    File:   modules/hianchir/hianchor.js
    Author: Chris McKinney
    Edited: Aug 10 2016
    Editor: Chris McKinney

    Description:

    Highlights the current anchor.

    Edit History:

    0.12.20 - Created.

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

window.hianchor_bg = undefined;
window.hianchor_hash = undefined;

window.hianchor_update = function () {
    if (window.hianchor_hash !== undefined) {
        $(window.hianchor_hash).css("background-color", window.hianchor_bg);
    }
    window.hianchor_hash = window.location.hash;
    window.hianchor_bg = $(window.hianchor_hash).css("background-color");
    $(window.hianchor_hash).css("background-color", "#ff0");
}

window.loadActions.push(function() {
    window.hianchor_update();
    $(window).on('hashchange', window.hianchor_update)
})
