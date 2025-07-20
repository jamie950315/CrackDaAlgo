def algo1(inputStr):
    total = 0
    length = len(inputStr)

    def charValue(c):
        if c.islower():
            return ord(c) - ord('a') + 1*length
        elif c.isupper():
            return -(ord(c) - ord('A') + 1*length)
        elif c.isdigit():
            return int(c) * length
        else:
            return 0

    for c in inputStr:
        total += charValue(c)

    digitSum = sum(int(d) for d in str(abs(total)))
    firstValue = charValue(inputStr[0])

    finalresult = digitSum-(firstValue*length) + (firstValue%length)*digitSum + total*length
    return finalresult

def algo2(inputStr):
    length = len(inputStr)
    shift = algo1(inputStr) % length

    for i in range(4):
        total = 0
        def charValue(c):
            if c.islower():
                return ord(c) - ord('a') + 1 + i*length + shift
            elif c.isupper():
                return -(ord(c) - ord('A') + 1 -i + shift*length)
            elif c.isdigit():
                return int(c) * (length + i + shift)
            else:
                return 0

        for c in inputStr:
            total += charValue(c) + shift*(charValue(c) % length)

        digitSum = sum(int(d) for d in str(abs(total)))
        firstValue = charValue(inputStr[0])
        if length>=2:
            secondValue = charValue(inputStr[1])
        else:
            secondValue = 0

        shift = digitSum + firstValue + secondValue

    finalresult = digitSum + firstValue + shift + secondValue

    return finalresult

def algo3(inputStr):
    shift = algo2(inputStr)
    length = len(inputStr)

    for i in range(4):
        total = 0
        def charValue(c):
            if c.islower():
                return ord(c) - ord('a') + (shift*length)%(shift-length) + i*length + shift*(i+length)
            elif c.isupper():
                return -(ord(c) - ord('A') + (algo1(str(shift))*length-algo2(inputStr)*i)%(shift-length*algo1(str(length))) -i + shift*length-i)
            elif c.isdigit():
                return int(c) * (length + i + shift*length*algo1(str(length+shift)))
            else:
                return 0

        for c in inputStr:
            total += charValue(c) + shift*(charValue(c) % length)

        digitSum = sum(int(d) for d in str(abs(total)))
        firstValue = charValue(inputStr[0])

        if length>=3:
            thirdValue = charValue(inputStr[2])
        else:
            thirdValue = 0

        shift = digitSum + firstValue + thirdValue

    finalresult = digitSum*algo1(inputStr*length) + algo1(str(shift+length*thirdValue))%(firstValue+length) + shift + ((shift*length)*firstValue%length) + (thirdValue*length) + algo2(inputStr)%(thirdValue+length+algo1(inputStr))


    return finalresult


def algo4(inputStr):
    shift = algo3(inputStr)+algo2(inputStr)
    length = len(inputStr)

    for i in range(4):
        total = 0
        def charValue(c):
            if c.islower():
                return ord(c) - ord('a') + algo1(str(i*length)) + i*length*algo2(str(shift+algo1(inputStr))) + shift*length
            elif c.isupper():
                return -(ord(c) - ord('A') + (i*length)%(shift-length) -i*algo1(str(algo2(inputStr))) + (shift*length-i)%length)
           
            elif c.isdigit():
                return int(c) * (length + i + shift*length)-(shift%algo1(str(length+i)))
            else:
                return 0

        for c in inputStr:
            total += charValue(c) + shift*(charValue(c) % length)

        digitSum = sum(int(d) for d in str(abs(total)))
        firstValue = charValue(inputStr[0])

        lastValue = charValue(inputStr[length-1])

        shift = digitSum+lastValue + ((firstValue+digitSum)*length) + (firstValue + lastValue)*length + (algo3(inputStr)+length)+(lastValue+algo3(inputStr)*length)

    finalresult = (digitSum*algo2(inputStr*length) + algo1(str(shift+length*algo2(str(shift*(firstValue-length)-algo1(inputStr)))))%(firstValue+shift) + shift%(algo1(str(firstValue-shift%length))+lastValue*length+firstValue) + (((shift*length)*(firstValue+lastValue))%length*algo2(inputStr)) + algo3(str((firstValue+lastValue)*length)))%(256*length*shift+algo3(str(shift+length)) + algo2(str(length*digitSum)) + algo1(inputStr))

    return finalresult


def algo5(inputStr):
    shift = (algo4(inputStr)-algo3(inputStr))*(algo2(inputStr)%algo1(inputStr))
    length = len(inputStr)

    for i in range(4):
        total = 0
        def charValue(c):
            if c.islower():
                return ord(c) - ord('a') + algo4(str(i*length)) + i*length*algo4(str(shift+algo4(inputStr))) + shift*length
            elif c.isupper():
                return -(ord(c) - ord('A') + (i*length)%(shift-length) -i*algo4(str(algo4(inputStr))) + (shift*length-i)%length)
           
            elif c.isdigit():
                return int(c) * (length + i + shift*length)%algo4(inputStr)-(shift%algo4(str(length+i)))
            else:
                return 0

        for c in inputStr:
            total += charValue(c) + shift*(charValue(c) % length)

        digitSum = sum(int(d) for d in str(abs(total)))
        firstValue = charValue(inputStr[0])
        lastValue = charValue(inputStr[length-1])

    finalresult = ((digitSum + shift + lastValue)*length+(algo4(str(lastValue*length+shift))))%(256*length + algo4(str(shift+length))) + algo4(str(length*digitSum)) + algo4(inputStr)

    return finalresult




import itertools
import string
import time

def crackCharSumPlus(target1, target2, target3, target4, target5, maxLength):
    attempt=0
    startTime=time.time()

    charset = string.ascii_letters + string.digits
    for length in range(1, maxLength+1):
        for candidate in itertools.product(charset, repeat=length):
            candidateStr = ''.join(candidate)
            result1 = algo1(candidateStr)
            attempt+=1
            if attempt % 50000 == 0:
                print(f"Trying {attempt}: {candidateStr} -> {result1}")
            if result1 == target1:
                if target2==algo2(candidateStr):
                    if target3==algo3(candidateStr):
                        print(f"Match found for algo3: {candidateStr} -> {target3}")
                        if target4==algo4(candidateStr):
                            print(f"Match found for algo4: {candidateStr} -> {target4}")
                            if target5==algo5(candidateStr):
                                elapsed_time = time.time() - startTime
                                print(f"\n[+] Found match: {candidateStr} -> {result1} | {target2} | {target3} | {target4} | {target5}\nElapsed time: {elapsed_time:.2f} seconds, attempts: {attempt}")
                                return candidateStr
    print("[-] No match found")
    return None

if __name__ == "__main__":

    pswd=input("Enter the password to crack: ")
    if not pswd:
        print("Will use 'pswd' as password.")
        pswd = "pswd"
    maxLength = 32

    target1 = algo1(pswd)
    target2 = algo2(pswd)
    target3 = algo3(pswd)
    target4 = algo4(pswd)
    target5 = algo5(pswd)
    print(f"Target1: {target1}, Target2: {target2}, Target3: {target3}, Target4: {target4}, Target5: {target5}\n")
    time.sleep(1)

    crackCharSumPlus(target1, target2, target3, target4, target5, maxLength)