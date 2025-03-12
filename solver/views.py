from django.shortcuts import render
import math
import re

def bisection_method(request):
    result = None
    error_message = None
    user_function = ''
    a = None
    b = None
    iterations = None

    if request.method == 'POST':
        try:
            a = float(request.POST.get('a'))
            b = float(request.POST.get('b'))
            iterations = int(request.POST.get('iterations'))
            func_str = request.POST.get('function', '').strip()
            user_function = func_str

            if not func_str:
                raise ValueError("PROTOCOL VIOLATION: Function field cannot be empty")

            # Auto-insert multiplication operators
            modified_func = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', func_str)
            modified_func = re.sub(r'([a-zA-Z)])(\d)', r'\1*\2', modified_func)

            def f(x):
                try:
                    return eval(modified_func, {'math': math}, {'x': x})
                except Exception as e:
                    raise ValueError(f"DECODE FAILURE: {str(e)} - Original input: {func_str}")

            fa = f(a)
            fb = f(b)

            if fa * fb >= 0:
                error_message = "GRID MISALIGNMENT: Coordinates do not bracket target"
            else:
                results = []
                previous_c = None
                current_a, current_b = a, b

                for i in range(1, iterations + 1):
                    c = (current_a + current_b) / 2
                    fc = f(c)
                    fxi = f(current_a)

                    error_percent = abs((c - previous_c)/c * 100) if previous_c and c != 0 else 0.0

                    results.append({
                        'iteration': i,
                        'a': current_a,
                        'b': current_b,
                        'c': c,
                        'f_x_i': fxi,
                        'f_c': fc,
                        'error_percent': error_percent
                    })

                    if f(current_a) * fc < 0:
                        current_b = c
                    else:
                        current_a = c

                    previous_c = c

                result = results

        except Exception as e:
            error_message = f"SYSTEM ALERT: {str(e)}"

    return render(request, 'bisection/index.html', {
        'result': result,
        'error_message': error_message,
        'user_function': user_function,
        'a': a,  # Pass the value of a back to the template
        'b': b,  # Pass the value of b back to the template
        'iterations': iterations  # Pass the value of iterations back to the template
    })