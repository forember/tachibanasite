/*
    File:   modules/katex.exec/katex-exec.js
    Author: Chris McKinney
    Edited: Sep 23 2016
    Editor: Chris McKinney

    Description:

    Automatically converts elements with class "katex" from LaTeX to HTML.

    Edit History:

    0.9.23  - Created to support KaTeX.

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

window.loadActions.push(function() {
    $(".katex-math").each(function() {
        var latex = $(this).text();
        var html = katex.renderToString(latex);
        $(this).html(html);
    });
    $(".katex-display").each(function() {
        var latex = $(this).text();
        var html = katex.renderToString(latex, {displayMode: true});
        $(this).html(html);
    });
})
