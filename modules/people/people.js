/*
    File:   ./modules/people/people.js
    Author: Chris McKinney
    Edited: Aug 10 2016
    Editor: Chris McKinney

    Description:

    Crude mobile support.

    Edit History:

    0.8.10  - Created. Moved content from theme.js.

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

function deobfuscateEmail(t, mailto) {
    t = decodeURIComponent(t);
    s = '';
    for (var i = 0; i < t.length; ++i) {
        var c = t.charCodeAt(i);
        if (mailto) {
            s += String.fromCharCode(c ^ 0x1f);
        } else {
            s += '&#' + (c ^ 0x1f) + ';<span style="display:none">@</span>';
        }
    }
    return s;
}

window.loadActions.push(function() {
    var emailRegex = /^@@([jkhinolmbc]{4})<code>([%\/_.\-a-zA-Z0-9]+)<\/code>\1@@$/;
    $('a').each(function() {
        var href = $(this).attr('href');
        var hrefm = emailRegex.exec(href);
        if (hrefm != null) {
            $(this).attr('href', deobfuscateEmail(hrefm[2], true));
        }
        var html = $(this).html();
        var htmlm = emailRegex.exec(html);
        if (htmlm != null) {
            $(this).html(deobfuscateEmail(htmlm[2], false));
        }
    });
});

window.resizeActions.push(function() {
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
})
