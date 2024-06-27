import cProfile
import pstats
import io

def profile_code():
    # Your code to profile
    result = 0
    for i in range(1, 1000000):
        result += i
    return result

def main():
    pr = cProfile.Profile()
    pr.enable()
    profile_code()
    pr.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats()
    print(s.getvalue())

if __name__ == "__main__":
    main()
