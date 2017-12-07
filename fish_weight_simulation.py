"""
PROBLEM:

Fish Weight Simulation

Fish weight growth can be modeled as function of species' biophysical
characteristics and ambient water temperature. Given the current weight of a
fish (`weight_cur`), the new weight for a day's worth of growth in Alaskan
Salmon can be calculated as

    weight_new = (alpha * weight_cur^beta * e^(temp_cur * tau)) + weight_cur

where
    alpha = 0.038,
    beta = 0.6667,
    tau = 0.08,
    temp_cur is the current water temperature in degrees C,
    and the weight of the fish is in grams.

Targets:
    - Correctness
    - Readability
    - Simplicity

SOLUTION:
    - Rewrite the growth formula
        w[n+1] = f(w[n], t[n]) + w[n]
    - The simplest approximation would be an explicit iteration:
        w_tomorrow = f(w_today, t_today) + w_today
    - This looks best implemented by reduction in plain Python
        accumulated = f(accumulated, t[i]) + accumulated
"""

from math import exp


def simulate(initial_weight, data_file):
    """
    A standard read-check-run-display flow of simulators
        if users only want the raw input-to-output function, use the simulate_weight instead

    Args:
        initial_weight (float): the weight of the fish on day 1
            of recorded temperature data
        data_file (string): path to the temperature data_file.
            Format is comma delimited (csv), with labels, temperatures in 3rd column.

    Return:
        None
    """

    # read temperature data from sources
    temperature_data = read_data(data_file)

    # check for data validity, to avoid "garbage in, garbage out" results
    check_sanity({
        't': temperature_data,
        'w0': initial_weight
    })

    # main computation
    final_weight = simulate_weight(initial_weight, temperature_data)

    # display outputs
    output({
        'initial_weight': initial_weight,
        'final_weight': final_weight
    })


def simulate_weight(w0, temperatures):
    """
    The main computation of final weight given inputs

    Args:
        w0 (float): initial weight
        temperatures (float list): an array contains temperature
            on a range of continuous day

    Returns:
        final weight (float): the fish weight after last day of
            temperature recording
    """

    # the main formula for reduction-based implementations
    def formula(weight_cur, temp_cur):
        alpha = 0.038
        beta = 0.6667
        tau = 0.08
        return alpha * weight_cur ** beta * exp(temp_cur * tau) + weight_cur

    return reduce(formula, temperatures, w0)


def read_data(data_file):
    """
    Reading temperature data from a specified csv file

    Args:
        data_file (string): a comma delimited file with labels and 3 data columns

    Returns:
        (float list): an array of recorded temperatures
    """
    # we could use the fancy pandas.read_csv but let's stick to simplicity
    with open(data_file, 'r') as file:
        # this is standard text file reading procedure
        data = file.read()

    # extract and transform data steps
    data = data.split('\n')

    # remove empty entries
    # for ex. very often the last line is empty due to windows/linux
    # last empty line convention
    data = filter(bool, data)
    labels = data[0].split(',')
    data = [d.split(',') for d in data[1:]]

    temperatures = map(float, [d[2] for d in data])

    return temperatures


def check_sanity(data):
    """
    Check if the quantities are physically valid
    """

    assert data['w0'] > 0, 'Invalid initial weight, should be positive.'

    temperatures = data['t']
    assert len(temperatures) > 0, 'Empty temparature data'
    assert (all(map(lambda t: t > -273, temperatures)),
            'Invalid temperatures, should be larger than -273C')


def output(data):
    """
    Display the results to the screen
    could be customized to write to files
    """
    print '---Fish growth simulation program---\n'.upper()
    print 'Initial weight: {:9.02f} grams'.format(data['initial_weight'])
    print 'Final weight:   {:9.02f} grams'.format(data['final_weight'])

    growth = data['final_weight'] / data['initial_weight']
    print 'which is:       {:>9.0f} times bigger'.format(growth)
    print '\n---End of simulation---'.upper()


def test():
    """
    A simple test based on 1 gram of initial weight and the provided temperatures
    """
    temperature_data = read_data('temperature_series.csv')

    results = simulate_weight(1, temperature_data)
    answer = 1858.44736351

    assert abs(results - answer) < 1e-5, 'Inaccurate simulation'


if __name__ == '__main__':
    print 'Running tests ...'.upper()
    test()
    print 'All tests passed!\n'.upper()

    simulate(1, 'temperature_series.csv')
