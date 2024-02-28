python3 setops.py "set1=a1.txt;set2=b1.txt;operation=intersection"
diff -q result.txt res1.txt >/dev/null && echo "TEST CASE 1 PASSED" || echo "TEST CASE 1 FAILED"
python3 setops.py "set1=a2.txt;set2=b2.txt;operation=difference"
diff -q result.txt res2.txt >/dev/null && echo "TEST CASE 2 PASSED" || echo "TEST CASE 2 FAILED"

python3 setops.py "set1=a3.txt;set2=b3.txt;operation=union"
diff -q result.txt res3.txt >/dev/null && echo "TEST CASE 3 PASSED" || echo "TEST CASE 3 FAILED"

python3 setops.py "set1=a4.txt;set2=b4.txt;operation=intersection"
diff -q result.txt res4.txt >/dev/null && echo "TEST CASE 4 PASSED" || echo "TEST CASE 4 FAILED"
