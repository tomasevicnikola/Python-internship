import os

filename = input("Enter file name: ")

name, extension = os.path.splitext(filename)

if not extension:
    raise ValueError("No extension found")

print(f"The file extension is: {extension}")