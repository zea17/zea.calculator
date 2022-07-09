size = len(stack)
i = 0
while i < size:
    if stack[i] == "÷" or stack[i] == "×":
        op = stack[i]
        left = stack[i - 1]
        right = stack[i + 1]
        result = 0
        if op == "÷":
            result = left / right
        else:
            print("left", left, "right", right)
            result = left * right
        stack = stack[:i - 1] + [result] + stack[i + 2:]
        i++
