#!/bin/bash
#author: yezhihua@baidu.com

cityfield=1
idfield=2
namefield=3
timefield=7
weekdayfield=8
primetime=14
htmlfile=xingmei_monitor.html


sed -n '2,$p' wrongprice.csv |awk -F, '{print $2}'|sort -n|uniq > cinema.list


: > $htmlfile
echo "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN http://www.w3.org/TR/html4/loose.dtd\">" >> $htmlfile
echo "<html>" >> $htmlfile
echo "<head>" >> $htmlfile
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf8\">" >> $htmlfile
echo "<style type=\"text/css\">" >> $htmlfile
echo "table {border-collapse: collapse;}" >> $htmlfile
echo "td {padding: 0px;text-align: center;}" >> $htmlfile
echo "</style>" >> $htmlfile
echo "</head>" >> $htmlfile
echo "<body>" >> $htmlfile

echo "<p> 详细场次请见附件wrong.csv</p>" >> $htmlfile
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
echo "<p>1.	权重 4 一线城市影城 0：00 – 2：00  6折 ，周一至五 2：00 – 17:15 3D影片结算价30元，2D影片结算价25元； 17：15以后 6折。 六日 2:00 – 12：00 3D影片结算价 30元， 2D影片结算价25元；以后6折。</p>" >> $htmlfile
echo "<p>2.	权重 5 二线城市影城 0：00 – 2：00  6折 ，周一至五 2：00 – 17:15 3D影片结算价25元，2D影片结算价20元； 17：15以后 6折。 六日 2:00 – 12：00 3D影片结算价25元， 2D影片结算价20元；以后6折。</p>" >> $htmlfile
echo "<p>3.	权重 6 四个影城（北京金源、上海正大、成都环球中心、拉萨神力）周一至五 2：00 – 17:15 所有片结算价30元， 17：15以后 7折， 六日 2:00 – 12：00 所有片结算价 30元， 以后7折</p>" >> $htmlfile
echo "<p>4.	影厅类型非普通厅（包括 VIP厅、Imax厅、巨幕厅、贵宾厅） 影片类型非普通影片（包括 Imax Dmax 等非2D 3D）的场次都为原价。</p>" >> $htmlfile
echo "</body>" >> $htmlfile
echo "</html>" >> $htmlfile
