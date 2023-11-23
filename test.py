
def main():
    print(len("[PASSING CITATIONS]"))
    exit(1)
    for chunk in generator():
        print(chunk)

def generator():
    for i in range(0, 20):
        yield(i)
    yield "Done"
if __name__=="__main__":
    main()