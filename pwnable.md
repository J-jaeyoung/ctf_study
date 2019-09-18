### fd
setuid비트: set되어있으면 실 사용자에서 프로그램 소유자의 ID로  유효사용자(EUID)가 변경됨 
            -> 일반 사용자가 프로그램 실행중에만 root권한을 얻을 수 있음

실행파일의 소유자'실행' 권한에 s
'chmod u+s setuid2' or 'chmod 4777 setuid2'

```
int fd = atoi( argv[1] ) - 0x1234;
int len = 0;
len = read(fd, buf, 32);
```
read(a,b,c)에서 a는 파일 디스크립터 값, b는 읽은 데이터를 저장할 버퍼, c는 얼마나 읽을지
파일 디스크립터(file descriptor): 시스템이 할당해준 파일이나 소켓을 대표하는 정수
            표준입력:0      표준출력:1      표준에러출력:2



### col
