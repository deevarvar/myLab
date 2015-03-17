<?php

function getPhoneUser(){
$phone = "18511878557";
return 	$phone;
}

   //发送监控短信，多个手机号以逗号,分割
function sendSmsp($phone, $content) {
    $username = 'lbs_movie';
    $password = '%^Gf8)T#';
    $base_url = 'http://emsg.baidu.com/service/sendSms.json';
    $businessCode = '695'; 
    $priority = 9;
    $signature = md5($username . $password . $phone . $content . $businessCode . $priority);

    $param = array(
        'businessCode' => $businessCode,
        'msgDest' => $phone, 
        'msgContent' => $content,
        'username' => $username,
        'signature' => $signature,
        'priority' => $priority,
    );      
    $data = array(
        'errorNo' => '-1',
        'errorMsg' => "",
        'phone' => $phone, 
    );      
    $reponse = array();
    $times = 0;
    $retry = 2;
    while (empty($reponse) && ($times < $retry)) {
        $reponse = curl_post($base_url, $param);
        if (empty($reponse)) {
            $times++;
            continue;
        }       
        $reponse = json_decode($reponse, true);
        if ($reponse['result'] == 1000) {  
            $data['errorNo'] = 0;
            break;
        } else {
            $times++;
            continue;
        }
     }
    return $data;
}

//发送post/get请求
function curl_post($post_url, $data=array(), $ispost = 1, $is_http_build_query = true) { 
    $timeStart = microtime(true);
    $fargvs = func_get_args();
    unset($fargvs);
    if ($is_http_build_query) {
        $post = http_build_query($data);
    } else {
        $post = '';
        foreach ($data as $k => $v) {
            $post.=$k . '=' . $v . '&';
        }       
        $post = substr($post, 0, -1); 
    }       
    $login = curl_init($post_url); //创建CURL对象  
    curl_setopt($login, CURLOPT_HEADER, 0); //返回头部  
    curl_setopt($login, CURLOPT_RETURNTRANSFER, 1); //返回信息  
    if ($ispost) {
        curl_setopt($login, CURLOPT_POST, $ispost); //设置POST提交  
        curl_setopt($login, CURLOPT_POSTFIELDS, $post); //提交POST数据  
    }       
    curl_setopt($login, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($login, CURLOPT_SSL_VERIFYPEER, 0);
    if (strtolower(substr(PHP_SAPI, 0, 3)) == 'cli') {
        curl_setopt($login, CURLOPT_TIMEOUT, 30);
    } else {
        curl_setopt($login, CURLOPT_TIMEOUT, 3);
    }       
    $data = curl_exec($login); //执行已经定义的设置  
    curl_close($login); //关闭 */ 
    return $data;
}
?>

