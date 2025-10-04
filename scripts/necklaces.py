import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
#So, there are two methods for generating necklaces, my old one which is really bad 
# and another that's presented in this paper:

# https://www.sciencedirect.com/science/article/pii/019667749290047G

# I'm going to try and recreate that algorithm here but it might not work.

def cycle_list(l:list,loops:int = 1):
    """Used to cycle list elements so that everything is one step left

    Args:
        l (list): the list to cycle
        loops (int, optional): The number of steps to do. Defaults to 1.
    """
    n = len(l)
    if loops < 0:
        l = l[::-1]
    for t in range(np.abs(loops)):
        l = [l[(i+1) % n] for i in range(n)]
    if loops < 0:
        l = l[::-1]
    return(l)


def generate_unique_combinations(N,tqdm_disable = True):
    """Old Method

    Args:
        N (int): Number of elements long
    """
    combinations = generate_binary_strings(N)
    non_repeating = [combinations[0]]
    for i in tqdm(range(len(combinations)),desc = "Genearting Unique Binary Numbers",disable = tqdm_disable):
        ref = list(combinations[i])
        N = len(ref)
        test = 0
        for j in range(len(non_repeating)):
            for n in range(N):
                
                if cycle_list(list(non_repeating[j]),loops = n+1) == ref:
                    test += 1
        
        if test == 0:
            non_repeating.append(combinations[i])
            
    for i in np.arange(len(non_repeating)):
        non_repeating[i] = [int(s) for s in list(non_repeating[i])]
    return(non_repeating)

def generate_binary_strings(bit_count):
    """Generates all binary strings of length <bit_count>

    Args:
        bit_count (int): Number of bits

    Returns:
        list: list of binary strings
    """
    binary_strings = []
    def genbin(n, bs=''):
        #not sure this is great but it does work...kinda?
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + '0')
            genbin(n, bs + '1')


    genbin(bit_count)
    return binary_strings

# Now for the new
# I think the idea is to generate a tree. then you keep the tree going if and only if the output is a valid necklace
# though this is not clear to me how we check that.

def tau_fn(binary_list):
    binary_list[-1] = abs(binary_list[-1] -1)
    return(binary_list)

def check_necklace(current_output,candidate):
    for l in range(len(candidate)):
        if cycle_list(candidate,l) in current_output:
            return(False)
    else:
        return(True)

def check_children(bn,current_output,pbar):
    if check_necklace(bn,current_output):
        for n in range(1,len(bn) -1):
            child = tau_fn(cycle_list(bn,n))
            if check_necklace(current_output,child):
                pbar.update(1)
                current_output.append(child)
                current_output = check_children(child,current_output,pbar)
    return(current_output)

def bin_to_int(all_binaries):
    binary_strings = ["0b" + "".join([str(ab_) for ab_ in ab]) for ab in all_binaries]
    binary_base_10 = [int(bs,2) for bs in binary_strings]
    return(binary_base_10)
def standardise_binary(b_list):
    # goal here is to make the binary number the lowest it can be
    all_binaries = [cycle_list(b_list,n) for n in range(len(b_list))]

    #this line is super slow so might need updated
    binary_base_10 = bin_to_int(all_binaries)
    return(all_binaries[binary_base_10.index(min(binary_base_10))])

def order_binary(final_output):
    value_list = bin_to_int(final_output)
    final_output = [bn for _, bn in sorted(zip(value_list,final_output))]
    return(final_output)
def generate_unique_necklaces(n,tqdm_disable = True,tqdm_total = 632):

    #assumme tqdm total, need to write code that can calculate this from n

    
    
    #we start at all 0s
    #define binary numbers as lists of values for now
    # I could deal in strings but not necessarily keen to right now
    # therefore 0^n = [0]*n (i.e. 0^2 = [0,0])
    final_output = []
    zero_n = [0]*n
    final_output.append(zero_n) #cause this is a given
    
    with tqdm(total = tqdm_total,disable = tqdm_disable) as pbar:
        final_output = check_children(zero_n,final_output,pbar = pbar)
        #this step not strictly necessary but it helps with keeping things standard
        final_output = [standardise_binary(b) for b in final_output]
        final_output = order_binary(final_output)
    return(final_output)


if __name__ == "__main__":
    import timeit
    
    t_start = timeit.default_timer()
    new_N = generate_unique_necklaces(13,tqdm_disable=False)
    t_end = timeit.default_timer()
    print(f"New Method: {(t_end - t_start):.1f}s | n_uniques = {len(new_N)}")

    t_start = timeit.default_timer()
    old_N = generate_unique_combinations(13,tqdm_disable=False)
    t_end = timeit.default_timer()
    print(f"Old Method: {(t_end - t_start):.1f}s | n_uniques = {len(old_N)}")
    