```python
# 입력
(python -c 'print "A"';cat) | ./target

# 여러개의 입력을 받을 때
(python -c 'print "AndNextOne"';cat) | (python -c 'print "ThisFirst"';cat) | ./target


# 인자를 받을 때
./target `python -c 'print "A"'`

#인자를 여러 개 받을 때
./target `python -c 'print "First" + " " + "Second"'`
```
