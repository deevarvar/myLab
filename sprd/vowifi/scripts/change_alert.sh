#!/bin/bash
# author: zhihua.ye@spreadtrum.com

#column definition
hashcol=1
adcol=2
cecol=3
msgcol=4
format="%h|%ad|%ce|%B"
tmphash="x"
declare -a libdir=("avatar" "adapter" "lemon" "melon" "watermelon" "grape" "service" "security" "app")

zfile="result"
zfile=$(readlink -f $zfile)
htmlfile="code_changes.html"
htmlfile=$(readlink -f $htmlfile)
: > $zfile
: > $htmlfile


function gennotes()
{
	today=$(date +%Y-%m-%d-%H:%M)
	yesday=$(date -d "1 day ago" +%Y-%m-%d-%H:%M)
	echo "<p> from $yesday to $today, code changes are listed below:</p>" >> $htmlfile
	echo "<p>You can click the commit's bitbucket link to view the changes</p>" >> $htmlfile
	echo "<p>bitbucket login account is in the juphoon_code_usage.docx </p>" >> $htmlfile
}


function genhtmlopen()
{
echo "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN http://www.w3.org/TR/html4/loose.dtd\">" >> $htmlfile
echo "<html>" >> $htmlfile
echo "<head>" >> $htmlfile
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">" >> $htmlfile
#echo "<style type=\"text/css\">" >> $htmlfile
#echo "table {border-collapse: collapse;}" >> $htmlfile
#echo "td {padding: 0px;text-align: center;}" >> $htmlfile
#echo "</style>" >> $htmlfile
gennotes


echo "</head>" >> $htmlfile
echo "<body>" >> $htmlfile
}



function genhtmlclose(){

echo "</body>" >> $htmlfile
echo "</html>" >> $htmlfile

}


function resetver()
{
#just reset to HEAD~3
	git reset --hard HEAD~3
}

function gethash()
{
tmp=$(git log -1 --pretty=format:'%h|%ad|%ce|%B'| tr '\n' ' ')
tmphash=$(echo $tmp | cut -d '|' -f $hashcol)
tmpmsg=$(echo $tmp | cut -d '|' -f "$msgcol"-)
#echo $tmp
#echo $tmphash
#echo $tmpmsg
	
}

function getdiff()
{

repodir=$1

if [ -z "$repodir" ]
then
	echo "You should enter a correct dir name"
	exit -1
fi

echo trying to get diff in $repodir, now is $(date +%Y-%m-%d-%H:%M:%S)
echo $repodir >> $zfile 

echo "<br>" >> $htmlfile
echo "<table border=\"1\">" >> $htmlfile
echo "<caption>$repodir commits today</caption>" >> $htmlfile
echo "<th>hash id</th>" >> $htmlfile
echo "<th>author date</th>" >> $htmlfile
echo "<th>committer email</th>" >> $htmlfile
echo "<th>commit msg</th>" >> $htmlfile

cd $repodir
#for test 
resetver
gethash
prevhash=$tmphash
git pull
gethash
curhash=$tmphash


#add check if curhash == prevhash
if [ "$curhash" != "$prevhash" ]
then
	changes="$repodir.changes"
	git log $prevhash..$curhash --pretty=format:'%h' > $changes
	#just append one more \n
	echo >> $changes
	while read commitid
	do
		#echo hash is $commitid
		tmp=$(git log -1 $commitid --pretty=format:'%h|%ad|%ce|%B'| tr '\n' ' ')
		echo $tmp >>  $zfile
		cid=$(echo $tmp | cut -d '|' -f 1)
		ad=$(echo $tmp | cut -d '|' -f 2)
		ce=$(echo $tmp | cut -d '|' -f 3)
		cmsg=$(echo $tmp | cut -d '|' -f 4-)

      	        echo "<tr>" >> $htmlfile
                echo "<td>$cid</td>" >> $htmlfile
                echo "<td>$ad</td>" >> $htmlfile
                echo "<td>$ce</td>" >> $htmlfile
                echo "<td>$cmsg</td>"  >> $htmlfile
                echo "</tr>" >> $htmlfile
	done  < $changes
	
	echo "</table>" >> $htmlfile


else
	echo no update
fi

cd ..
}

: <<  COMMENT
COMMENT


genhtmlopen

for lib in "${libdir[@]}"
do
	echo start to check "$lib"
	getdiff $lib
done

genhtmlclose

