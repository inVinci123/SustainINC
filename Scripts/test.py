# import math

# str = input("String to be presented: ")#"AAAA aaaAa Lorem ipsum sit dolor ame..."
# if str == "": str = "This is atests\ntringthatiswayt\noolong\n"
# # str = "ab cd"
# max_size = input("Max Size: ")
# max_size = 10 if max_size == "" else int(max_size)# = 10

# lines = []

# str = str.strip().split("\n")
# for s in str:
#     n = math.ceil(len(s)/max_size)

#     for i in range(n):
#         line = s[i*max_size:(i+1)*max_size]
#         # print(line)
#         if line[-1] == ' ':
#             lines.append(line.strip())
#             # print("end was empty")
#         else:
#             try:
#                 if s[(i+1)*max_size] == ' ':
#                     # print("start of next was empty")
#                     lines.append(line.strip())
#                 else:
#                     # print(str[(i+1)*max_size], "was not expt")
#                     lines.append(line.strip()+'-')
#             except IndexError:
#                 # print("INDEX ERROR")
#                 lines.append(line.strip())
#             # => can be 'a|a', 'a| ', ' |a' 
# for l in lines:
#     print(l)
while True:
    startx = int(input("startx: "))*10 - 2560
    starty = int(input("starty: "))*10 - 2560
    endx = int(input("endx: "))*10 - 2560
    endy = int(input("endy: "))*10 - 2560

    sizx = endx-startx
    sizy = endy-starty

    outstr = f"""
        "xpos": {startx},
        "ypos": {starty},
        "xsiz": {sizx},
        "ysiz": {sizy}
    """
    outstr = "{" + outstr
    outstr += "}"
    print(outstr)
