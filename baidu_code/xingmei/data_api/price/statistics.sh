#!/bin/bash
#author: yezhihua@baidu.com

#25%
badPlanGate=25


function addplandetails(){


    #details
    echo "<br>" >> $htmlfile
    echo "<table border=\"1\">" >> $htmlfile
    echo "<caption>问题排期影院统计</caption>" >> $htmlfile
    echo "<th>影院id</th>" >> $htmlfile
    echo "<th>影院名</th>" >> $htmlfile
    echo "<th>今天排期数</th>" >> $htmlfile
    echo "<th>明天排期数</th>" >> $htmlfile
    echo "<th>后天排期数</th>" >> $htmlfile
    while read line
    do
        cid=$(echo $line|cut -d , -f 1)
        cname=$(echo $line|cut -d , -f 2)
        today=$(echo $line|cut -d , -f 3)
        tomorrow=$(echo $line|cut -d , -f 4)
        aftertomorrow=$(echo $line|cut -d , -f 5)
        echo "<tr>" >> $htmlfile
        echo "<td>$cid</td>" >> $htmlfile
        echo "<td>$cname</td>" >> $htmlfile
        echo "<td>$today</td>" >> $htmlfile
        echo "<td>$tomorrow</td>"  >> $htmlfile
        echo "<td>$aftertomorrow</td>" >> $htmlfile
        echo "</tr>" >> $htmlfile
    done < badplan.csv
    echo "</table>" >> $htmlfile

}


function addplancontent(){
    badplannum=$(cat planstat.csv |awk -F, '$3==0||$4==0||$5==0'|wc -l)
    cat planstat.csv |awk -F, '$3==0&&$4==0&&$5==0' > noplan.csv

    cat planstat.csv | awk -F, '$3!=0&&$4==0&&$5==0'>oneplan.csv
    cat planstat.csv | awk -F, '$3==0&&$4!=0&&$5==0'>>oneplan.csv
    cat planstat.csv | awk -F, '$3==0&&$4==0&&$5!=0'>>oneplan.csv

   # cat planstat.csv | awk -F, '$3!=0&&$4!=0&&$5==0'>twoplan.csv
   # cat planstat.csv | awk -F, '$3==0&&$4!=0&&$5!=0'>>twoplan.csv
   # cat planstat.csv | awk -F, '$3!=0&&$4==0&&$5!=0'>>twoplan.csv

    noplannum=$(cat noplan.csv|wc -l)
    oneplannum=$(cat oneplan.csv|wc -l)
 #   twoplannum=$(cat twoplan.csv|wc -l)
    totalnum=$(cat planstat.csv|wc -l)
    totalnum=$((totalnum-1))
    : > badplan.csv
    cat noplan.csv >> badplan.csv
    cat oneplan.csv >> badplan.csv
  #  cat twoplan.csv >> badplan.csv

    badnum=$(cat badplan.csv|wc -l)
    noplanratio=$(echo $noplannum $totalnum| awk '{printf "%.2f", $1*100/$2}')
    oneplanratio=$(echo $oneplannum $totalnum| awk '{printf "%.2f", $1*100/$2}')
#   twoplanratio=$(echo $twoplannum $totalnum| awk '{printf "%.2f", $1*100/$2}')
    badratio=$(echo $noplannum $oneplannum $totalnum| awk '{printf "%.2f", ($1+$2)*100/$3}')

    badrateFlag=$(echo  $badratio '>' $badPlanGate|bc -l)

    if [ $badrateFlag -eq 1 ] || [ $noplannum -gt 0 ];then
        planFlag=1
    else
        planFlag=0
    fi


    echo $planFlag > badplanflag

    #add option to view the rate even the rate is below the water
    if [ $planFlag -eq 1 ] || [  $htmlfile != "xingmei_monitor.html" ];then

    echo "<table border=\"1\">" >> $htmlfile
    echo "<caption>排期问题影院比例</caption>" >> $htmlfile
    echo "<th>无排期比例($noplannum/$totalnum)</th>" >> $htmlfile
    echo "<th>一天排期比例($oneplannum/$totalnum)</th>" >> $htmlfile
#    echo "<th>两天排期比例($twoplannum/$totalnum)</th>" >> $htmlfile
    echo "<th>总计($badnum/$totalnum)</th>" >> $htmlfile
    echo "<tr>" >> $htmlfile
    echo "<td>$noplanratio%</td>" >> $htmlfile
    echo "<td>$oneplanratio%</td>" >> $htmlfile
 #  echo "<td>$twoplanratio%</td>" >> $htmlfile
    echo "<td style=\"color: red; font-weight: bold\">$badratio%</td>"  >> $htmlfile
    echo "</tr>" >> $htmlfile
    echo "</table>" >> $htmlfile

    addplandetails

    echo "<p> 星美排期检测规则:</p>" >> $htmlfile
    echo "<p>0. 如果有<span style=\"font-weight: bold\">没有排期</span>的影院， 会发报警邮件</p>" >>$htmlfile
    echo "<p>1. <span style=\"font-weight: bold\">没有排期</span>的和<span style=\"font-weight: bold\">只有一天排期</span>的影院比例占到总影院的<span style=\"color: red; font-weight: bold\">$badPlanGate%</span>， 就发报警邮件</p>" >> $htmlfile
    echo "<hr>" >> $htmlfile
    fi


}

function addpricecontent(){

wrongpricenum=$(wc -l wrongprice.csv|cut -d ' ' -f 1)

if [ $wrongpricenum -eq 1 ];then
    echo "no wrong price plan."
    return
fi


sed -n '2,$p' wrongprice.csv |awk -F, '{print $2}'|sort -n|uniq > cinema.list
cinematotal=$(wc -l cinema.list|cut -d ' ' -f 1)
primetotal=$(cat wrongprice.csv| awk -F, -v primetime=14 '$primetime==1'|wc -l|cut -f 1)
plantotal=$(wc -l wrongprice.csv|cut -d ' ' -f 1)
plantotal=$(echo ${plantotal}-1|bc)
nonprimetotal=$(echo ${plantotal}-${primetotal}|bc)

echo $cinematotal, $plantotal,$primetotal, $nonprimetotal,
echo "<p> 如果有问题场次，详细非黄价格场次请见附件wrong.csv</p>" >> $htmlfile

echo "<table border=\"1\">" >> $htmlfile
echo "<caption>非黄价格场次总结统计</caption>" >> $htmlfile
echo "<th>问题影院总数</th>" >> $htmlfile
echo "<th>问题场次总数</th>" >> $htmlfile
echo "<th>非黄场次总数</th>" >> $htmlfile
echo "<th>黄金场次总数</th>" >> $htmlfile
echo "<tr>" >> $htmlfile
echo "<td>$cinematotal</td>" >> $htmlfile
echo "<td>$plantotal</td>" >> $htmlfile
echo "<td>$nonprimetotal</td>" >> $htmlfile
echo "<td>$primetotal</td>"  >> $htmlfile
echo "</tr>" >> $htmlfile
echo "</table>" >> $htmlfile
echo "<br>" >> $htmlfile
echo "<table border=\"1\">" >> $htmlfile
echo "<caption>星美价格监控</caption>" >> $htmlfile
echo "<tr>" >> $htmlfile
echo "<th>一/二线城市</th>" >> $htmlfile
echo "<th>影院id</th>" >> $htmlfile
echo "<th>影院名</th>" >> $htmlfile
echo "<th>非黄价格问题场次数</th>" >> $htmlfile
echo "<th>黄金时段价格问题场次数</th>" >> $htmlfile
echo "</tr>" >> $htmlfile

while read cid
do
    totalnum=$(awk -F , -v cid=$cid  -v namefield=3 -v idfield=2 '$idfield==cid {print $namefield}' wrongprice.csv|wc -l)
    nonprimenum=$(awk -F , -v cid=$cid -v namefield=3 -v idfield=2 -v primetime=14 '$idfield==cid&&$primetime==0 {print $namefield}' wrongprice.csv|wc -l)
    citytype=$(awk -F , -v cid=$cid -v cityfield=1 -v idfield=2 '$idfield==cid {print $cityfield}' wrongprice.csv|uniq)
    cityname=$(awk -F , -v cid=$cid -v namefield=3 -v idfield=2 '$idfield==cid {print $namefield}' wrongprice.csv|uniq)
    primenum=$(echo $totalnum-$nonprimenum|bc)
    echo $cid, $cityname, $citytype, $totalnum, $nonprimenum, $primenum

echo "<tr>" >> $htmlfile

if [ $citytype == "second" ];then
    realname="二线"
else realname="一线"
fi

echo "<td>$realname</td>" >> $htmlfile
echo "<td>$cid</td>" >> $htmlfile
echo  "<td>$cityname</td>" >> $htmlfile
echo  "<td>$nonprimenum</td>" >> $htmlfile
echo  "<td>$primenum</td>" >> $htmlfile

echo  "</tr>" >> $htmlfile
done < cinema.list

echo "</table>" >> $htmlfile

echo "<p> 星美价格规则:</p>" >> $htmlfile
echo "<p>0. 法定节假日按照周六日的规则;周六日如果是工作日，按照工作日规则</p>" >> $htmlfile
echo "<p>1. 一线城市影城 0：00 – 2：00  6折 ，周一至五 2：00 – 17:15 3D影片结算价30元，2D影片结算价25元； 17：15以后 6折。 六日 2:00 – 12：00 3D影片结算价 30元， 2D影片结算价25元；以后6折。</p>" >> $htmlfile
echo "<p>2.	二线城市影城 0：00 – 2：00  6折 ，周一至五 2：00 – 17:15 3D影片结算价25元，2D影片结算价20元； 17：15以后 6折。 六日 2:00 – 12：00 3D影片结算价25元， 2D影片结算价20元；以后6折。</p>" >> $htmlfile
echo "<p>3. 四个影城（北京金源、上海正大、成都环球中心、拉萨神力）周一至五 2：00 – 17:15 所有片结算价按照一线二线计算， 17：15以后 7折， 六日 2:00 – 12：00 所有片结算价按照一线二线计算， 以后7折</p>" >> $htmlfile
echo "<p>4.	影厅类型非普通厅（包括 VIP厅、Imax厅、巨幕厅、贵宾厅） 影片类型非普通影片（包括 Imax Dmax 等非2D 3D）的场次都为原价。</p>" >> $htmlfile
echo "<p>其他特殊规则</p>" >> $htmlfile
echo "<p>1. 针对《北京纽约》在2015.3.6,3.7,3.8三天的价格设置为最低价</p>" >> $htmlfile
echo "<p>2.	星美合资影院和暂停营业的影院不在合作范围内，星美目前的合资影院有： </p>" >> $htmlfile
echo "<p>合资店信息如下：北京世纪东都、广州华影、成都西南影都、成都沙河、南宁新世界、无锡站前、天津盛林、天津星月同辉、郑州上街</p>" >> $htmlfile
echo "<p>暂停营业的影院有：南昌红谷新城</p>" >> $htmlfile


}


cityfield=1
idfield=2
namefield=3
timefield=7
weekdayfield=8
primetime=14
htmlfile=${1:-xingmei_monitor.html}



: > $htmlfile
echo "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN http://www.w3.org/TR/html4/loose.dtd\">" >> $htmlfile
echo "<html>" >> $htmlfile
echo "<head>" >> $htmlfile
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">" >> $htmlfile
echo "<style type=\"text/css\">" >> $htmlfile
echo "table {border-collapse: collapse;}" >> $htmlfile
echo "td {padding: 0px;text-align: center;}" >> $htmlfile
echo "</style>" >> $htmlfile
echo "</head>" >> $htmlfile
echo "<body>" >> $htmlfile




addplancontent
addpricecontent





echo "</body>" >> $htmlfile
echo "</html>" >> $htmlfile
