<?php
/*
    File:   utils/LoadsJavascript.php
    Author: Chris McKinney
    Edited: May 21 2016
    Editor: Chris McKinney

    Description:

    Utilities to load javascript for the whole site.

    Edit History:

    0.5.22  - Created to handle contact forms.

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

$to = get_config_option('email');
$from = get_config_option('sender_email');
$installURL = get_config_option('install_url');

$subject = 'TachibanaTech: ' . $_POST['subject'];
$subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$message = 'You received a message from ' . $_POST['name'];
$replyTo = $_POST['email'];
if ($replyTo) {
    $message .= ' <' . $replyTo . '>';
}
$message .= " on TachibanaTech:\n\n" . $_POST['message'];
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
    header("Location: $installURL/pages/mail-success/");
} else {
    header("Location: $installURL/pages/mail-failure/");
}
die();
?>
