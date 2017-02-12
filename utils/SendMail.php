<?php
/*
    File:   utils/SendMail.php
    Author: Chris McKinney
    Edited: May 21 2016
    Editor: Chris McKinney

    Description:

    Sends email from a contact form.

    Edit History:

    0.5.22  - Created to handle contact forms.

    0.8.18  - Made site title generic.

    0.11.24 - Now checks that name, subject, and message are non-empty.

    1.1.29  - Added mail filter.

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

include 'ConfigIniUtils.php';
include 'MarkdownUtils.php';

$to = get_config_option('email');
$from = get_config_option('sender_email');
$installURL = get_config_option('install_url');
$siteTitle = get_config_option('site_title');

function mailSuccess() {
    global $installURL;
    header("Location: $installURL/pages/mail-success/");
    die();
}

function mailFailure() {
    global $installURL;
    header("Location: $installURL/pages/mail-failure/");
    die();
}

if (!($_POST['subject'] && $_POST['name'] && $_POST['message'])) {
    mailFailure();
}

$filterPath = pathCommon('SendMailFilter.php');
if (file_exists($filterPath)) {
    include $filterPath;
}

$subject = "$siteTitle: " . $_POST['subject'];
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$message = 'You received a message from ' . $_POST['name'];
$replyTo = $_POST['email'];
if ($replyTo) {
    $message .= ' <' . $replyTo . '>';
}
$message .= " on $siteTitle:\n\n" . $_POST['message'];
$message = preg_replace('/([^\r])\n/', "\${1}\r\n", $message);

$headers = "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=utf-8\r\n";
$headers .= 'X-Mailer: PHP/' . phpversion() . "\r\n";
$encodedName = '=?UTF-8?B?' . base64_encode($_POST['name']) . '?=';
$headers .= "From: $encodedName <$from>\r\n";
if (preg_match('/^[a-zA-Z0-9._\-]+@[a-zA-Z0-9._\-]+$/', $replyTo)) {
    $headers .= "Reply-To: $replyTo\r\n";
}

if(mail($to, $subject, $message, $headers)) {
    mailSuccess();
} else {
    mailFailure();
}
?>
