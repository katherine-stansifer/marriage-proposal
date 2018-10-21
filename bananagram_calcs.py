# A program to determine how letter distributions in banagrame must be
# altered to allow spelling of marriage proposal to Paul Stansifer!
import string, random, copy
def assess_prob(distro, target_strs, num_letters, num_trials):
    """Given a distribution of letters and target strings, determine
    the probability of being able to spell at least one of the target
    strings
    Arguments: distro: dictionary mapping letters to their counts in
    the current banagrams set (assume that all 26 upper-case letters
    are included and that counts are whole numberg)
    target_str: list of strings that I would like to be able to spell
    num_letters: number of letters to draw
    num_trials: number of simulation trials to run
    Returns a tuple of (probability of drawing at least one of the
    targets, dictionary with number of successes for each target)
    """
    
    overall_success = 0
    success_counts = dict(zip(target_strs, [0]*len(target_strs)))
    # Concatenate all the letters in the current distribution together
    # into one string for sampling purposes
    distro_str = ''.join([letter*current_distro[letter]
                          for letter in string.ascii_uppercase])
    for i in range(num_trials) :
        randstr = random.sample(distro_str, num_letters)
        successful = []
        for target in target_strs:
            successful.append(True)
            for letter in list(set(target)):
                if target.count(letter) > randstr.count(letter):
                    successful[-1] = False
            if successful[-1]:
                success_counts[target] += 1
        if True in successful:
            overall_success += 1
    return (overall_success/float(num_trials), success_counts)

# Distribution of letters in an unaltered banagrams set
baseline_distro = {'J':2, 'K':2, 'Q':2, 'X':2, 'Z':2,
    'B':3, 'C':3, 'F':3, 'H':3, 'M':3, 'P':3, 'V':3, 'W':3, 'Y':3,
    'G':4, 'L':5, 'D':6, 'S':6, 'U':6, 'N':8, 'T':9, 'R':9, 'I':11,
    'O':12, 'A':13, 'E':18}

# Strings I want to be able to spell
target_strs = ['WILLYOUMARRME', 'WILLYOUMARRYE', 'MARRYEPAUL', 'MARRYEPLEASE']

# Require that there is probability of probability_threshold of having
# at least one target_str after drawing num_letters
prob_threshold = 0.95
num_letters = 60

# Number of trials to run for assessing probability
num_trials = 5000

# Maximum bananagrams sets to combine
max_sets = 3

# Determine the letter in the target_strs
letters_in_target = set(''.join(target_strs))
other_letters_set = \
    set(string.ascii_uppercase).difference(letters_in_target)

#Before altering distribution, determine baseline probability of
#being able to spell target with a normal bananagrams set
current_distro = copy.copy(baseline_distro)
current_prob = assess_prob(current_distro, target_strs, num_letters,
                           num_trials)[0]

# Alter the letter distribution (keeping the total number of letters
# constant) one letter at a time until the probability of being able
# to spell at least one of the target strings reaches prob_threshold
while current_prob < prob_threshold:
    # Increase each letter by 1 and keep track of probability
    # increases
    prob_diffs = []
    for letter in letters_in_target:
        if current_distro[letter] < baseline_distro[letter] * max_sets:
            current_distro[letter] +=1
            prob_diffs.append((assess_prob(current_distro,
                                           target_strs,
                                           num_letters, num_trials)[0]
                               - current_prob, letter))
            current_distro[letter] -=1
        else:
            prob_diffs.append((-100, letter))
    # Add one of the letter that increases probability the most, and
    # remove a random letter not in any of the target strings
    current_distro[max(prob_diffs)[1]] += 1
    other_letters_str = ''.join([letter*current_distro[letter]
                                 for letter in
                                 list(other_letters_set)])
    current_distro[random.sample(other_letters_str, 1)[0]] -= 1
    current_prob = assess_prob(current_distro, target_strs,
                               num_letters, num_trials)[0]
    print max(prob_diffs), current_prob

# Output results (number of letters to add or subtract)
print assess_prob(current_distro, target_strs, num_letters,
                  num_trials)
for letter in string.ascii_uppercase:
    if baseline_distro[letter] != current_distro[letter]:
        print letter, current_distro[letter] - baseline_distro[letter]
