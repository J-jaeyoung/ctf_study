# GDB 사용법 정리


set disassembly-flavor intel
`%eax로 보임`

set disassembly-flavor att
`eax로 보임`


disas [함수 이름]
`함수의 어셈블리 코드를 보여줌` `+현재 eip의 위치를 =>로 보여줌`

b *메모리주소
`메모리 주소 또는 함수의 이름, 혹은 offset만큼 떨어진 곳에 bp를 걸어줌`
>b *main  
b *0x00401000  
b *0xmain+0

info b
`bp들을 모두 보여줌`

d [bp의 번호]
`bp 삭제`

r [argument]
`gdb 상에서 프로그램에 argument를 넘겨주며 실행`

c
`bp 걸린 부분부터 이어하기`

ni
`다음 instruction 실행`

info reg(또는 i r)
`레지스터 정보를 출력`

bt
`함수 Call Stack을 출력`

print [Variable Name | Expression]
`Variable의 현재 값이나 Exp의 결과값을 출력`

info address [function name]
`특정 function의 메모리 주소를 출력`


i r $esp $ebp
`esp와 ebp의 값만 보여줌`

----------------------------------


*출력관련*
```
# 바이트 옵션
x/b 0x004010000 -> 0x55
x/h 0x004010000 -> 0x8955
x/w 0x004010000 -> 0x83e58955

# 진법 옵션
x/x 0x004010000 -> 0x83e58955
x/u 0x004010000 -> 2212858197

# 레지스터 보기($register_name)
x/4wx $esp  ->  0x00000000 0x00000000 0x00000000 0x00000000
```
* 바이트나 진법 옵션은 설정하지 않으면 이전 옵션으로 실행
