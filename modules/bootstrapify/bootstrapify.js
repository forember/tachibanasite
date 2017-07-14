/*
    File:   modules/mobiletext/mobiletext.js
    Author: Chris McKinney
    Edited: Aug 10 2016
    Editor: Chris McKinney

    Description:

    Crude mobile support.

    Edit History:

    0.8.10  - Created. Moved content from theme.js.

    0.11.24 - Made the container go edge-to-edge.

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
    $("#content table").addClass("table");
    $("#content pre code").addClass("well");
    $("#content pre code").css("margin-bottom", "0");
    $("#content .sidephoto").addClass("img-thumbnail");
    $("#content img.columnphoto").addClass("img-thumbnail");
    $(".navbar-header a").addClass("navbar-brand");
    $(".navbar-header h1").css("margin", "0");
    $("nav ul").first().addClass("nav navbar-nav");
    $("nav a").css("text-decoration", "none");
    $("nav #current").parent().addClass("active");
    $(".dropdown-menu").css("padding", "0");
    $(".dropdown-menu ul").addClass("list-group");
    $(".dropdown-menu ul").css("margin-bottom", "0");
    $(".dropdown-menu ul a").addClass("list-group-item");
    $(".dropdown-menu ul a").css("color", "#66c");
    $(".dropdown-menu ul a").each(function() {
        var p = $(this).parent();
        p.before(this);
        p.remove();
    })
})
