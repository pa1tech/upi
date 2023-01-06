<?php

$update = json_decode(file_get_contents("php://input"), TRUE);
$path = "https://api.telegram.org/bot<TOKEN>";


if( sizeof($update['inline_query']) > 0){
    
$chatId = $update['inline_query']["id"];
$query = $update['inline_query']["query"];

$inpVars =  explode(" ", $query);

if( sizeof(explode("@", $inpVars[0])) == 1 ){
        //Bank
        if(sizeof($inpVars) > 1){
            $ac = $inpVars[0];
            $ifsc = $inpVars[1];
            $title = $ac." - ".$ifsc;
            $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=".$ac."@".$ifsc.".ifsc.npci%26pn=Whomsoever&chld=H?raw=True";
            $descp = "Scan this <a href='{$url}'>QR</a>\n(or)\n<b><a href='https://pa1tech.github.io/upi/bank/?{$ac}&{$ifsc}'>Click here</a></b> to pay <b>{$ac}-{$ifsc}</b>";
            if(sizeof($inpVars) == 3){
                $amt = $inpVars[2];
                $title = $ac." - ".$ifsc." - ₹".$amt;

                $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa={$ac}@{$ifsc}.ifsc.npci%26am={$amt}%26pn=Whomsoever&chld=H?raw=True";
                $descp = "Scan this <a href='{$url}'>QR</a>\n(or)\n<b><a href='https://pa1tech.github.io/upi/bank/?{$ac}&{$ifsc}&{$amt}'>Click here</a></b> to pay ₹{$amt} to<b>{$ac}-{$ifsc}</b>";
            }
        
    }
    }else{
        //UPI
        if(sizeof($inpVars) > 0){
            $upi = $inpVars[0];
            $title = $upi;
            
            $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa={$upi}%26pn=Whomsoever&chld=H?raw=True";
            
            $descp = "Scan this <a href='{$url}'>QR</a>\n(or)\n<b><a href='https://pa1tech.github.io/upi/?{$upi}'>Click here</a></b> to pay <b>{$upi}</b>";
   
            if(sizeof($inpVars) == 2){
                $amt = $inpVars[1];
                $title = $upi." - ₹".$amt;
                $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa={$upi}%26am={$amt}%26pn=Whomsoever&chld=H?raw=True";
                $descp = "Scan this <a href='{$url}'>QR</a>\n(or)\n<b><a href='https://pa1tech.github.io/upi/?{$upi}&{$amt}'>Click here</a></b> to pay ₹{$amt} to <b>{$upi}</b>";
               
            }
            
        }
    }

$results = array();

$entry = array(
    "type" => "article", 
    "id" => "1", 
    "title" => $title,  
    "input_message_content" => array(
                                "message_text" => $descp,
                                "parse_mode" => "HTML"
                                )
    
);

array_push($results, $entry);

$post = array(
    "inline_query_id" => $chatId, 
    "results" => json_encode($results)
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,$path."/answerInlineQuery");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
$content = curl_exec ($ch);
curl_close ($ch);
}

$start_msg = <<<EOD
Welcome to *!ncred UPI Pay!*

This bot helps you to create UPI payment link and QR, which you can share with your friends to receive money

*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
Example: *pmcares@sbi 11*

*Just VPA:* Send <upi id> to the bot. Sender has the freedom to fill the amount to be sent 
Example: *pmcares@sbi*

*Bank A/C, IFSC and Amount:* Beneficiary a/c no., IFSC and payable amount are to be sent in the format <a/c no.><space><ifsc><space><amount>
Example: *917897897897 PYTM0123456 116*

*Bank A/C, IFSC:* Send <a/c no.><space><ifsc> to the bot. Sender has the freedom to fill the amount to be sent. 
Example: *917897897897 PYTM0123456*

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Inline usage examples:
  1. *@incred_upibot pmcares@sbi 11*
  2. *@incred_upibot pmcares@sbi*
  3. *@incred_upibot 917897897897 PYTM0123456 116*
  4. *@incred_upibot 917897897897 PYTM0123456*

To know more about the working of the bot : /about

*Please note,* the links generated are purely front-end and are not saved on the bot server

PS: Looks like the payment via link is being allowed on BHIM but other apps are not allowing for security reasons. QR's work just fine
EOD;

$help_msg = <<<EOD
*VPA and Amount:* Receiver UPI ID and payable amount are to be sent in the format <upi id><space><amount>
Example: *pmcares@sbi 11*

*Just VPA:* This creates QR and link with just the receiver UPI ID. Sender has the freedom to fill the amount to be sent. Send <upi id> to the bot 
Example: *pmcares@sbi*

*Bank A/C, IFSC and Amount:* Beneficiary a/c no., IFSC and payable amount are to be sent in the format <a/c no.><space><ifsc><space><amount>
Example: *917897897897 PYTM0123456 116*

*Bank A/C, IFSC:* This creates QR and link to the specified a/c no. and IFSC. Sender has the freedom to fill the amount to be sent. Send <a/c no.><space><ifsc> to the bot 
Example: *917897897897 PYTM0123456*

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Inline usage examples:
  1. *@incred_upibot pmcares@sbi 11*
  2. *@incred_upibot pmcares@sbi*
  3. *@incred_upibot 917897897897 PYTM0123456 116*
  4. *@incred_upibot 917897897897 PYTM0123456*

To know more about the working of the bot : /about
EOD;

$about_msg = <<<EOD
This bot has been developed in pHp using Telegram BotAPI
QR codes are genearted using [Google Charts API](https://developers.google.com/chart/infographics/docs/qr_codes)

[Source Code](https://github.com/pa1tech/upi/tree/master/incred_upibot) 
Developer: @pa1tech
EOD;

$help_msg = urlencode($help_msg);
$about_msg = urlencode($about_msg);
$start_msg = urlencode($start_msg);

$chatId = $update["message"]["chat"]["id"];
$message = $update["message"]["text"];

if ($message == "/start") {
    file_get_contents($path."/sendmessage?chat_id=".$chatId."&parse_mode=MARKDOWN&text=".$start_msg);
} elseif ($message == "/about") {
    file_get_contents($path."/sendmessage?chat_id=".$chatId."&parse_mode=MARKDOWN&text=".$about_msg);
} elseif ($message == "/help") {
    file_get_contents($path."/sendmessage?chat_id=".$chatId."&parse_mode=MARKDOWN&text=".$help_msg);
}else{
    $inpVars =  explode(" ", $message);
    
    if( sizeof(explode("@", $inpVars[0])) == 1 ){
        //Bank
        if(sizeof($inpVars) > 1){
            $ac = $inpVars[0];
            $ifsc = $inpVars[1];
            $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa=".$ac."@".$ifsc.".ifsc.npci%26pn=Whomsoever&chld=H?raw=True";
            $descp = "<b><a href='https://pa1tech.github.io/upi/bank/?{$ac}&{$ifsc}'>Click here</a></b> to pay <b>{$ac}-{$ifsc}</b>\n(or)\nScan the above QR";
            if(sizeof($inpVars) == 3){
                $amt = $inpVars[2];
                $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa={$ac}@{$ifsc}.ifsc.npci%26am={$amt}%26pn=Whomsoever&chld=H?raw=True";
                $descp = "<b><a href='https://pa1tech.github.io/upi/bank/?{$ac}&{$ifsc}&{$amt}'>Click here</a></b> to pay ₹{$amt} to <b>{$ac}-{$ifsc}</b>\n(or)\nScan the above QR";
            }
            file_get_contents($path."/sendphoto?chat_id=".$chatId."&photo=".urlencode($url)."&caption=".urlencode($descp)."&parse_mode=HTML");
    }
    }else{
        //UPI
        if(sizeof($inpVars) > 0){
            $upi = $inpVars[0];
            
            $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa={$upi}%26pn=Whomsoever&chld=H?raw=True";
            
            $descp = "<b><a href='https://pa1tech.github.io/upi/?{$upi}'>Click here</a></b> to pay <b>{$upi}</b>\n(or)\nScan the above QR";
            if(sizeof($inpVars) == 2){
                $amt = $inpVars[1];
                $url = "https://chart.googleapis.com/chart?chs=350x350&cht=qr&chl=upi://pay?pa={$upi}%26am={$amt}%26pn=Whomsoever&chld=H?raw=True";
                $descp = "<b><a href='https://pa1tech.github.io/upi/?{$upi}&{$amt}'>Click here</a></b> to pay ₹{$amt} to <b>{$upi}</b>\n(or)\nScan the above QR";
            }
            
            file_get_contents($path."/sendphoto?chat_id=".$chatId."&photo=".urlencode($url)."&caption=".urlencode($descp)."&parse_mode=HTML");
        }
    }
}
//https://api.telegram.org/bot<TOKEN>/setwebhook/?url=https://homenet2683.000webhostapp.com/upi.php
//https://nordicapis.com/how-to-build-your-first-telegram-bot-using-php-in-under-30-minutes/
?>