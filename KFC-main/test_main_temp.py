from classes.pieces.bishop import Bishop

def main():
    b = Bishop('white')

    if b.can_move((2,0), (3,1)):
        print("SUCCESS")
    else:
        print("FAILURE")

    if b.can_move((7, 7), (0,0)):
        print("SUCCESS")
    else:
        print("FAILURE")

    if b.can_move((7, 0), (0,7)):
        print("SUCCESS")
    else:
        print("FAILURE")
    if b.can_move((1, 0), (7,6)):
        print("SUCCESS")
    else:
        print("FAILURE")
        
    if not b.can_move((2,0), (3,0)):
        print("SUCCESS")
    else:
        print("FAILURE")


    print(b.pass_through((2,0), (3,1)))
    print(b.pass_through((7, 7), (0,0)))
    print(b.pass_through((0, 0), (7,7)))
    print(b.pass_through((1, 0), (7, 6)))
    print(b.pass_through((7, 6), (1, 0)))













if __name__ == '__main__':
    main()