#!/bin/bash
# author: zhihua.ye@spreadtrum.com

#column definition
hashcol=1
adcol=2
cecol=3
msgcol=4
format="%h|%ad|%ce|%B"
tmphash="x"
bitbucketurl="https://bitbucket.org/vowifi_team"
codedir=/home/apuser/juphoon_code/bitbucket
mailflag=0
declare -a libdir=("avatar" "adapter" "lemon" "melon" "watermelon" "grape" "service" "security" "app" "ImsCm")
defaultinter="30 mins ago"
interval=${1:-$defaultinter}



cd $codedir
mkdir -p log
datedir=log/$(date +%Y-%m-%d-%H-%M-%S)
datedir=$(readlink -f $datedir)
mkdir -p $datedir 
htmlfile="$datedir/code_changes.html"
allcommits="$datedir/allcommits"
: > $htmlfile


function gennotes()
{
	now=$(date +%Y-%m-%d-%H:%M)
	before=$(date -d "$interval" +%Y-%m-%d-%H:%M)
	echo "<h1>Code changes in last $interval, from $before to $now</h1>" >> $htmlfile
	echo "<p>You can click the commit id's bitbucket link to view the changes</p>" >> $htmlfile
	echo "<p>bitbucket login account is in the juphoon_code_usage.docx </p>" >> $htmlfile
}


function genhtmlopen()
{
echo "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN http://www.w3.org/TR/html4/loose.dtd\">" >> $htmlfile
echo "<html>" >> $htmlfile
echo "<head>" >> $htmlfile
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">" >> $htmlfile
echo "<style type=\"text/css\">" >> $htmlfile
echo "caption {font-weight: bold;font-size: 160%;}" >> $htmlfile
echo "</style>" >> $htmlfile
gennotes


echo "</head>" >> $htmlfile
echo "<body>" >> $htmlfile
}



function genhtmlclose(){

echo "</body>" >> $htmlfile
echo "</html>" >> $htmlfile

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

cd $repodir
#for test 
#resetver


git pull

repocommits="$allcommits.$repodir"
git log --since="$interval" --pretty=format:'%h' > $repocommits


if [ -s $repocommits ]
then
	mailflag=1
	echo "<br>" >> $htmlfile
	echo "<table border=\"1\">" >> $htmlfile
	echo "<caption>$repodir commits today</caption>" >> $htmlfile
	echo "<th>hash id</th>" >> $htmlfile
	echo "<th>author date</th>" >> $htmlfile
	echo "<th>committer email</th>" >> $htmlfile
	echo "<th>commit msg</th>" >> $htmlfile
	#curhash=$(head -n 1 $repocommits)
	#prevhash=$(tail -n 1 $repocommits)
	#echo in $repodir , prevhash is $prevhash, curhash is $curhash 
	#changes="$datedir/$repodir.changes"
	#git log $prevhash~1..$curhash --pretty=format:'%h' > $changes
	#just append one more \n
	echo >> $repocommits
	while read commitid
	do
		echo hash is $commitid
		tmp=$(git log -1 $commitid --pretty=format:'%h|%ad|%ce|%B'| tr '\n' ' ')
		cid=$(echo $tmp | cut -d '|' -f 1)
		ad=$(echo $tmp | cut -d '|' -f 2)
		ce=$(echo $tmp | cut -d '|' -f 3)
		cmsg=$(echo $tmp | cut -d '|' -f 4-)
		cid="<a href=\"${bitbucketurl}/$repodir/commits/$cid\">$cid</a>"
      	        echo "<tr>" >> $htmlfile
                echo "<td>$cid</td>" >> $htmlfile
                echo "<td>$ad</td>" >> $htmlfile
                echo "<td>$ce</td>" >> $htmlfile
                echo "<td>$cmsg</td>"  >> $htmlfile
                echo "</tr>" >> $htmlfile
	done  < $repocommits
	
	echo "</table>" >> $htmlfile

else
	echo no update
fi

cd ..
}

function sendemail()
{
	cat $htmlfile | mutt -s "daily code changes" -e "my_hdr From:vowifi_mailer@spreadtrum.com" -e "set content_type=text/html"  -- zhihua.ye@spreadtrum.com #Sally.He@spreadtrum.com Zhaodi.Chen@spreadtrum.com 
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

if [ "$mailflag" == 1 ]
then
	sendemail
else
	echo "All repo is up to date."
fi
