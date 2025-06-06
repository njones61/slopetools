from global_config import non_circ
from slice import generate_slices
from fileio import load_globals
from plot import plot_solution, plot_inputs
from solve import oms, bishop, janbu_corrected, janbu, spencer, corps_engineers, lowe_karafiath


def solve_selected(func, df, circle=None, circular=True):
    success, result = func(df, circle=circle, circular=circular)
    if not success:
        print(f'Error: {result}')
        return result

    if func == oms:
        print(f'OMS: FS={result["FS"]:.3f}')
    elif func == bishop:
        print(f'Bishop: FS={result["FS"]:.3f}')
    elif func == spencer:
        print(f'Spencer: FS={result["FS"]:.3f}, theta={result["theta"]:.2f}')
    elif func == janbu_corrected:
        print(f'Janbu Corrected FS={result["FS"]:.3f}, fo={result["fo"]:.2f}')
    elif func == janbu:
        print(f'Janbu Corrected FS={result["FS"]:.3f}, fo={result["fo"]:.2f}')
    elif func == corps_engineers:
        print(f'Corps Engineers: FS={result["FS"]:.3f}, theta={result["theta"]:.2f}')
    elif func == lowe_karafiath:
        print(f'Lowe & Karafiath: FS={result["FS"]:.3f}')
    return result

def solve_all(df, circular=True):
    solve_selected(oms, df, circular=circular)
    solve_selected(bishop, df, circular=circular)
    solve_selected(oms, df, circular=circular)
    solve_selected(spencer, df, circular=circular)
    solve_selected(janbu_corrected, df, circular=circular)

data = load_globals("docs/input_template_lface.xlsx")

# plot_inputs(data)

circle = data['circles'][0] if data['circular'] else None
non_circ = data['non_circ'] if not data['circular'] else None

print(f"circle: {circle}")

success, result = generate_slices(data, circle, non_circ, num_slices=20)
if success:
    df, failure_surface = result
else:
    print(result)

# export df to excel
df.to_excel("slices.xlsx", index=False)

# options = [oms, bishop, spencer, janbu_corrected, corps_engineers, lowe_karafiath]
results = solve_selected(janbu, df, circle=circle, circular=True)

plot_solution(data, df, failure_surface, results)

# solve_all(df, circular=True)