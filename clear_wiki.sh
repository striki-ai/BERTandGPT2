echo "step  1: remove xml tags"
sed -i 's/<[^>]*>//g' $1
echo "step  2: remove [[ and ]]"
sed -i 's/\(\[\[\|\]\]\)//g' $1
echo "step  3: remove '''"
sed -i "s/'''//g" $1
echo "step  4: remove {{ and }}"
sed -i 's/\({{\|}}\)//g' $1
echo "step  5: remove &(nbsp|lt|gt|amp|quot|apos);"
sed -i 's/&\(nbsp\|lt\|gt\|amp\|quot\|apos\);/ /g' $1
echo "step  6: remove ''"
sed -i "s/''//g" $1
echo "step  7: remove \" ndash \""
sed -i 's/ ndash / /g' $1
echo "step  8: remove leading *"
sed -i 's/^\(\*\*\*\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\|\*\*\*\*\*\*\|\*\*\*\*\*\|\*\*\*\*\|\*\*\*\|\*\*\|\*\) //g' $1
echo "step  9: remove leading * again"
sed -i 's/^\* //g' $1
echo "step 10: remove leading (Cc)ategory:"
sed -i 's/^\(C\|c\)ategory://g' $1
echo "step 11: remove leading spaces"
sed -i 's/^ *//g' $1
echo "step 12: remove wikiext and text/x-wiki at the beggining ot the lines"
sed -i 's/^\(wikitext\|text\/x-wiki\)//g' $1
echo "step 13: remove leading #"
sed -i 's/^\#//g' $1
echo "step 14: remove leading # from the rest"
sed -i 's/^\#//g' $1
echo "step 15: remove lines that start with File:"
sed -i 's/^File:.*//g' $1
echo "step 16: remove lines that start with {, | or !"
sed -i 's/^[{|\||!].*//g' $1
echo "step 17: remove starting admin| from lines"
sed -i 's/^admin|//g' $1
echo "step 18: remove starting user| from lines"
sed -i 's/^user|//g' $1
echo "step 19: remove lines that start with up to 5 # chars"
sed -i 's/^\(######\|#####\|####\|###\|##\|#\)//g' $1
echo "step 20: remove lines that start with --"
sed -i 's/^--.*//g' $1
echo "step 21: remove * at the beginning of the lines"
sed -i 's/^*//g' $1
echo "step 22: remove up to 4 : chars at the beginning of the lines"
sed -i 's/^(\:\:\:\:|\:\:\:|\:\:|\:)//g' $1
echo "step 23: remove up to 4 : chars at the beginning of the lines"
sed -i 's/^(\:\:\:\:|\:\:\:|\:\:|\:)//g' $1
echo "step 24: remove up to 4 : chars at the beginning of the lines"
sed -i 's/^(\:\:\:\:|\:\:\:|\:\:|\:)//g' $1
echo "step 25: remove up to 4 : chars at the beginning of the lines"
sed -i 's/^(\:\:\:\:|\:\:\:|\:\:|\:)//g' $1
echo "step 26: remove up to 4 : chars at the beginning of the lines"
sed -i 's/^(\:\:\:\:|\:\:\:|\:\:|\:)//g' $1
echo "step 27: ' nbsp;' text from the lines"
sed -i 's/ nbsp;/ /g' $1
echo "step 28: remove 'extent' from the beginning of the lines"
sed -i 's/^extent//g' $1
echo "step 29: remove ; from the beginning of the lines"
sed -i 's/^;//g' $1
echo "step 30: remove lines with digits only"
sed -i 's/^[0-9][0-9]*$//' $1
echo "step 31: remove lines with time only"
sed -i 's/^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z$//' $1
echo "step 32: remove lines with 31 random chars and numbers only"
sed -i 's/^\w\{31\}$//' $1
echo "step 33: remove text (including) !-- and --"
sed -i 's/\!\-\-.*\?\-\-//g' $1
echo "step 34: remove few tokens ..."
sed -i 's/\|\(thumbnail\|thumb\|\d\d*px\|right\|center\|left\|padding\|border\|bg\|border2\|bg2\|upright\)//g' $1
echo "step 35: remove |<digits>| (because sed doesn't understand \d)"
sed -i 's/\|[0123456789][0123456789]*px\|//g' $1
echo "step 36: remove multiple |s one by one"
sed -i 's/|||*//g' $1
echo "step 37: remove starting one or more : signs"
sed -i 's/^::*//g' $1
echo "step 38: remove two or more : signs"
sed -i 's/:::*//g' $1
echo "step 39: remove one or more space signs from the beginning of the lines"
sed -i 's/^  *//g' $1
echo "step 40: remove two or more space signs from the lines"
sed -i 's/   *//g' $1
echo "step 41: remove nowrap| from the lines"
sed -i 's/[Nn]owrap|//g' $1
echo "step 42: remove reflist from the beginning of the lines"
sed -i 's/^[Rr]eflist.*//g' $1
