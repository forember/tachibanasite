/*
    File:   common/themes/default/theme.js
    Author: Chris McKinney
    Edited: May 21 2016
    Editor: Chris McKinney

    Description:

    Javascript for default theme.

    Edit History:

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

function deobfuscateEmail(t) {
    t = decodeURIComponent(t);
    s = "";
    for (var i = 0; i < t.length; ++i) {
        var c = t.charCodeAt(i);
        s += String.fromCharCode(c ^ 0x1f);
    }
    return s;
}

window.loadActions.push(function() {
    var emailRegex = /^@@([jkhinolmbc]{4})<code>([%\/_.\-a-zA-Z0-9]+)<\/code>\1@@$/
    $('a').each(function() {
        var href = $(this).attr('href');
        var hrefm = emailRegex.exec(href);
        if (hrefm != null) {
            $(this).attr('href', deobfuscateEmail(hrefm[2]));
        }
        var html = $(this).html();
        var htmlm = emailRegex.exec(html);
        if (htmlm != null) {
            $(this).text(deobfuscateEmail(htmlm[2]));
        }
    });
});

var containerMarginTop = null;

window.resizeActions.push(function() {
    // Mobile
    if (window.mobilecheck()) {
        document.getElementById('content').style.fontSize = '300%';
    }
    // Push the whole about me section below the photo if there are less than
    // 250 pixels available to the right of the photo.
    var people = document.getElementsByClassName('person');
    for (var i = 0; i < people.length; i++) {
        var person = people[i];
        var photos = person.getElementsByClassName('person-photo');
        var names = person.getElementsByClassName('person-name');
        for (var j = 0; j < photos.length; j++) {
            photos[j].parentNode.style.padding = '0';
        }
        if (photos.length > 0 && names.length > 0) {
            if (person.clientWidth - photos[0].offsetWidth < 250) {
                names[0].style.clear = 'right';
            } else {
                names[0].style.clear = 'none';
            }
        }
    }
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
