Server software for <https://tachibanatech.com/> and <http://afrl.cse.sc.edu/>.

Documentation at <https://tachibanatech.com/ts/>.

# Version History

## 1.8.1

-   Colored Pencil now has color presets.

## 1.8.0

-   Bootstrap 4 Beta 2
-   New theme: Colored Pencil

## 1.7.15

-   Now that we have real mobile support, it's about time the `people` module
    got the ability to set photo dimensions. Only took a year and a half.

## 1.7.14

-   Added Bootstrap support.
-   Added ability to disable modules in config.ini.
-   Bug fixes.

## 1.4.18

-   New "paper" theme.

## 1.1.29

-   Added common file SendMailFilter.php

## 0.12.20

-   Made the TachibanaSite version link to the documentation.
-   Added the hianchor module for highlighting the current anchor.

## 0.11.24

-   Made the default theme main container more reasonably-sized on large
    screens and mobile.

-   Made captions act more reasonably.
-   Added check for empty mail.

## 0.9.23

-   Added KaTeX support.

## 0.8.24

-   Added template switch and common override recursion.

## 0.8.22

-   Made some enhancements to the photos module.

## 0.8.18

-   Made SendMail.php use config site title.

## 0.8.11

-   Added modules from old AFRL site:
    -   csv2table: generates tables from CSV files.
    -   nosidebar: removes sidebar if element with id `nosidebar` is present.

## 0.8.10

-   Added a module system. Created modules:
    -   mobiletext: enlarges content text on mobile.
    -   people: handles displaying "about me"-style information.
    -   photos: nice column layout for photos.
    -   highlight.js: loads highlight.js files.
    -   highlight.js-exec: highlights code using highlight.js.

## 0.6.22 (& 0.6.20)

-   Added photo column and thumbnail support.
-   Added favicon support (favicon.png in common).

## 0.5.22 A

-   Added mail support.

## 0.5.21

-   Moved theme presets from the standard page into the theme.
-   Made the theme image URLs relative.
-   Added theme options to config.
-   Moved the standard page into the theme and separated the head and body.
-   Moved theme-related javascript from utils to the theme.
-   Added email obfustication (deobfusticated by js).
-   Added section parsing support for config.
-   Added URL support to common override mechanic.
-   Added theme loading utilities.
-   Added script loading utilities.
-   Added registration for actions on window events (load and resize).

## 0.4.6

-   Added versioning.
-   Added jQuery support.
