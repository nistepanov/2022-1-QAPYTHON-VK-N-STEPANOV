#!/bin/bash
echo Total requests
cat access.log | grep -E '"GET|"POST|"PUT|"PATCH|"DELETE|"COPY|"HEAD|"OPTIONS|"LINK|"UNLINK|"PURGE|"LOCK|"UNLOCK|"PROPFIND|"VIEW' | wc -l

echo -e "\nTotal requests by type:"
COUNT_GET=$(cat access.log | grep -E '"GET' | wc -l)
echo GET - $COUNT_GET

COUNT_POST=$(cat access.log | grep -E '"POST' | wc -l)
echo POST - $COUNT_POST

COUNT_PUT=$(cat access.log | grep -E '"PUT' | wc -l)
echo PUT - $COUNT_PUT

COUNT_DELETE=$(cat access.log | grep -E '"DELETE' | wc -l)
echo DELETE - $COUNT_DELETE

COUNT_PATCH=$(cat access.log | grep -E '"PATCH' | wc -l)
echo PATCH - $COUNT_PATCH

COUNT_OPTIONS=$(cat access.log | grep -E '"OPTIONS' | wc -l)
echo OPTIONS - $COUNT_OPTIONS

COUNT_HEAD=$(cat access.log | grep -E '"HEAD' | wc -l)
echo HEAD - $COUNT_HEAD

COUNT_LINK=$(cat access.log | grep -E '"LINK' | wc -l)
echo LINK - $COUNT_LINK

COUNT_UNLINK=$(cat access.log | grep -E '"UNLINK' | wc -l)
echo UNLINK - $COUNT_UNLINK

COUNT_PURGE=$(cat access.log | grep -E '"PURGE' | wc -l)
echo PURGE - $COUNT_PURGE

COUNT_LOCK=$(cat access.log | grep -E '"LOCK' | wc -l)
echo LOCK - $COUNT_LOCK

COUNT_UNLOCK=$(cat access.log | grep -E '"UNLOCK' | wc -l)
echo LOCK - $COUNT_UNLOCK

COUNT_PROPFIND=$(cat access.log | grep -E '"PROPFIND' | wc -l)
echo PROPFIND - $COUNT_PROPFIND

COUNT_VIEW=$(cat access.log | grep -E '"VIEW' | wc -l)
echo VIEW - $COUNT_VIEW

echo -e "\nTop 10 requests by usage:"
cat access.log | cut -d' ' -f7 | sort | uniq -c | sort -k1 -nr | head -10

echo -e "\nTop 5 requests by response size ended with 4** error:"
cat access.log | awk '$9 ~ /4[0-9][0-9]/ {print $7 " " $9 " " $10 " " $1}' | sort -k3 -nr | head -5

echo -e "\nTop 5 users by count of requests ended with 5** error:"
cat access.log | awk '$9 ~ /5[0-9][0-9]/ {print  $1}' | sort | uniq -c | sort -k1 -nr | head -5

exit 100
