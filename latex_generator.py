from tester import load_rules

filenames = ["2b/_1",
             "2b/_3",
             "3a/_1",
             "5b/_6"]
for short in filenames:
    filename = f"output/phase{short}_log.txt"
    print(f"Reading {filename}")
    rules = load_rules(filename);
    for i in range(13):
        a = i
        b = i + 13
        c = i + 26
        d = i + 39
        print(f"{a + 1} & {rules[a]} & {b + 1} & {rules[b]} & {c + 1} & {rules[c]} & {d + 1} & {rules[d]} \\\\")
        print("\\hline")
    print("\n\n\n\n\n")
