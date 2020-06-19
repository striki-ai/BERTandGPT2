echo "step  1"
sed -i 's/<[^>]*>//g' $1
echo "step  2"
sed -i 's/\(\[\[\|\]\]\)//g' $1
echo "step  3"
sed -i "s/'''//g" $1
echo "step  4"
sed -i 's/\({{\|}}\)//g' $1
echo "step  5"
sed -i 's/&\(nbsp\|lt\|gt\|amp\|quot\|apos\);/ /g' $1
echo "step  6"
sed -i "s/''//g" $1
echo "step  7"
sed -i 's/ ndash / /g' $1
echo "step  8"
sed -i 's/^\(\*\*\*\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\*\|\*\*\*\*\*\*\*\|\*\*\*\*\*\*\|\*\*\*\*\*\|\*\*\*\*\|\*\*\*\|\*\*\|\*\) //g' $1
echo "step  9"
sed -i 's/^\* //g' $1
echo "step 10"
sed -i 's/^\(C\|c\)ategory://g' $1
echo "step 11"
sed -i 's/^ *//g' $1
echo "step 12"
sed -i 's/^\(wikitext\|text\/x-wiki\)//g' $1